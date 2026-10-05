import pytest
from app.models.hdc import LineaCredito, ObligacionCredito
from app.services.gastos import (
    _pmt,
    _tasa_mensual,
    _nivel_riesgo,
    _buscar_pct,
    _meses_entre_fechas,
    calcular_cuota_obligacion,
    calcular_cuotas_centrales,
    _TABLA_PCT_SALDO,
    _TABLA_PCT_CONTINGENTE,
)

_ACCOUNT_TYPES = {
    LineaCredito.TDC: 2,
    LineaCredito.ROT: 3,
    LineaCredito.CAB: 10,
    LineaCredito.VIV: 13,
    LineaCredito.SOSTENIMIENTO: 23,
}


def _ob(**kwargs) -> ObligacionCredito:
    linea = kwargs.get("linea_credito", LineaCredito.CAB)
    defaults = dict(
        entidad_nit="",
        entidad_nombre="Test",
        linea_credito=linea,
        account_type=_ACCOUNT_TYPES.get(linea, 10),
        sub_account_type="00",
    )
    defaults.update(kwargs)
    return ObligacionCredito(**defaults)


class TestPMT:
    def test_tdc_saldo(self):
        tasa_m = _tasa_mensual(0.20)
        cuota = _pmt(tasa_m, 36, 12_330_000)
        assert abs(cuota - 448_059) < 1

    def test_rot_saldo(self):
        tasa_m = _tasa_mensual(0.25)
        cuota = _pmt(tasa_m, 60, 1_000_000)
        assert abs(cuota - 27_917) < 1

    def test_cab_plazo_total(self):
        tasa_m = _tasa_mensual(0.125)
        cuota = _pmt(tasa_m, 72.66, 15_000_000)
        assert abs(cuota - 290_160) < 100

    def test_viv_plazo_total(self):
        tasa_m = _tasa_mensual(0.11)
        cuota = _pmt(tasa_m, 120.07, 200_000_000)
        assert abs(cuota - 2_695_792) < 500

    def test_zero_values(self):
        assert _pmt(0.015, 36, 0) == 0
        assert _pmt(0.015, 0, 100_000) == 0
        assert _pmt(0, 36, 100_000) == 0


class TestNivelRiesgo:
    def test_riesgo_1(self):
        assert _nivel_riesgo(900) == 1
        assert _nivel_riesgo(895) == 1

    def test_riesgo_3(self):
        assert _nivel_riesgo(820) == 3

    def test_riesgo_5(self):
        assert _nivel_riesgo(750) == 5
        assert _nivel_riesgo(740) == 5

    def test_riesgo_6(self):
        assert _nivel_riesgo(530) == 6
        assert _nivel_riesgo(620) == 6
        assert _nivel_riesgo(None) == 6


class TestBuscarPct:
    def test_saldo_cero(self):
        assert _buscar_pct(_TABLA_PCT_SALDO, 0, 5) == 0

    def test_saldo_rango_0_3(self):
        assert _buscar_pct(_TABLA_PCT_SALDO, 1, 3) == 0.25

    def test_saldo_rango_6_9(self):
        assert _buscar_pct(_TABLA_PCT_SALDO, 8.78, 5) == 0.70

    def test_saldo_mayor_12(self):
        assert _buscar_pct(_TABLA_PCT_SALDO, 15, 6) == 1.00

    def test_contingente_cero(self):
        assert _buscar_pct(_TABLA_PCT_CONTINGENTE, 0, 3) == 0.10

    def test_contingente_rango_0_3(self):
        assert _buscar_pct(_TABLA_PCT_CONTINGENTE, 1, 3) == 0.15


class TestMesesEntreFechas:
    def test_plazo_cab(self):
        meses = _meses_entre_fechas("2024-07-30", "2030-08-18")
        assert abs(meses - 72.66) < 0.1

    def test_meses_faltantes(self):
        meses = _meses_entre_fechas("2025-02-28", "2030-08-18")
        assert abs(meses - 65.65) < 0.1

    def test_caso_proximo_vencer(self):
        meses = _meses_entre_fechas("2025-02-28", "2025-03-15")
        assert meses is not None
        assert meses < 2

    def test_none_dates(self):
        assert _meses_entre_fechas(None, "2030-08-18") is None
        assert _meses_entre_fechas("2025-02-28", None) is None


