import httpx

from app.config import settings
from app.services.experian_auth import obtener_token_valor_ingreso
from app.models.experian import ExperianData, ExperianResponse, Aportante, ResultadoPago


TIPOS_DOCUMENTO = {
    "CC": 1,
    "CE": 4,
    "PAS": 5,
    "PPT": 6,
    "TI": 7,
}


async def consultar_valor_ingreso(
    numero_documento: str,
    tipo_documento: str = "CC",
) -> ExperianResponse:
    token = await obtener_token_valor_ingreso()
    url = f"{settings.EXPERIAN_VI_BASE_URL}/cs/incomes/v1/income/indicator"

    tipo_id = TIPOS_DOCUMENTO.get(tipo_documento.upper(), 1)

    params = {
        "TipoIdentificacionUsuario": 2,
        "IdentificacionUsuario": settings.EXPERIAN_VI_SUBSCRIBER_NIT,
        "TipoIDSuscriptor": 2,
        "NitSuscriptor": settings.EXPERIAN_VI_SUBSCRIBER_NIT,
        "NombreSuscriptor": settings.EXPERIAN_VI_SUBSCRIBER_NAME,
        "TipoIdBuscar": tipo_id,
        "IdentificacionBuscar": numero_documento,
        "ProductoId": 12,
        "CanalConsulta": 2,
        "ProductoConsulta": 1,
        "VIPlus": 1,
    }
    headers = {
        "client_id": settings.EXPERIAN_VI_CLIENT_ID,
        "client_secret": settings.EXPERIAN_VI_CLIENT_SECRET,
        "access_token": token,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        raw = resp.json()

    return _mapear_respuesta(raw, numero_documento)


def _mapear_respuesta(raw: dict, cedula: str) -> ExperianResponse:
    respuesta_id = raw.get("respuesta_id")

    aportantes = []
    for ap_raw in raw.get("aportantes", []):
        pagos = [
            ResultadoPago(
                ano_periodo_validado=p["ano_periodo_validado"],
                mes_periodo_validado=p["mes_periodo_validado"],
                realizo_pago=p["realizo_pago"],
                ingresos=p.get("ingresos", 0),
            )
            for p in ap_raw.get("resultado_pagos", [])
        ]
        aportantes.append(Aportante(
            tipo_identificacion_aportante_id=ap_raw.get("tipo_identificacion_aportante_id", 0),
            numero_identificacion_aportante=ap_raw.get("numero_identificacion_aportante", ""),
            razon_social_aportante=ap_raw.get("razon_social_aportante", ""),
            tipo_cotizante_persona_natural=ap_raw.get("tipo_cotizante_persona_natural", 0),
            descripcion_cotizante_persona_natural=ap_raw.get("descripcion_cotizante_persona_natural", ""),
            tiene_salario_integral_actualmente=ap_raw.get("tiene_salario_integral_actualmente", False),
            tiene_salario_fijo_actualmente=ap_raw.get("tiene_salario_fijo_actualmente", False),
            tiene_salario_variable_actualmente=ap_raw.get("tiene_salario_variable_actualmente", False),
            tiene_novedad_ingreso_actualmente_empleador=ap_raw.get("tiene_novedad_ingreso_actualmente_empleador", False),
            tiene_novedad_retiro_actualmente_empleado=ap_raw.get("tiene_novedad_retiro_actualmente_empleado", False),
            tiene_licencia_no_remunerada_actualmente_empleador=ap_raw.get("tiene_licencia_no_remunerada_actualmente_empleador", False),
            ingreso_maximo_empleador=ap_raw.get("ingreso_maximo_empleador", 0),
            ingreso_minimo_empleador=ap_raw.get("ingreso_minimo_empleador", 0),
            promedio_ingresos=ap_raw.get("promedio_ingresos", 0),
            media_ingresos=ap_raw.get("media_ingresos", 0),
            tipo_planilla=ap_raw.get("tipo_planilla", ""),
            description_tipo_planilla=ap_raw.get("description_tipo_planilla", ""),
            actividad_aportante=ap_raw.get("actividad_aportante", ""),
            descripcion_actividad_aportante=ap_raw.get("descripcion_actividad_aportante", ""),
            nivel_impacto_aportante=ap_raw.get("nivel_impacto_aportante", ""),
            benef_upc=ap_raw.get("benef_upc"),
            ded_obl_ley=ap_raw.get("ded_obl_ley"),
            resultado_pagos=pagos,
        ))

    data = ExperianData(
        fecha=raw.get("fecha", ""),
        consulta_id=raw.get("consulta_id"),
        respuesta_id=respuesta_id,
        tipo_identificacion_persona_natural_id=raw.get("tipo_identificacion_persona_natural_id"),
        numero_identificacion_persona_natural=cedula,
        primer_nombre_persona_natural=raw.get("primer_nombre_persona_natural"),
        segundo_nombre_persona_natural=raw.get("segundo_nombre_persona_natural"),
        primer_apellido_persona_natural=raw.get("primer_apellido_persona_natural"),
        segundo_apellido_persona_natural=raw.get("segundo_apellido_persona_natural"),
        EPS=raw.get("EPS"),
        AFP=raw.get("AFP"),
        aportantes=aportantes,
    )

    status = "ok" if respuesta_id == 4 else "error"
    status_msg = None if respuesta_id == 4 else f"respuesta_id={respuesta_id}"

    return ExperianResponse(
        id=raw.get("consulta_id", ""),
        status=status,
        status_message=status_msg,
        provider="experian_api",
        data=data,
    )
