"""Pruebas del parseo de la respuesta Experian HDC+ (estructura real UAT).

El fixture `tests/fixtures/hdc_plus_sample.json` se construyó a partir de
respuestas reales del ambiente UAT, anonimizadas: contiene una cuenta de
ahorro, una TDC vigente, un CAB vigente, un CAB cerrado (pago total), un
crédito como codeudor, un crédito de vivienda como cotitular cerrado, un
crédito en mora y una cuenta sin bloque `values`.
"""
import json
from pathlib import Path

import pytest

from app.models.hdc import (
    HDCplusResponse,
    LineaCredito,
    ResultadoHDC,
    ScoreExperian,
)
from app.services.experian_hdc import _procesar_respuesta
from app.services.gastos import analizar_gastos

FIXTURE = Path(__file__).parent / "fixtures" / "hdc_plus_sample.json"


@pytest.fixture(scope="module")
def raw() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def resultado(raw) -> ResultadoHDC:
    return _procesar_respuesta(raw, "1000000001")


class TestModeloTolerante:
    def test_valida_estructura_real(self, raw):
        hdc = HDCplusResponse.model_validate(raw)
        rep = hdc.ReportHDCplus
        assert len(rep.savings) == 1
        assert len(rep.liabilities) == 6
        assert len(rep.creditCard) == 1

    def test_account_type_string_se_normaliza_a_int(self, raw):
        rep = HDCplusResponse.model_validate(raw).ReportHDCplus
        assert rep.creditCard[0].account.accountType == 2  # venía "02"
        assert rep.liabilities[0].account.accountType == 5  # venía "05"

    def test_features_credit_card_con_mayuscula(self, raw):
        rep = HDCplusResponse.model_validate(raw).ReportHDCplus
        tdc = rep.creditCard[0]
        assert tdc.featuresCreditCard is not None
        assert tdc.caracteristicas.typeOfDebtor == "00"

    def test_type_of_debtor_numerico_se_normaliza(self, raw):
        rep = HDCplusResponse.model_validate(raw).ReportHDCplus
        cotit = rep.liabilities[3]
        assert cotit.caracteristicas.typeOfDebtor == "96"

    def test_secciones_ausentes_no_rompen(self, raw):
        sin_tdc = json.loads(json.dumps(raw))
        del sin_tdc["ReportHDCplus"]["creditCard"]
        rep = HDCplusResponse.model_validate(sin_tdc).ReportHDCplus
        assert rep.creditCard == []