# =====================================================================
# TDC: ejemplos del Excel hoja "TDC Y ROT"
# =====================================================================

class TestTDC:
    def test_serfinanza_score_750(self):
        """TDC row 9: saldo > cupo, score 750 (R5)."""
        ob = _ob(
            entidad_nombre="Serfinanza",
            linea_credito=LineaCredito.TDC,
            cupo=9_650_000,
            saldo=12_330_000,
            cuota_reportada=1_404_000,
            fecha_corte="2025-02-28",
        )
        d = calcular_cuota_obligacion(ob, score=750)

        assert d.meses_para_pagar == pytest.approx(8.78, abs=0.01)
        assert d.porcentaje_saldo == 0.70
        assert d.cuota_por_saldo == pytest.approx(982_800, abs=1)
        assert d.cupo_contingente == 0
        assert d.cuota_por_contingente == 0
        assert d.cuota_final == pytest.approx(982_800, abs=1)

    def test_bbva_score_820_con_saldo(self):
        """TDC row 10: score 820 (R3), saldo bajo, cupo contingente."""
        ob = _ob(
            entidad_nombre="BBVA",
            linea_credito=LineaCredito.TDC,
            cupo=4_900_000,
            saldo=1_100_000,
            cuota_reportada=1_100_000,
            fecha_corte="2025-02-28",
        )
        d = calcular_cuota_obligacion(ob, score=820)

        assert d.meses_para_pagar == pytest.approx(1, abs=0.01)
        assert d.porcentaje_saldo == 0.25
        assert d.cuota_por_saldo == pytest.approx(275_000, abs=1)
        assert d.cupo_contingente == pytest.approx(3_800_000, abs=1)
        assert d.porcentaje_contingente == 0.15
        assert d.cuota_por_contingente == pytest.approx(20_713, abs=5)
        assert d.cuota_final == pytest.approx(295_713, abs=10)

    def test_bbva_score_530_sin_saldo(self):
        """TDC row 11: saldo 0, score 530 (R6), solo contingente."""
        ob = _ob(
            entidad_nombre="BBVA",
            linea_credito=LineaCredito.TDC,
            cupo=4_900_000,
            saldo=0,
            cuota_reportada=0,
            fecha_corte="2025-02-28",
        )
        d = calcular_cuota_obligacion(ob, score=530)

        assert d.meses_para_pagar == 0
        assert d.porcentaje_saldo == 0
        assert d.cuota_por_saldo == 0
        assert d.cupo_contingente == pytest.approx(4_900_000, abs=1)
        assert d.porcentaje_contingente == 0.25
        assert d.cuota_por_contingente == pytest.approx(44_515, abs=5)
        assert d.cuota_final == pytest.approx(44_515, abs=5)


# =====================================================================
# ROT: ejemplos del Excel hoja "TDC Y ROT"
# =====================================================================

