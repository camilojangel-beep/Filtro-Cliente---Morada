from __future__ import annotations

import pytest

from app.config import settings
from app.models.experian import (
    Aportante,
    ExperianData,
    ExperianResponse,
    ResultadoPago,
)
from app.models.solicitud import (
    EmpleadorFlag,
    EvaluarIngresoRequest,
    Parentesco,
)
from app.services.ingreso import (
    VectorPago,
    aplicar_tabla_decisiones,
    calcular_ingreso_solicitante,
    consolidar_vector,
    determinar_inicio_vector,
    evaluar_ingreso,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hacer_pagos(pagos_desc: list[tuple[int, int, bool, float]]) -> list[ResultadoPago]:
    """Crea lista de ResultadoPago a partir de tuplas (año, mes, pago, ingreso)."""
    return [
        ResultadoPago(
            ano_periodo_validado=a,
            mes_periodo_validado=m,
            realizo_pago=p,
            ingresos=i,
        )
        for a, m, p, i in pagos_desc
    ]


def _hacer_aportante(
    nit: str = "900111222",
    pagos: list[ResultadoPago] | None = None,
    retiro: bool = False,
    licencia: bool = False,
) -> Aportante:
    return Aportante(
        tipo_identificacion_aportante_id=2,
        numero_identificacion_aportante=nit,
        razon_social_aportante=f"Empresa {nit}",
        tipo_cotizante_persona_natural=1,
        descripcion_cotizante_persona_natural="Empleado",
        tiene_novedad_retiro_actualmente_empleado=retiro,
        tiene_licencia_no_remunerada_actualmente_empleador=licencia,
        resultado_pagos=pagos or [],
    )


def _hacer_experian(
    cedula: str = "102449000",
    aportantes: list[Aportante] | None = None,
    fecha: str = "04/23/2026 04:58:50 PM",
) -> ExperianResponse:
    return ExperianResponse(
        id="test-id",
        status="APPROVED",
        data=ExperianData(
            fecha=fecha,
            numero_identificacion_persona_natural=cedula,
            aportantes=aportantes or [],
        ),
    )


def _vector_desde_flags(flags: list[tuple[bool, float]]) -> list[VectorPago]:
    """Crea vector descendente desde 2026-03 hacia atrás."""
    vector = []
    anio, mes = 2026, 3
    for pago, ingreso in flags:
        vector.append(VectorPago(anio=anio, mes=mes, realizo_pago=pago, ingresos=ingreso))
        mes -= 1
        if mes == 0:
            mes = 12
            anio -= 1
    return vector


# ===========================================================================
# 8.1.1 — Determinación del inicio del vector
# ===========================================================================


class TestDeterminarInicioVector:
    def test_dia_20_o_posterior_usa_mes_cero(self):
        vector = _vector_desde_flags([(True, 2_000_000)])
        assert determinar_inicio_vector(vector, dia_consulta=20) == 0
        assert determinar_inicio_vector(vector, dia_consulta=25) == 0

    def test_dia_anterior_a_20_con_ingreso_usa_mes_cero(self):
        vector = _vector_desde_flags([(True, 2_000_000)])
        assert determinar_inicio_vector(vector, dia_consulta=10) == 0

    def test_dia_anterior_a_20_sin_ingreso_salta_a_mes_menos_1(self):
        vector = _vector_desde_flags([(False, 0), (True, 2_000_000)])
        assert determinar_inicio_vector(vector, dia_consulta=10) == 1

    def test_vector_vacio(self):
        assert determinar_inicio_vector([], dia_consulta=25) == 0


# ===========================================================================
# 8.1.2 — Tabla de decisiones
# ===========================================================================


class TestTablaDecisiones:
    def test_si_si_si_promedio_3_meses(self):
        """Fila 1: SI SI SI → promedio últimos 3 meses."""
        vector = _vector_desde_flags([
            (True, 3_000_000),
            (True, 2_000_000),
            (True, 1_000_000),
        ])
        ingreso, decision = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == 2_000_000
        assert "Promedio" in decision

    def test_si_no_si_con_5_pagos_en_6(self):
        """Fila 2: SI NO SI con ≥5 pagos en 6 → promedio de 2 con ingreso."""
        vector = _vector_desde_flags([
            (True, 3_000_000),   # -1 SI
            (False, 0),          # -2 NO
            (True, 1_000_000),   # -3 SI
            (True, 2_000_000),   # -4 SI
            (True, 2_000_000),   # -5 SI
            (True, 2_000_000),   # -6 SI → 5 pagos en 6
        ])
        ingreso, _ = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == 2_000_000  # (3M + 1M) / 2

    def test_si_no_si_con_menos_de_5_pagos_en_6(self):
        """Fila 2: SI NO SI con <5 pagos en 6 → promedio 3 con NO=0."""
        vector = _vector_desde_flags([
            (True, 3_000_000),   # -1 SI
            (False, 0),          # -2 NO
            (True, 1_500_000),   # -3 SI
            (False, 0),          # -4 NO
            (False, 0),          # -5 NO
            (True, 2_000_000),   # -6 SI → 3 pagos en 6
        ])
        ingreso, _ = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == pytest.approx(1_500_000)  # (3M + 0 + 1.5M) / 3

    def test_no_si_si_con_5_pagos_en_6(self):
        """Fila 3: NO SI SI con ≥5 pagos en 6 → promedio de 2 con ingreso."""
        vector = _vector_desde_flags([
            (True, 2_000_000),   # -1 SI
            (True, 2_000_000),   # -2 SI
            (False, 0),          # -3 NO
            (True, 2_000_000),   # -4
            (True, 2_000_000),   # -5
            (True, 2_000_000),   # -6 → 5 pagos en 6
        ])
        ingreso, _ = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == 2_000_000

    def test_no_no_si_con_8_pagos_en_12(self):
        """Fila 4: NO NO SI con ≥8 en 12 → último ingreso."""
        pagos = [(True, 2_500_000)]  # mes -1 SI
        pagos += [(False, 0), (False, 0)]  # mes -2, -3 NO
        pagos += [(True, 2_000_000)] * 9  # 9 meses más con pago
        vector = _vector_desde_flags(pagos)
        ingreso, _ = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == 2_500_000  # último ingreso

    def test_no_no_si_con_menos_de_8_pagos_en_12(self):
        """Fila 4: NO NO SI con <8 en 12 → promedio 3 con NO=0."""
        pagos = [(True, 3_000_000)]  # -1 SI
        pagos += [(False, 0)] * 11  # -2 a -12 NO
        vector = _vector_desde_flags(pagos)
        ingreso, _ = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == 1_000_000  # (3M + 0 + 0) / 3

    def test_si_si_no_ingreso_cero(self):
        """Fila 5: mes más reciente sin pago → ingreso 0."""
        vector = _vector_desde_flags([
            (False, 0),          # -1 NO
            (True, 2_000_000),   # -2 SI
            (True, 2_000_000),   # -3 SI
        ])
        ingreso, _ = aplicar_tabla_decisiones(vector, inicio=0)
        assert ingreso == 0.0


# ===========================================================================
# 8.1.4 — Consolidación de múltiples empleadores
# ===========================================================================


class TestConsolidarVector:
    def test_un_empleador_normal(self):
        pagos = _hacer_pagos([
            (2026, 3, True, 2_000_000),
            (2026, 2, True, 2_000_000),
        ])
        aportante = _hacer_aportante(pagos=pagos)
        vector, obs, bloqueado = consolidar_vector([aportante], "102449000")
        assert not bloqueado
        assert len(vector) == 2
        assert vector[0].ingresos == 2_000_000

    def test_independiente_cedula_igual_nit(self):
        pagos = _hacer_pagos([(2026, 3, True, 5_000_000)])
        aportante = _hacer_aportante(nit="102449000", pagos=pagos)
        vector, obs, bloqueado = consolidar_vector([aportante], "102449000")
        assert bloqueado
        assert any("independiente" in o for o in obs)

    def test_licencia_no_remunerada_bloquea(self):
        pagos = _hacer_pagos([(2026, 3, True, 2_000_000)])
        aportante = _hacer_aportante(pagos=pagos, licencia=True)
        vector, obs, bloqueado = consolidar_vector([aportante], "102449000")
        assert bloqueado

    def test_retiro_unico_empleador_bloquea(self):
        pagos = _hacer_pagos([(2026, 3, True, 2_000_000)])
        aportante = _hacer_aportante(pagos=pagos, retiro=True)
        vector, obs, bloqueado = consolidar_vector([aportante], "102449000")
        assert bloqueado

    def test_retiro_un_empleador_con_otros_ignora_reciente(self):
        pagos_a = _hacer_pagos([
            (2026, 3, True, 1_000_000),
            (2026, 2, True, 1_000_000),
        ])
        pagos_b = _hacer_pagos([
            (2026, 3, True, 2_000_000),
            (2026, 2, True, 2_000_000),
        ])
        ap_retiro = _hacer_aportante(nit="900111111", pagos=pagos_a, retiro=True)
        ap_activo = _hacer_aportante(nit="900222222", pagos=pagos_b)

        vector, obs, bloqueado = consolidar_vector(
            [ap_retiro, ap_activo], "102449000"
        )
        assert not bloqueado
        # Mes 2026-03: solo ap_activo (2M), ap_retiro ignorado
        # Mes 2026-02: ap_retiro (1M) + ap_activo (2M) = 3M
        assert vector[0].ingresos == 2_000_000  # marzo (sin el retirado)
        assert vector[1].ingresos == 3_000_000  # febrero (ambos)

    def test_dos_empleadores_suman_ingresos(self):
        pagos_a = _hacer_pagos([(2026, 3, True, 1_500_000)])
        pagos_b = _hacer_pagos([(2026, 3, True, 2_500_000)])
        ap_a = _hacer_aportante(nit="900111111", pagos=pagos_a)
        ap_b = _hacer_aportante(nit="900222222", pagos=pagos_b)

        vector, _, bloqueado = consolidar_vector([ap_a, ap_b], "102449000")
        assert not bloqueado
        assert vector[0].ingresos == 4_000_000

    def test_marca_inconsistencia_bloquea(self):
        pagos = _hacer_pagos([(2026, 3, True, 2_000_000)])
        aportante = _hacer_aportante(nit="900111222", pagos=pagos)
        flags = [EmpleadorFlag(nit="900111222", marca_inconsistencia=True)]
        vector, obs, bloqueado = consolidar_vector(
            [aportante], "102449000", flags
        )
        assert bloqueado
        assert any("inconsistencia" in o for o in obs)


# ===========================================================================
# 8.1.3 — Dos solicitantes
# ===========================================================================


class TestDossSolicitantes:
    def _experian_simple(self, cedula: str, ingreso: float) -> ExperianResponse:
        pagos = _hacer_pagos([
            (2026, 3, True, ingreso),
            (2026, 2, True, ingreso),
            (2026, 1, True, ingreso),
        ])
        return _hacer_experian(
            cedula=cedula,
            aportantes=[_hacer_aportante(pagos=pagos)],
        )

    def test_dos_solicitantes_aceptados(self):
        req = EvaluarIngresoRequest(
            solicitante_principal=self._experian_simple("100", 4_000_000),
            solicitante_secundario=self._experian_simple("200", 2_000_000),
            parentesco=Parentesco.CONYUGE,
            score_principal=600,
            score_secundario=600,
        )
        resp = evaluar_ingreso(req)
        assert resp.segundo_solicitante_aceptado is True
        assert resp.ingreso_total == 6_000_000

    def test_segundo_solicitante_rechazado_por_score(self):
        req = EvaluarIngresoRequest(
            solicitante_principal=self._experian_simple("100", 3_000_000),
            solicitante_secundario=self._experian_simple("200", 2_000_000),
            parentesco=Parentesco.HIJO,
            score_principal=600,
            score_secundario=300,  # menor al mínimo
        )
        resp = evaluar_ingreso(req)
        # participación 2M / 5M = 40% > 20% → requiere score mínimo
        assert resp.segundo_solicitante_aceptado is False
        assert resp.ingreso_total == 3_000_000

    def test_segundo_solicitante_baja_participacion_con_moras(self):
        req = EvaluarIngresoRequest(
            solicitante_principal=self._experian_simple("100", 8_000_000),
            solicitante_secundario=self._experian_simple("200", 1_000_000),
            parentesco=Parentesco.HERMANO,
            score_principal=600,
            score_secundario=300,
            # Justo por encima del tope de 0.5 SMLMV, sea cual sea el SMLMV vigente
            moras_actuales_secundario=0.5 * settings.SMLMV + 1,
        )
        resp = evaluar_ingreso(req)
        # participación 1M / 9M = 11% ≤ 20% → score bajo OK pero moras no
        assert resp.segundo_solicitante_aceptado is False

    def test_segundo_solicitante_baja_participacion_sin_moras(self):
        req = EvaluarIngresoRequest(
            solicitante_principal=self._experian_simple("100", 8_000_000),
            solicitante_secundario=self._experian_simple("200", 1_000_000),
            parentesco=Parentesco.HERMANO,
            score_principal=600,
            score_secundario=300,
            moras_actuales_secundario=0,
        )
        resp = evaluar_ingreso(req)
        assert resp.segundo_solicitante_aceptado is True
        assert resp.ingreso_total == 9_000_000

    def test_sin_parentesco_rechaza_segundo(self):
        req = EvaluarIngresoRequest(
            solicitante_principal=self._experian_simple("100", 4_000_000),
            solicitante_secundario=self._experian_simple("200", 2_000_000),
            parentesco=None,
            score_principal=600,
            score_secundario=600,
        )
        resp = evaluar_ingreso(req)
        assert resp.segundo_solicitante_aceptado is False


# ===========================================================================
# Integración: calcular_ingreso_solicitante con data Experian
# ===========================================================================


class TestCalcularIngresoSolicitante:
    def test_caso_sample_experian(self):
        """Reproduce el JSON de ejemplo: 11 meses de pago a $2M, 1 sin pago."""
        pagos = _hacer_pagos([
            (2026, 3, True, 2_000_000),
            (2026, 2, True, 2_000_000),
            (2026, 1, True, 2_000_000),
            (2025, 12, True, 2_000_000),
            (2025, 11, True, 2_000_000),
            (2025, 10, True, 2_000_000),
            (2025, 9, True, 2_000_000),
            (2025, 8, True, 2_000_000),
            (2025, 7, True, 2_000_000),
            (2025, 6, True, 2_000_000),
            (2025, 5, True, 2_000_000),
            (2025, 4, False, 0),
        ])
        experian = _hacer_experian(
            aportantes=[_hacer_aportante(pagos=pagos)],
            fecha="04/23/2026 04:58:50 PM",
        )
        detalle = calcular_ingreso_solicitante(experian)
        assert detalle.ingreso_calculado == 2_000_000
        assert "Promedio" in detalle.decision_aplicada
