from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.models.solicitud import IngresoArriendoInput, DetalleIngresoArriendo
from app.services.otros_ingresos import (
    calcular_ingreso_arriendo,
    calcular_ingresos_arriendos,
)


HOY = date(2026, 4, 24)
HACE_10_DIAS = (HOY - timedelta(days=10)).strftime("%Y-%m-%d")
HACE_40_DIAS = (HOY - timedelta(days=40)).strftime("%Y-%m-%d")


def _arriendo(
    fecha_emision: str = HACE_10_DIAS,
    propietario: str = "1024490001",
    declarado: float = 1_200_000,
    sim_arriendo: float | None = 1_300_000,
    sim_inmueble: float | None = None,
    meses: int = 6,
) -> IngresoArriendoInput:
    return IngresoArriendoInput(
        pin_certificado="ABC123",
        fecha_emision_certificado=fecha_emision,
        propietario_cedula=propietario,
        ingreso_arriendo_declarado=declarado,
        valor_arriendo_simulador=sim_arriendo,
        valor_inmueble_simulador=sim_inmueble,
        meses_contrato=meses,
    )


CEDULA = "1024490001"


# ===========================================================================
# Validaciones de rechazo
# ===========================================================================


class TestValidaciones:
    def test_certificado_vencido(self):
        arr = _arriendo(fecha_emision=HACE_40_DIAS)
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 0.0
        assert any("vencido" in v for v in det.validaciones)

    def test_certificado_fecha_futura(self):
        futuro = (HOY + timedelta(days=5)).strftime("%Y-%m-%d")
        arr = _arriendo(fecha_emision=futuro)
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 0.0
        assert any("futura" in v for v in det.validaciones)

    def test_certificado_fecha_invalida(self):
        arr = _arriendo(fecha_emision="no-es-fecha")
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 0.0
        assert any("inválido" in v for v in det.validaciones)

    def test_propietario_no_coincide(self):
        arr = _arriendo(propietario="999999999")
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 0.0
        assert any("no coincide" in v for v in det.validaciones)

    def test_contrato_menos_de_4_meses(self):
        arr = _arriendo(meses=3)
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 0.0
        assert any("meses" in v and "mínimo" in v for v in det.validaciones)

    def test_sin_valor_referencia(self):
        arr = _arriendo(sim_arriendo=None, sim_inmueble=None)
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 0.0
        assert any("referencia" in v for v in det.validaciones)


# ===========================================================================
# Cálculo del ingreso
# ===========================================================================


class TestCalculoIngreso:
    def test_declarado_menor_que_simulador_usa_declarado(self):
        arr = _arriendo(declarado=1_000_000, sim_arriendo=1_500_000)
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 1_000_000

    def test_declarado_mayor_que_simulador_usa_simulador(self):
        arr = _arriendo(declarado=2_000_000, sim_arriendo=1_200_000)
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 1_200_000
        assert any("supera" in o for o in det.observaciones)

    def test_referencia_por_valor_inmueble(self):
        """0.55% de $300M = $1,650,000."""
        arr = _arriendo(
            declarado=2_000_000,
            sim_arriendo=None,
            sim_inmueble=300_000_000,
        )
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 1_650_000
        assert "0.55%" in det.metodo_referencia

    def test_ambos_simuladores_usa_menor(self):
        """Con ambos: usa el menor entre simulador de arriendo y 0.55% inmueble."""
        arr = _arriendo(
            declarado=5_000_000,
            sim_arriendo=2_000_000,
            sim_inmueble=300_000_000,  # 0.55% = 1,650,000
        )
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 1_650_000  # min(2M, 1.65M)

    def test_caso_aprobado_completo(self):
        arr = _arriendo()
        det = calcular_ingreso_arriendo(arr, CEDULA, HOY)
        assert det.ingreso_aceptado == 1_200_000
        assert any("aprobado" in v for v in det.validaciones)


# ===========================================================================
# Múltiples arriendos
# ===========================================================================


class TestMultiplesArriendos:
    def test_suma_arriendos_aprobados(self):
        arriendos = [
            _arriendo(declarado=1_000_000, sim_arriendo=1_500_000),
            _arriendo(declarado=800_000, sim_arriendo=900_000),
        ]
        total, detalles = calcular_ingresos_arriendos(arriendos, CEDULA, HOY)
        assert total == 1_800_000
        assert len(detalles) == 2

    def test_uno_aprobado_uno_rechazado(self):
        arriendos = [
            _arriendo(declarado=1_000_000, sim_arriendo=1_500_000),
            _arriendo(meses=2),  # rechazado por contrato corto
        ]
        total, detalles = calcular_ingresos_arriendos(arriendos, CEDULA, HOY)
        assert total == 1_000_000
        assert detalles[0].ingreso_aceptado == 1_000_000
        assert detalles[1].ingreso_aceptado == 0.0

    def test_lista_vacia(self):
        total, detalles = calcular_ingresos_arriendos([], CEDULA, HOY)
        assert total == 0.0
        assert detalles == []