class TestROT:
    def test_bancolombia_score_740(self):
        """ROT row 16: score 740 (R5)."""
        ob = _ob(
            entidad_nombre="Bancolombia",
            linea_credito=LineaCredito.ROT,
            cupo=10_500_000,
            saldo=1_000_000,
            cuota_reportada=1_000_000,
            fecha_corte="2025-02-28",
        )
        d = calcular_cuota_obligacion(ob, score=740)

        assert d.meses_para_pagar == pytest.approx(1, abs=0.01)
        assert d.porcentaje_saldo == 0.35
        assert d.cuota_por_saldo == pytest.approx(350_000, abs=1)
        assert d.cupo_contingente == pytest.approx(9_500_000, abs=1)
        assert d.porcentaje_contingente == 0.25
        assert d.cuota_por_contingente == pytest.approx(66_303, abs=10)
        assert d.cuota_final == pytest.approx(416_303, abs=15)

    def test_banco_bogota_score_620_alto_uso(self):
        """ROT row 18: score 620 (R6), > 12 meses para pagar."""
        ob = _ob(
            entidad_nombre="Banco Bogotá",
            linea_credito=LineaCredito.ROT,
            cupo=50_000_000,
            saldo=15_000_000,
            cuota_reportada=1_000_000,
            fecha_corte="2025-02-28",
        )
        d = calcular_cuota_obligacion(ob, score=620)

        assert d.meses_para_pagar == pytest.approx(15, abs=0.01)
        assert d.porcentaje_saldo == 1.0
        assert d.cuota_por_saldo == pytest.approx(1_000_000, abs=1)
        assert d.cupo_contingente == pytest.approx(35_000_000, abs=1)
        assert d.porcentaje_contingente == 1.0
        assert d.cuota_por_contingente == pytest.approx(977_101, abs=50)
        assert d.cuota_final == pytest.approx(1_977_101, abs=100)


# =====================================================================
# CAB: ejemplos del Excel hoja "CONS-VIV"
# =====================================================================

class TestCAB:
    def test_banco_popular_principal(self):
        """CAB row 9: cuota reportada > calculada, se toma reportada."""
        ob = _ob(
            entidad_nombre="Banco Popular",
            linea_credito=LineaCredito.CAB,
            cupo=15_000_000,
            saldo=8_000_000,
            cuota_reportada=310_000,
            fecha_apertura="2024-07-30",
            fecha_vencimiento="2030-08-18",
            fecha_corte="2025-02-28",
            calidad_deudor="00",
            periodicidad=1,
        )
        d = calcular_cuota_obligacion(ob, score=900)

        assert d.cuota_anualidad == pytest.approx(290_160, abs=200)
        assert d.cuota_calculada == pytest.approx(310_000, abs=1)
        assert d.cuota_final == pytest.approx(310_000, abs=1)
        assert d.excluida_por_cuotas is False

    def test_coop_unimos_proximo_vencer(self):
        """CAB row 10: meses faltantes < 2, excluida."""
        ob = _ob(
            entidad_nombre="Coop. Unimos",
            linea_credito=LineaCredito.CAB,
            cupo=120_000_000,
            saldo=2_400_000,
            cuota_reportada=2_400_000,
            fecha_apertura="2020-03-05",
            fecha_vencimiento="2025-03-15",
            fecha_corte="2025-02-28",
            calidad_deudor="00",
            periodicidad=1,
        )
        d = calcular_cuota_obligacion(ob, score=780)

        assert d.meses_faltantes is not None
        assert d.meses_faltantes < 2
        assert d.excluida_por_cuotas is True
        assert d.cuota_final == 0

    def test_muebles_jamar_codeudor(self):
        """CAB row 11: codeudor → 25% de la cuota."""
        ob = _ob(
            entidad_nombre="Muebles Jamar",
            linea_credito=LineaCredito.CAB,
            cupo=3_000_000,
            saldo=500_000,
            cuota_reportada=70_000,
            fecha_apertura="2023-09-14",
            fecha_vencimiento="2029-09-14",
            fecha_corte="2025-02-28",
            calidad_deudor="01",
            periodicidad=1,
        )
        d = calcular_cuota_obligacion(ob, score=520)

        assert d.porcentaje_calidad == 0.25
        assert d.cuota_final == pytest.approx(17_500, abs=10)


# =====================================================================
# VIV: ejemplos del Excel hoja "CONS-VIV"
# =====================================================================