class TestProcesarRespuesta:
    def test_datos_generales(self, resultado):
        assert resultado.codigo_respuesta == 13
        assert resultado.nombre_completo == "JUAN PRUEBA DEMO"
        assert resultado.huellas_consulta == 3

    def test_score_modelo_df(self, resultado):
        assert resultado.scores == [
            ScoreExperian(model_code="DF", score_value=658, model_date="2026-09-27")
        ]
        assert resultado.score_advance == 658

    def test_score_cero_es_sin_score(self):
        r = ResultadoHDC(cedula="x", scores=[ScoreExperian(model_code="DF", score_value=0)])
        assert r.score_advance is None

    def test_score_prefiere_z0(self):
        r = ResultadoHDC(cedula="x", scores=[
            ScoreExperian(model_code="DF", score_value=600),
            ScoreExperian(model_code="Z0", score_value=720),
        ])
        assert r.score_advance == 720

    def test_savings_no_es_obligacion(self, resultado):
        assert all(ob.account_type != 51 for ob in resultado.obligaciones)

    def test_solo_vigentes_y_conteo_cerradas(self, resultado):
        # Vigentes: CAB, codeudor EDU, mora CON, TDC. Cerradas: APD 03, CAV 03, CEL 03.
        assert len(resultado.obligaciones) == 4
        assert resultado.obligaciones_cerradas == 3
        assert all(ob.vigente for ob in resultado.obligaciones)

    def test_tdc_valores_desde_values(self, resultado):
        tdc = next(ob for ob in resultado.obligaciones if ob.linea_credito == LineaCredito.TDC)
        assert tdc.entidad_nombre == "BANCO ALFA VISA"  # businessLineCode
        assert tdc.entidad_nit == "903938"
        assert tdc.cupo == 2_700_000
        assert tdc.saldo == 2_576_000
        assert tdc.cuota_reportada == 903_000
        assert tdc.periodicidad == 1  # TDC no trae periodicidad
        assert tdc.fecha_vencimiento == "2029-07-04"
        assert tdc.fecha_corte == "2026-07-31"
        assert tdc.estado_cuenta == "01"
        assert tdc.estado_cuenta_desc == "AL DÍA"

    def test_cab_valores_y_cuotas(self, resultado):
        cab = next(ob for ob in resultado.obligaciones if ob.entidad_nombre == "BANCO ALFA")
        assert cab.linea_credito == LineaCredito.CAB
        assert cab.account_type == 5
        assert cab.cupo == 17_600_000
        assert cab.saldo == 17_761_000
        assert cab.cuota_reportada == 553_000
        assert cab.cuotas_pagadas == 0
        assert cab.total_cuotas == 60
        assert cab.cuotas_restantes == 60
        assert cab.fecha_apertura == "2026-07-21"
        assert cab.fecha_vencimiento == "2031-07-21"
        assert cab.calidad_deudor == "00"

    def test_codeudor(self, resultado):
        ob = next(ob for ob in resultado.obligaciones if ob.entidad_nombre == "BANCO GAMMA")
        assert ob.calidad_deudor == "01"
        assert ob.calidad_deudor_desc == "CODEUDOR"
        assert ob.linea_credito == LineaCredito.SOSTENIMIENTO  # 43 educación
        assert ob.cuotas_restantes == 10

    def test_mora(self, resultado):
        ob = next(ob for ob in resultado.obligaciones if ob.entidad_nombre == "FINANCIERA EPSILON")
        assert ob.estado_cuenta == "02"
        assert ob.cuotas_mora == 1
        assert ob.monto_mora == 761_000

    def test_menos_uno_se_trata_como_cero(self, raw):
        # Forzamos la cuenta cotitular (valores -1) a vigente para verificar montos
        mod = json.loads(json.dumps(raw))
        cotit = mod["ReportHDCplus"]["liabilities"][3]
        cotit["status"]["account"]["businessAccountStatus"] = "01"
        cotit["liabilitiesAccount"]["paymentType"] = 0
        res = _procesar_respuesta(mod, "x")
        ob = next(o for o in res.obligaciones if o.entidad_nombre == "COOP DELTA")
        assert ob.cupo == 0 and ob.saldo == 0 and ob.cuota_reportada == 0
        assert ob.monto_mora == 0
        assert ob.calidad_deudor == "96"
        assert ob.linea_credito == LineaCredito.VIV

    def test_codigo_no_exitoso(self, raw):
        mod = json.loads(json.dumps(raw))
        mod["ReportHDCplus"]["productResult"]["responseCode"] = 12
        mod["ReportHDCplus"]["productResult"]["responseDesc"] = "No coincide apellido"
        res = _procesar_respuesta(mod, "x")
        assert res.codigo_respuesta == 12
        assert res.obligaciones == []


class TestEndpointCapacidadPago:
    def test_endpoint_serializa_respuesta(self, raw, monkeypatch):
        from fastapi.testclient import TestClient
        from app.main import app
        import app.api.gastos as api_gastos

        async def fake_hdc(numero_documento, primer_apellido, tipo_documento="CC"):
            return _procesar_respuesta(raw, numero_documento)

        monkeypatch.setattr(api_gastos, "consultar_hdc", fake_hdc)
        client = TestClient(app)
        resp = client.post("/filtro/capacidad-pago", json={
            "cedula": "1000000001",
            "primer_apellido": "PRUEBA",
            "tipo_documento": "CC",
            "ingreso_bruto": 5_000_000,
        })
        assert resp.status_code == 200, resp.text
        data = resp.json()
        hdc = data["hdc_principal"]
        assert hdc["nombre_completo"] == "JUAN PRUEBA DEMO"
        assert hdc["obligaciones_cerradas"] == 3
        assert len(hdc["obligaciones"]) == 4
        assert hdc["obligaciones"][0]["estado_cuenta_desc"] == "AL DÍA"
        assert data["analisis"]["solicitante_principal"]["score_advance"] == 658
        assert len(data["analisis"]["solicitante_principal"]["detalle_obligaciones"]) == 4


class TestEndpointParsearHDC:
    """La Carpeta sube el JSON HDC+ y el backend lo interpreta sin ir a Experian."""

    def test_parsea_json_subido_y_devuelve_score_y_original(self, raw):
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        resp = client.post("/experian/hdc/parsear", json={"respuesta": raw})
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["cedula"] == "1000000001"  # tomada de la respuesta
        assert data["nombre_completo"] == "JUAN PRUEBA DEMO"
        assert data["score_advance"] == 658
        assert data["scores"][0]["model_code"] == "DF"
        assert data["fecha_consulta"] == "2026-09-27"
        assert data["respuesta_original"] == raw

    def test_cedula_explicita_prevalece(self, raw):
        from fastapi.testclient import TestClient
        from app.main import app

        resp = TestClient(app).post(
            "/experian/hdc/parsear", json={"respuesta": raw, "cedula": "52890002"}
        )
        assert resp.json()["cedula"] == "52890002"

    def test_json_que_no_es_hdc_da_422(self):
        from fastapi.testclient import TestClient
        from app.main import app

        resp = TestClient(app).post(
            "/experian/hdc/parsear", json={"respuesta": {"data": {"aportantes": []}}}
        )
        assert resp.status_code == 422
        assert "ReportHDCplus" in resp.json()["detail"]

    def test_codigo_no_exitoso_conserva_original(self, raw):
        from fastapi.testclient import TestClient
        from app.main import app

        mod = json.loads(json.dumps(raw))
        mod["ReportHDCplus"]["productResult"]["responseCode"] = 12
        data = TestClient(app).post(
            "/experian/hdc/parsear", json={"respuesta": mod}
        ).json()
        assert data["codigo_respuesta"] == 12
        assert data["score_advance"] is None
        assert data["respuesta_original"]["ReportHDCplus"]["productResult"]["responseCode"] == 12