class TestVIV:
    def test_davivienda_principal(self):
        """VIV row 16: deudor principal, cuota reportada > calculada."""
        ob = _ob(
            entidad_nombre="Davivienda",
            linea_credito=LineaCredito.VIV,
            cupo=200_000_000,
            saldo=180_000_000,
            cuota_reportada=3_100_000,
            fecha_apertura="2024-07-30",
            fecha_vencimiento="2034-07-30",
            fecha_corte="2025-02-28",
            calidad_deudor="00",
            periodicidad=1,
        )
        d = calcular_cuota_obligacion(ob, score=999)

        assert d.cuota_anualidad == pytest.approx(2_695_792, abs=500)
        assert d.cuota_calculada == pytest.approx(3_100_000, abs=1)
        assert d.cuota_final == pytest.approx(3_100_000, abs=1)

    def test_avvillas_codeudor_viv(self):
        """VIV row 18: codeudor VIV → 50%."""
        ob = _ob(
            entidad_nombre="AVVillas",
            linea_credito=LineaCredito.VIV,
            cupo=50_000_000,
            saldo=10_000_000,
            cuota_reportada=500_000,
            fecha_apertura="2023-09-14",
            fecha_vencimiento="2043-09-14",
            fecha_corte="2025-02-28",
            calidad_deudor="01",
            periodicidad=1,
        )
        d = calcular_cuota_obligacion(ob, score=700)

        assert d.porcentaje_calidad == 0.50
        assert d.cuota_final == pytest.approx(250_000, abs=100)


class TestSostenimiento:
    def test_cuota_cero(self):
        ob = _ob(
            entidad_nombre="Claro",
            linea_credito=LineaCredito.SOSTENIMIENTO,
            cupo=500_000,
            saldo=200_000,
            cuota_reportada=50_000,
        )
        d = calcular_cuota_obligacion(ob, score=800)
        assert d.cuota_final == 0


# =====================================================================
# Ejemplo_A del Excel: cliente Pedro Perez, score 750
# =====================================================================

class TestEjemploA:
    def _obligaciones_pedro(self):
        return [
            _ob(
                entidad_nombre="Serfinanza",
                linea_credito=LineaCredito.TDC,
                cupo=9_650_000,
                saldo=12_330_000,
                cuota_reportada=1_404_000,
                fecha_corte="2025-02-28",
            ),
            _ob(
                entidad_nombre="BBVA",
                linea_credito=LineaCredito.TDC,
                cupo=4_900_000,
                saldo=1_100_000,
                cuota_reportada=1_100_000,
                fecha_corte="2025-02-28",
            ),
            _ob(
                entidad_nombre="BBVA",
                linea_credito=LineaCredito.CAB,
                cupo=26_693_000,
                saldo=25_687_000,
                cuota_reportada=639_000,
                fecha_apertura="2024-07-30",
                fecha_vencimiento="2030-08-18",
                fecha_corte="2025-02-28",
                calidad_deudor="00",
                periodicidad=1,
            ),
            _ob(
                entidad_nombre="Muebles Jamar",
                linea_credito=LineaCredito.CAB,
                cupo=6_449_000,
                saldo=6_270_000,
                cuota_reportada=179_000,
                fecha_apertura="2023-09-14",
                fecha_vencimiento="2029-09-14",
                fecha_corte="2025-02-28",
                calidad_deudor="00",
                periodicidad=1,
            ),
        ]

    def test_total_cuotas_pedro(self):
        """Ejemplo_A con score 750 → R5. El Excel usa R6 por error;
        los tests individuales (hoja TDC Y ROT) confirman R5."""
        obs = self._obligaciones_pedro()
        detalles, total = calcular_cuotas_centrales(obs, score=750)

        assert len(detalles) == 4
        assert total == pytest.approx(2_220_322, abs=200)


class TestParametrosPolitica:
    """Los cuadros que se muestran en la hoja de Capacidad de Pago deben
    coincidir con las tablas que usa el motor."""

    def test_parametros_reflejan_tablas_del_motor(self):
        from app.services.gastos import (
            parametros_politica, _TABLA_GASTOS_BASICOS, _TASA_EA_TDC, _PLAZO_TDC,
        )
        P = parametros_politica()
        assert P["gastos_basicos"]["tabla"] == [f for _, f in _TABLA_GASTOS_BASICOS]
        assert len(P["gastos_basicos"]["rangos_smlmv"]) == len(_TABLA_GASTOS_BASICOS)
        assert P["cuotas_centrales"]["pct_saldo"] == _TABLA_PCT_SALDO
        assert P["cuotas_centrales"]["pct_contingente"] == _TABLA_PCT_CONTINGENTE
        assert len(P["cuotas_centrales"]["rangos_meses"]) == len(_TABLA_PCT_SALDO)
        tdc = next(l for l in P["cuotas_centrales"]["lineas"] if l["linea"] == "TDC")
        assert tdc["tasa_ea"] == _TASA_EA_TDC and tdc["plazo_meses"] == _PLAZO_TDC
        assert [n["nivel"] for n in P["niveles_riesgo"]] == [1, 2, 3, 4, 5, 6]

    def test_fila_gastos_basicos_coincide_con_calculo(self):
        from app.config import settings
        from app.services.gastos import (
            _fila_gastos_basicos, _TABLA_GASTOS_BASICOS, calcular_gastos_basicos,
        )
        for smlmv, fila in [(20, 0), (12, 1), (9, 2), (5, 3), (3, 4), (1.5, 5), (1, 5), (0.5, 6)]:
            assert _fila_gastos_basicos(smlmv) == fila
            pct, _ = calcular_gastos_basicos(smlmv * settings.SMLMV, 760)  # R4
            assert pct == _TABLA_GASTOS_BASICOS[fila][1][3]

    def test_fila_meses_coincide_con_buscar_pct(self):
        from app.services.gastos import _fila_meses
        for meses, fila in [(0, 0), (2, 1), (3, 1), (4.5, 2), (8, 3), (12, 4), (13, 5)]:
            assert _fila_meses(meses) == fila
            assert _buscar_pct(_TABLA_PCT_SALDO, meses, 2) == _TABLA_PCT_SALDO[fila][1]

    def test_detalle_incluye_fila_usada(self):
        det = calcular_cuota_obligacion(
            _ob(linea_credito=LineaCredito.TDC, cupo=10_000_000, saldo=4_000_000,
                cuota_reportada=300_000, calidad_deudor="00"),
            score=760,
        )
        assert det.fila_tabla_meses == 5
        assert det.porcentaje_saldo == _TABLA_PCT_SALDO[5][3]

    def test_endpoint_parametros(self):
        from fastapi.testclient import TestClient
        from app.main import app
        r = TestClient(app).get("/filtro/parametros")
        assert r.status_code == 200
        assert "gastos_basicos" in r.json() and "cuotas_centrales" in r.json()


# =====================================================================
# Ingreso Neto Calculado = ingreso bruto - retención en la fuente
# - fondo de solidaridad - gastos básicos (porcentaje buscado con el bruto
# y aplicado al bruto). Retención y solidaridad llegan del Análisis de
# Ingresos y no se recalculan.
# =====================================================================