class TestIntegracionGastos:
    def test_analisis_usa_obligaciones_y_score(self, resultado):
        a = analizar_gastos(
            ingreso_bruto_principal=5_000_000,
            cedula_principal=resultado.cedula,
            score_principal=resultado.score_advance,
            obligaciones_principal=resultado.obligaciones,
        )
        p = a.solicitante_principal
        assert p.score_advance == 658
        assert p.nivel_riesgo == 6
        assert len(p.detalle_obligaciones) == 4
        # La TDC y el CAB vigentes deben generar cuota > 0
        por_entidad = {d.entidad: d for d in p.detalle_obligaciones}
        assert por_entidad["BANCO ALFA VISA"].cuota_final > 0
        assert por_entidad["BANCO ALFA"].cuota_final >= 553_000
        assert por_entidad["BANCO GAMMA"].cuota_final == 0  # sostenimiento
        assert p.total_cuotas_centrales > 0

    def test_mora_vencida_cuenta_y_no_se_excluye(self, resultado):
        """FINANCIERA EPSILON: EN MORA, vencimiento 2025-09-14 ya pasado.
        Antes quedaba excluida por '≤ 2 meses faltantes'; ahora cuenta."""
        a = analizar_gastos(
            ingreso_bruto_principal=5_000_000,
            score_principal=resultado.score_advance,
            obligaciones_principal=resultado.obligaciones,
        )
        p = a.solicitante_principal
        d = next(d for d in p.detalle_obligaciones if d.entidad == "FINANCIERA EPSILON")
        assert d.en_mora and not d.castigada
        assert d.estado_cuenta == "02"
        assert not d.excluida_por_cuotas
        assert d.cuota_final >= 272_000
        assert d.cuotas_mora == 1 and d.monto_mora == 761_000
        assert p.obligaciones_en_mora == 1
        assert p.obligaciones_castigadas == 0
        assert p.monto_mora_total == 761_000

    def test_castigada_exige_saldo_total(self, raw):
        mod = json.loads(json.dumps(raw))
        ep = mod["ReportHDCplus"]["liabilities"][4]  # FINANCIERA EPSILON
        ep["status"]["account"]["businessAccountStatus"] = "06"
        ep["status"]["account"]["businessAccountStatusDesc"] = "CASTIGADA"
        res = _procesar_respuesta(mod, "x")
        a = analizar_gastos(
            ingreso_bruto_principal=5_000_000,
            score_principal=res.score_advance,
            obligaciones_principal=res.obligaciones,
        )
        p = a.solicitante_principal
        d = next(d for d in p.detalle_obligaciones if d.entidad == "FINANCIERA EPSILON")
        assert d.castigada and d.en_mora
        assert not d.excluida_por_cuotas
        assert d.cuota_final >= 489_000  # nunca menor al saldo completo
        assert d.cuota_final == max(d.cuota_calculada, d.saldo)
        assert any("exigible" in o for o in d.observaciones)
        assert p.obligaciones_castigadas == 1
        assert p.saldo_castigado == 489_000

    def test_sostenimiento_castigado_cuenta_saldo(self, raw):
        mod = json.loads(json.dumps(raw))
        ed = mod["ReportHDCplus"]["liabilities"][2]  # BANCO GAMMA (43 educación)
        ed["status"]["account"]["businessAccountStatus"] = "05"
        ed["status"]["account"]["businessAccountStatusDesc"] = "DUDOSO RECAUDO"
        res = _procesar_respuesta(mod, "x")
        a = analizar_gastos(
            ingreso_bruto_principal=5_000_000,
            score_principal=res.score_advance,
            obligaciones_principal=res.obligaciones,
        )
        d = next(d for d in a.solicitante_principal.detalle_obligaciones if d.entidad == "BANCO GAMMA")
        assert d.linea_credito == LineaCredito.SOSTENIMIENTO
        assert d.castigada
        assert d.cuota_final == 6_952_000