class TestIngresoNetoCalculado:
    BRUTO = 20_000_000

    def test_formula_con_descuentos_del_analisis_de_ingresos(self):
        from app.services.gastos import analizar_gastos, calcular_gastos_basicos

        r = analizar_gastos(
            self.BRUTO, 800, [],
            retefuente_principal=1_500_000, solidaridad_principal=200_000,
        )
        p = r.solicitante_principal
        pct, gastos = calcular_gastos_basicos(self.BRUTO, 800)

        assert p.descuentos_del_analisis_ingresos is True
        assert p.retefuente == 1_500_000 and p.solidaridad == 200_000
        assert p.porcentaje_gastos_basicos == pct
        assert p.gastos_basicos == pytest.approx(pct * self.BRUTO)
        assert p.ingreso_neto_calculado == pytest.approx(
            self.BRUTO - 1_500_000 - 200_000 - gastos
        )
        assert r.total_ingreso_neto_calculado == p.ingreso_neto_calculado
        # Sin obligaciones, el neto de 8.8 es el mismo Ingreso Neto Calculado
        assert r.ingreso_neto == pytest.approx(p.ingreso_neto_calculado)
        assert r.disponible_pago == pytest.approx(r.ingreso_neto * r.factor_ajuste)

    def test_descuentos_en_cero_del_analisis_no_se_recalculan(self):
        """Un cero explícito del Análisis de Ingresos se respeta: no se va a
        las tablas de la política."""
        from app.services.gastos import analizar_gastos

        p = analizar_gastos(
            self.BRUTO, 800, [], retefuente_principal=0, solidaridad_principal=0,
        ).solicitante_principal
        assert p.descuentos_del_analisis_ingresos is True
        assert p.total_descuentos_nomina == 0
        assert p.ingreso_neto_calculado == pytest.approx(self.BRUTO - p.gastos_basicos)

    def test_sin_descuentos_previos_se_usan_las_tablas(self):
        from app.services.gastos import analizar_gastos

        p = analizar_gastos(self.BRUTO, 800, []).solicitante_principal
        assert p.descuentos_del_analisis_ingresos is False
        assert p.retefuente > 0 and p.solidaridad > 0
        assert p.ingreso_neto_calculado == pytest.approx(
            self.BRUTO - p.retefuente - p.solidaridad - p.gastos_basicos
        )

    def test_porcentaje_se_busca_y_se_aplica_con_el_bruto(self):
        """Bruto de 4.004 SMLMV: la fila de la tabla es "> 4 a 8" aunque el
        ingreso después de descuentos quede por debajo de 4 SMLMV."""
        from app.config import settings
        from app.services.gastos import analizar_gastos, calcular_gastos_basicos

        bruto = 4.004 * settings.SMLMV
        solidaridad = 0.01 * bruto
        p = analizar_gastos(
            bruto, 870, [], retefuente_principal=0, solidaridad_principal=solidaridad,
        ).solicitante_principal
        pct_bruto, gastos_bruto = calcular_gastos_basicos(bruto, 870)
        pct_despues, _ = calcular_gastos_basicos(bruto - solidaridad, 870)

        assert pct_bruto != pct_despues          # el caso distingue las dos bases
        assert p.porcentaje_gastos_basicos == pct_bruto
        assert p.gastos_basicos == pytest.approx(gastos_bruto, abs=0.01)
        assert p.ingreso_neto_calculado == pytest.approx(
            bruto - solidaridad - gastos_bruto, abs=0.01
        )

    def test_dos_solicitantes_y_cuotas(self):
        from app.services.gastos import analizar_gastos

        ob = _ob(
            linea_credito=LineaCredito.CAB, cupo=10_000_000, saldo=8_000_000,
            cuota_reportada=400_000, fecha_apertura="2024-01-01",
            fecha_vencimiento="2029-01-01", fecha_corte="2026-09-30",
            calidad_deudor="00", periodicidad=1,
        )
        r = analizar_gastos(
            8_000_000, 800, [ob],
            ingreso_bruto_secundario=3_000_000, score_secundario=720,
            obligaciones_secundario=[],
            retefuente_principal=100_000, solidaridad_principal=80_000,
            retefuente_secundario=0, solidaridad_secundario=0,
        )
        p, s = r.solicitante_principal, r.solicitante_secundario
        assert r.total_ingreso_bruto == 11_000_000
        assert r.total_ingreso_neto_calculado == pytest.approx(
            p.ingreso_neto_calculado + s.ingreso_neto_calculado
        )
        # 8.8 = Ingreso Neto Calculado total - cuotas en centrales
        assert r.ingreso_neto == pytest.approx(
            r.total_ingreso_neto_calculado - p.total_cuotas_centrales - s.total_cuotas_centrales,
            abs=0.05,
        )
        assert p.total_cuotas_centrales > 0

    def test_endpoint_exige_ingreso_bruto(self):
        from fastapi.testclient import TestClient
        from app.main import app

        r = TestClient(app).post(
            "/filtro/capacidad-pago",
            json={"cedula": "1", "primer_apellido": "X"},
        )
        assert r.status_code == 422
        assert "ingreso_bruto" in str(r.json()["detail"])
