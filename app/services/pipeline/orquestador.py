from __future__ import annotations

import re
import time
from typing import Optional

from app.models.contrato import (
    CampoBooleano,
    CampoExtraido,
    CampoNumerico,
    ContratoExtraido,
    DatosFinancieros,
    DatosInmueble,
    DatosParteContrato,
    DatosVigencia,
    NivelConfianza,
    ServiciosPublicos,
    VerificacionFirma,
)
from app.services.contrato_arrendamiento import (
    AnalisisContrato,
    analizar_contrato,
    _parsear_fecha,
    _parsear_direccion,
    _parsear_arrendadores,
    _parsear_canon,
)
from app.services.pipeline.preproceso import pdf_a_imagenes, preprocesar
from app.services.pipeline.template_registry import (
    TipoCampo,
    detectar_plantilla,
    recortar_roi,
)
from app.services.pipeline.motores.tesseract_motor import ocr_roi, ocr_pagina_completa
from app.services.pipeline.motores.claude_vision_motor import (
    esta_disponible as claude_disponible,
    extraer_con_vision,
    ResultadoClaude,
)

FUENTE = "tesseract"
FUENTE_ROI = "tesseract_roi"
FUENTE_CLAUDE = "claude_vision"
CONFIANZA_BASE_OCR = 0.55
CONFIANZA_ROI = 0.65
CONFIANZA_CLAUDE = 0.90
CONFIANZA_CAMPO_VACIO = 0.0


def extraer_contrato(ruta_pdf: str) -> ContratoExtraido:
    inicio = time.monotonic()
    es_pdf_escaneado = ruta_pdf.lower().endswith(".pdf")

    legacy = analizar_contrato(ruta_pdf)
    texto = legacy.texto_completo or ""

    roi_resultados: dict[str, str] = {}
    vision: Optional[ResultadoClaude] = None
    fuente_usada = FUENTE

    if es_pdf_escaneado and not _tiene_capa_texto(ruta_pdf):
        if claude_disponible():
            try:
                vision = extraer_con_vision(ruta_pdf)
                if vision:
                    fuente_usada = FUENTE_CLAUDE
            except Exception:
                pass

        if not vision:
            try:
                texto_mejorado = _ocr_mejorado_pagina_completa(ruta_pdf)
                if texto_mejorado and len(texto_mejorado) > len(texto):
                    texto = texto_mejorado
                    fuente_usada = "tesseract_preprocesado"
                    legacy = _reparsear_legacy(texto, legacy)
            except Exception:
                pass

            try:
                roi_resultados = _extraer_por_roi(ruta_pdf)
            except Exception:
                pass

    if vision:
        legacy = _aplicar_vision(legacy, vision)

    firma_arrendador, firma_arrendatario = _extraer_secciones_firma(texto)

    arrendador = _extraer_arrendador(legacy, texto, firma_arrendador, roi_resultados, fuente_usada)
    arrendatario = _extraer_arrendatario(texto, firma_arrendatario, roi_resultados, fuente_usada)
    inmueble = _extraer_inmueble(legacy, texto, roi_resultados, fuente_usada)
    financiero = _extraer_financiero(legacy, texto, roi_resultados, fuente_usada)
    vigencia = _extraer_vigencia(legacy, texto, roi_resultados, fuente_usada)

    if vision and vision.tiene_firma_arrendador is not None:
        firma = VerificacionFirma(
            tiene_firma_arrendador=bool(vision.tiene_firma_arrendador),
            tiene_firma_arrendatario=bool(vision.tiene_firma_arrendatario),
            confianza_arrendador=CONFIANZA_CLAUDE,
            confianza_arrendatario=CONFIANZA_CLAUDE,
            ambas_firmadas=bool(vision.tiene_firma_arrendador and vision.tiene_firma_arrendatario),
        )
    else:
        from app.services.pipeline.verificar_firma import verificar_firmas
        resultado_firma = verificar_firmas(ruta_pdf)
        firma = VerificacionFirma(
            tiene_firma_arrendador=resultado_firma.tiene_firma_arrendador,
            tiene_firma_arrendatario=resultado_firma.tiene_firma_arrendatario,
            confianza_arrendador=resultado_firma.confianza_arrendador,
            confianza_arrendatario=resultado_firma.confianza_arrendatario,
            ambas_firmadas=resultado_firma.ambas_firmadas,
        )

    validaciones_fallidas = _validar_cruces(financiero, vigencia)
    if not firma.ambas_firmadas:
        validaciones_fallidas.append("firma_incompleta")

    todos_campos = _recolectar_campos(
        arrendador, arrendatario, inmueble, financiero, vigencia,
    )
    campos_revision = [path for path, c in todos_campos if c.requiere_revision]

    confianzas = [c.confianza for _, c in todos_campos if c.valor is not None]
    confianza_global = sum(confianzas) / len(confianzas) if confianzas else 0.0

    if confianza_global >= 0.92 and not validaciones_fallidas:
        nivel = NivelConfianza.ALTO
    elif confianza_global >= 0.75:
        nivel = NivelConfianza.MEDIO
    else:
        nivel = NivelConfianza.BAJO

    elapsed_ms = int((time.monotonic() - inicio) * 1000)

    return ContratoExtraido(
        arrendador=arrendador,
        arrendatario=arrendatario,
        inmueble=inmueble,
        financiero=financiero,
        vigencia=vigencia,
        firma=firma,
        confianza_global=round(confianza_global, 3),
        nivel=nivel,
        campos_revision=campos_revision,
        validaciones_fallidas=validaciones_fallidas,
        motor_principal=fuente_usada,
        tiempo_procesamiento_ms=elapsed_ms,
        texto_completo=texto,
    )


def _reparsear_legacy(texto: str, original: AnalisisContrato) -> AnalisisContrato:
    """Re-ejecuta los parsers del legacy sobre texto mejorado."""
    fecha = _parsear_fecha(texto) or original.fecha_firma
    direccion, nomenclatura = _parsear_direccion(texto)
    arrendadores = _parsear_arrendadores(texto) or original.arrendadores
    canon = _parsear_canon(texto) or original.canon_mensual

    return AnalisisContrato(
        fecha_firma=fecha,
        direccion=direccion or original.direccion,
        nomenclatura=nomenclatura or original.nomenclatura,
        arrendadores=arrendadores,
        canon_mensual=canon,
        texto_completo=texto,
    )


def _aplicar_vision(legacy: AnalisisContrato, vision: ResultadoClaude) -> AnalisisContrato:
    """Sobreescribe los campos del legacy con los de Claude Vision (más confiables)."""
    nombre = vision.nombre_arrendador
    cedula = vision.cedula_arrendador
    arrendadores = legacy.arrendadores
    if nombre:
        arrendadores = f"{nombre} — CC {cedula}" if cedula else nombre

    return AnalisisContrato(
        fecha_firma=vision.fecha_inicio or legacy.fecha_firma,
        direccion=legacy.direccion,
        nomenclatura=legacy.nomenclatura,
        arrendadores=arrendadores,
        canon_mensual=vision.canon_mensual or legacy.canon_mensual,
        texto_completo=legacy.texto_completo,
    )


def _tiene_capa_texto(ruta: str) -> bool:
    import fitz
    doc = fitz.open(ruta)
    tiene = any(page.get_text().strip() for page in doc)
    doc.close()
    return tiene


def _extraer_por_roi(ruta_pdf: str) -> dict[str, str]:
    imagenes_raw = pdf_a_imagenes(ruta_pdf, dpi=300)
    imagenes = [preprocesar(img) for img in imagenes_raw]

    plantilla = detectar_plantilla(imagenes)
    if not plantilla:
        return {}

    resultados: dict[str, str] = {}
    num_paginas = len(imagenes)

    for roi in plantilla.rois:
        idx = roi.pagina if roi.pagina >= 0 else num_paginas + roi.pagina
        if idx < 0 or idx >= num_paginas:
            continue

        crop = recortar_roi(imagenes[idx], roi)
        if crop.size == 0:
            continue

        texto = ocr_roi(crop, roi)
        if texto and _roi_es_valido(texto, roi):
            resultados[roi.campo_path] = texto

    return resultados


def _roi_es_valido(texto: str, roi: "ROI") -> bool:
    """Rechaza resultados ROI que son claramente basura."""
    if len(texto) > 80 and roi.tipo != TipoCampo.TEXTO_MANUSCRITO:
        return False
    if len(texto) > 200:
        return False

    chars_raros = sum(1 for c in texto if c in "{}[]<>|\\~^`")
    if chars_raros > len(texto) * 0.15:
        return False

    letras = sum(1 for c in texto if c.isalpha())
    digitos = sum(1 for c in texto if c.isdigit())
    total_util = letras + digitos
    if len(texto) > 5 and total_util < len(texto) * 0.30:
        return False

    if roi.tipo == TipoCampo.NUMERO:
        if digitos < 3:
            return False
    elif roi.tipo == TipoCampo.EMAIL:
        if "@" not in texto and "©" not in texto and "." not in texto:
            return False

    return True


def _ocr_mejorado_pagina_completa(ruta_pdf: str) -> str:
    """OCR de página completa usando preproceso mejorado (sin ROIs)."""
    imagenes_raw = pdf_a_imagenes(ruta_pdf, dpi=300)
    textos = []
    for img in imagenes_raw:
        procesada = preprocesar(img)
        texto_pagina = ocr_pagina_completa(procesada)
        textos.append(texto_pagina)
    return "\n".join(textos)


# ---------------------------------------------------------------------------
# Sección de firmas — fuente más confiable para datos de contacto
# ---------------------------------------------------------------------------

def _extraer_secciones_firma(texto: str) -> tuple[str, str]:
    """Aísla los bloques de firma del arrendador y arrendatario.

    Busca el último 'EL ARRENDADOR' seguido de 'Nombre:' que indica la zona
    de firmas (no las cláusulas que mencionan "EL ARRENDADOR" en el cuerpo).
    """
    firma_arrendador = ""
    firma_arrendatario = ""

    patron_firma = r"EL\s+ARRENDADOR\s*\n\s*Nombre[.:\s]"
    matches = list(re.finditer(patron_firma, texto, re.IGNORECASE))
    if matches:
        pos_firma = matches[-1].start()
        m_arrendatario = re.search(
            r"EL\s+ARRENDATARIO\s*\n\s*Nombre",
            texto[pos_firma:], re.IGNORECASE,
        )
        if m_arrendatario:
            firma_arrendador = texto[pos_firma:pos_firma + m_arrendatario.start()]
            firma_arrendatario = texto[pos_firma + m_arrendatario.start():]
        else:
            firma_arrendador = texto[pos_firma:]

    return firma_arrendador, firma_arrendatario


def _extraer_datos_firma(bloque: str) -> dict[str, Optional[str]]:
    """Extrae campos estructurados de un bloque de firma."""
    datos: dict[str, Optional[str]] = {
        "nombre": None, "cedula": None, "email": None,
        "celular": None, "ciudad": None, "direccion_notificacion": None,
    }
    if not bloque:
        return datos

    m = re.search(r"Nombre[.:\s]*([^\n]{3,50})", bloque)
    if m:
        nombre = m.group(1).strip()
        nombre = re.sub(r"[|>\d$:]+$", "", nombre).strip()
        if len(nombre) > 2:
            datos["nombre"] = nombre

    m = re.search(r"C\.?C\.?\s*(?:No\.?)?\s*[.:\s]*(\d[\d\s.]+)", bloque)
    if m:
        cedula = re.sub(r"[\s.]", "", m.group(1))
        if len(cedula) >= 5:
            datos["cedula"] = cedula

    m = re.search(r"E-?[Mm]ail[:\s]*([^\n]{3,60})", bloque)
    if m:
        raw_email = m.group(1).strip()
        if re.search(r"[@©®(2)]|\.com|\.co|gmail|hotmail|yahoo|outlook", raw_email, re.IGNORECASE):
            datos["email"] = _limpiar_email(raw_email)

    m = re.search(r"[Cc]elular[:\s]*([^\n]{3,30})", bloque)
    if m:
        val = m.group(1).strip()
        nums = re.sub(r"[^\d]", "", val)
        if len(nums) >= 7:
            datos["celular"] = nums

    m = re.search(r"[Cc]iudad[:\s]*([^\n]{2,40})", bloque)
    if m:
        ciudad = m.group(1).strip().split("\t")[0].strip()
        ciudad = re.sub(r"[|,]+$", "", ciudad).strip()
        if len(ciudad) > 1 and not re.search(r"\d{4,}", ciudad):
            datos["ciudad"] = ciudad

    m = re.search(r"Dir\.?\s*Notificaci[oó]n[:\s]*([^\n]{3,60})", bloque)
    if m:
        dir_val = m.group(1).strip()
        if re.search(r"\d", dir_val) and not re.match(r"^(Ciudad|Celular|E-?Mail)", dir_val, re.IGNORECASE):
            datos["direccion_notificacion"] = dir_val

    return datos


# ---------------------------------------------------------------------------
# Extracción por sección
# ---------------------------------------------------------------------------

def _campo(valor: Optional[str], confianza: float = CONFIANZA_BASE_OCR, fuente: str = FUENTE) -> CampoExtraido:
    if not valor:
        return CampoExtraido(confianza=CONFIANZA_CAMPO_VACIO, fuente=fuente, requiere_revision=True)
    return CampoExtraido(
        valor=valor,
        confianza=confianza,
        fuente=fuente,
        requiere_revision=confianza < 0.75,
    )


def _campo_num(valor: Optional[str], numerico: Optional[int], confianza: float = CONFIANZA_BASE_OCR, fuente: str = FUENTE) -> CampoNumerico:
    if numerico is None and valor is None:
        return CampoNumerico(confianza=CONFIANZA_CAMPO_VACIO, fuente=fuente, requiere_revision=True)
    return CampoNumerico(
        valor=valor,
        valor_numerico=numerico,
        confianza=confianza,
        fuente=fuente,
        requiere_revision=confianza < 0.75,
    )


def _campo_bool(valor: Optional[bool], confianza: float = CONFIANZA_BASE_OCR, fuente: str = FUENTE) -> CampoBooleano:
    if valor is None:
        return CampoBooleano(confianza=CONFIANZA_CAMPO_VACIO, fuente=fuente, requiere_revision=True)
    return CampoBooleano(
        valor=str(valor),
        valor_bool=valor,
        confianza=confianza,
        fuente=fuente,
        requiere_revision=confianza < 0.75,
    )


def _roi_o_fallback(
    roi_resultados: dict[str, str],
    campo_path: str,
    fallback: Optional[str],
    conf_roi: float = CONFIANZA_ROI,
    conf_fallback: float = CONFIANZA_BASE_OCR,
    fuente_usada: str = FUENTE,
) -> tuple[Optional[str], float, str]:
    """Retorna (valor, confianza, fuente) priorizando ROI sobre fallback regex."""
    roi_val = roi_resultados.get(campo_path)
    if roi_val and len(roi_val) >= 2:
        return roi_val, conf_roi, FUENTE_ROI
    if fallback:
        return fallback, conf_fallback, fuente_usada
    return None, 0.0, fuente_usada


def _extraer_arrendador(
    legacy: AnalisisContrato, texto: str, firma: str,
    roi: dict[str, str] = {}, fuente: str = FUENTE,
) -> DatosParteContrato:
    datos_firma = _extraer_datos_firma(firma)

    nombre = datos_firma["nombre"]
    cedula = datos_firma["cedula"]

    if not nombre and legacy.arrendadores:
        partes = legacy.arrendadores.split("—")
        nombre = partes[0].strip() if partes else legacy.arrendadores
    if not cedula and legacy.arrendadores and "—" in legacy.arrendadores:
        cc = re.sub(r"[^\d]", "", legacy.arrendadores.split("—")[1])
        if cc:
            cedula = cc

    es_claude = fuente == FUENTE_CLAUDE
    conf_firma = CONFIANZA_CLAUDE if es_claude else (0.70 if firma else 0.55)
    fuente_dato = FUENTE_CLAUDE if es_claude else fuente

    n_val, n_conf, n_src = _roi_o_fallback(roi, "arrendador.nombre", nombre, 0.68, conf_firma, fuente_dato)
    c_val, c_conf, c_src = _roi_o_fallback(roi, "arrendador.cedula", cedula, 0.70, conf_firma, fuente_dato)
    e_val, e_conf, e_src = _roi_o_fallback(roi, "arrendador.email", datos_firma["email"], 0.60, 0.65, fuente)
    cel_val, cel_conf, cel_src = _roi_o_fallback(roi, "arrendador.celular", datos_firma["celular"], 0.60, 0.65, fuente)
    ci_val, ci_conf, ci_src = _roi_o_fallback(roi, "arrendador.ciudad", datos_firma["ciudad"], 0.60, 0.65, fuente)

    return DatosParteContrato(
        nombre=_campo(n_val, n_conf, n_src),
        cedula=_campo(c_val, c_conf, c_src),
        email=_campo(e_val, e_conf, e_src),
        celular=_campo(cel_val, cel_conf, cel_src),
        ciudad=_campo(ci_val, ci_conf, ci_src),
        direccion_notificacion=_campo(
            datos_firma["direccion_notificacion"],
            0.60 if datos_firma["direccion_notificacion"] else 0.0,
        ),
    )


def _extraer_arrendatario(
    texto: str, firma: str,
    roi: dict[str, str] = {}, fuente: str = FUENTE,
) -> DatosParteContrato:
    datos_firma = _extraer_datos_firma(firma)

    nombre = datos_firma["nombre"]
    cedula = datos_firma["cedula"]

    if not nombre:
        nombre = _buscar_regex(
            texto,
            r"[Nn]ombre\s+del\s+[Aa]rrendatario[:\s|]*([^\n]{3,60})",
        )
    if not cedula:
        m = re.search(
            r"[Ii]dentificaci[oó]n\s+del\s+[Aa]rrendatario\s*\n?\s*([^\n]{3,20})",
            texto,
        )
        if m:
            nums = re.findall(r"\d+", m.group(1))
            if nums:
                cedula = "".join(nums)

    conf_firma = 0.70 if firma else 0.55

    n_val, n_conf, n_src = _roi_o_fallback(roi, "arrendatario.nombre", nombre, 0.68, conf_firma, fuente)
    c_val, c_conf, c_src = _roi_o_fallback(roi, "arrendatario.cedula", cedula, 0.70, conf_firma, fuente)
    e_val, e_conf, e_src = _roi_o_fallback(roi, "arrendatario.email", datos_firma["email"], 0.60, 0.65, fuente)
    cel_val, cel_conf, cel_src = _roi_o_fallback(roi, "arrendatario.celular", datos_firma["celular"], 0.60, 0.65, fuente)
    ci_val, ci_conf, ci_src = _roi_o_fallback(roi, "arrendatario.ciudad", datos_firma["ciudad"], 0.60, 0.65, fuente)

    return DatosParteContrato(
        nombre=_campo(n_val, n_conf, n_src),
        cedula=_campo(c_val, c_conf, c_src),
        email=_campo(e_val, e_conf, e_src),
        celular=_campo(cel_val, cel_conf, cel_src),
        ciudad=_campo(ci_val, ci_conf, ci_src),
        direccion_notificacion=_campo(
            datos_firma["direccion_notificacion"],
            0.60 if datos_firma["direccion_notificacion"] else 0.0,
        ),
    )


def _extraer_inmueble(
    legacy: AnalisisContrato, texto: str,
    roi: dict[str, str] = {}, fuente: str = FUENTE,
) -> DatosInmueble:
    seccion_inmueble = ""
    m = re.search(r"DATOS\s+DEL\s+INMUEBLE([\s\S]{0,800}?)(?:VALOR|TERCERA|Valor\s+del\s+Canon)", texto, re.IGNORECASE)
    if m:
        seccion_inmueble = m.group(1)

    ciudad = _buscar_regex(
        seccion_inmueble or texto,
        r"[Cc]iudad\s*\n?\s*([^\n|]{3,30})",
    )
    if ciudad:
        ciudad = _limpiar_valor_tabla(ciudad)

    barrio = _buscar_regex(
        seccion_inmueble or texto,
        r"[Bb]arrio\s+de\s+ubicaci[oó]n\s+del\s*\n?\s*inmueble\s*\n?\s*([^\n|]{3,50})",
    )
    if barrio:
        barrio = _limpiar_valor_tabla(barrio)

    ph = _detectar_checkbox(
        seccion_inmueble or texto,
        r"propiedad\s+horizontal",
        r"Si\s*X",
    )

    servicios = ServiciosPublicos(
        agua=_detectar_servicio(seccion_inmueble or texto, "Agua"),
        gas=_detectar_servicio(seccion_inmueble or texto, "Gas"),
        energia=_detectar_servicio(seccion_inmueble or texto, r"Energ[ií]a\s+El[eé]ctrica"),
        telefono=_detectar_servicio(seccion_inmueble or texto, r"Tel[eé]fono"),
        internet=_detectar_servicio(seccion_inmueble or texto, "Internet"),
    )

    direccion = legacy.direccion
    if direccion:
        direccion = _limpiar_valor_tabla(direccion)

    d_val, d_conf, d_src = _roi_o_fallback(roi, "inmueble.direccion", direccion, 0.65, 0.55, fuente)
    b_val, b_conf, b_src = _roi_o_fallback(roi, "inmueble.barrio", barrio, 0.62, 0.50, fuente)
    c_val, c_conf, c_src = _roi_o_fallback(roi, "inmueble.ciudad", ciudad, 0.65, 0.55, fuente)

    # ROI para checkboxes de servicios
    for srv_name, srv_field in [("agua", "inmueble.servicios.agua"), ("gas", "inmueble.servicios.gas"),
                                 ("energia", "inmueble.servicios.energia"), ("telefono", "inmueble.servicios.telefono"),
                                 ("internet", "inmueble.servicios.internet")]:
        roi_val = roi.get(srv_field)
        if roi_val is not None:
            val_bool = roi_val == "True"
            setattr(servicios, srv_name, _campo_bool(val_bool, 0.80, FUENTE_ROI))

    ph_roi = roi.get("inmueble.propiedad_horizontal")
    if ph_roi is not None:
        ph = _campo_bool(ph_roi == "True", 0.80, FUENTE_ROI)

    return DatosInmueble(
        direccion=_campo(d_val, d_conf, d_src),
        barrio=_campo(b_val, b_conf, b_src),
        ciudad=_campo(c_val, c_conf, c_src),
        propiedad_horizontal=ph,
        servicios=servicios,
    )


def _extraer_financiero(
    legacy: AnalisisContrato, texto: str,
    roi: dict[str, str] = {}, fuente: str = FUENTE,
) -> DatosFinancieros:
    canon_letras = _buscar_regex(
        texto,
        r"(\w+\s+mill[oó]n(?:es)?\s+de\s+pesos\s*(?:m/?l)?(?:\s*\([^)]*\))?)",
    )
    if not canon_letras:
        canon_letras = _buscar_regex(
            texto,
            r"[Vv]alor\s+en\s+letras[^)]*\)\)?\s*\.?\s*([A-Za-záéíóúñ][^\n(]{5,60})",
        )

    es_claude = fuente == FUENTE_CLAUDE
    canon_str = str(legacy.canon_mensual) if legacy.canon_mensual else None
    canon_cruce = _verificar_cruce_canon(legacy.canon_mensual, canon_letras)

    seccion_valor = ""
    m = re.search(r"VALOR([\s\S]{0,600}?)(?:Condiciones\s+Generales|TERCERA)", texto, re.IGNORECASE)
    if m:
        seccion_valor = m.group(1)
    fuente_cuenta = seccion_valor or texto

    tipo_cuenta_raw = _buscar_regex(
        fuente_cuenta,
        r"[Tt]ipo\s+de\s+cuenta\s*\n?\s*([^\n]{3,30})",
    )
    tipo_cuenta = None
    if tipo_cuenta_raw:
        lower = tipo_cuenta_raw.lower()
        if "ahorro" in lower or re.search(r"ahorro", lower):
            tipo_cuenta = "ahorros"
        elif "corriente" in lower:
            tipo_cuenta = "corriente"
        else:
            tipo_cuenta = _limpiar_valor_tabla(tipo_cuenta_raw)

    numero_cuenta = _buscar_regex(
        fuente_cuenta,
        r"[Nn][uú]mero\s+de\s+cuenta\s*\n?\s*([^\n]{5,30})",
    )
    if numero_cuenta:
        digitos = re.sub(r"[^\d]", "", numero_cuenta)
        numero_cuenta = _deduplicar_valor(digitos)

    banco = _buscar_regex(
        fuente_cuenta,
        r"[Bb]anco\s+(?:en\s+)?donde\s+se\s+consigna\s*\n?\s*([^\n]{3,40})",
    )
    if banco:
        banco = _limpiar_valor_tabla(banco)

    nombre_prop = _buscar_regex(
        fuente_cuenta,
        r"[Nn]ombre\s+del\s+propietario\s+del\s+inmueble\s+([^\n]{3,60})",
    )
    if nombre_prop:
        nombre_prop = _limpiar_valor_tabla(nombre_prop)

    admin_incluida: Optional[bool] = None
    if re.search(r"cuota\s+de\s+administraci[oó]n\s+hace\s+parte.*?No\s*X", texto, re.IGNORECASE):
        admin_incluida = False
    elif re.search(r"cuota\s+de\s+administraci[oó]n\s+hace\s+parte.*?Si\s*X", texto, re.IGNORECASE):
        admin_incluida = True

    nc_val, nc_conf, nc_src = _roi_o_fallback(roi, "financiero.numero_cuenta", numero_cuenta, 0.68, 0.55, fuente)
    bk_val, bk_conf, bk_src = _roi_o_fallback(roi, "financiero.banco", banco, 0.62, 0.50, fuente)
    np_val, np_conf, np_src = _roi_o_fallback(roi, "financiero.nombre_propietario_cuenta", nombre_prop, 0.62, 0.55, fuente)
    cl_val, cl_conf, cl_src = _roi_o_fallback(roi, "financiero.canon_letras", canon_letras, 0.55, 0.45, fuente)

    return DatosFinancieros(
        canon_mensual=_campo_num(canon_str, legacy.canon_mensual, CONFIANZA_CLAUDE if es_claude and legacy.canon_mensual else (0.60 if legacy.canon_mensual else 0.0), fuente),
        canon_letras=_campo(cl_val, cl_conf, cl_src),
        canon_cruce_ok=canon_cruce,
        admin_incluida=_campo_bool(admin_incluida, 0.70 if admin_incluida is not None else 0.0, fuente),
        nombre_propietario_cuenta=_campo(np_val, np_conf, np_src),
        tipo_cuenta=_campo(tipo_cuenta, 0.65 if tipo_cuenta else 0.0, fuente),
        numero_cuenta=_campo(nc_val, nc_conf, nc_src),
        banco=_campo(bk_val, bk_conf, bk_src),
    )


def _extraer_vigencia(
    legacy: AnalisisContrato, texto: str,
    roi: dict[str, str] = {}, fuente: str = FUENTE,
) -> DatosVigencia:
    es_claude = fuente == FUENTE_CLAUDE
    fecha_inicio = legacy.fecha_firma

    vigencia_meses = None
    m = re.search(r"vigencia[^0-9]{0,30}?(\d{1,3})\s*meses", texto, re.IGNORECASE)
    if m:
        vigencia_meses = int(m.group(1))

    fecha_terminacion = None
    m = re.search(
        r"[Ff]echa\s+de\s+terminaci[oó]n\s+del\s*\n?\s*[Cc]ontrato",
        texto,
    )
    if m:
        resto = texto[m.end():m.end() + 80]
        m_fecha = re.search(r"(\d{1,2}[/\-]\d{1,2}[/\-]\d{4})", resto)
        if m_fecha:
            fecha_terminacion = m_fecha.group(1)
        else:
            from app.services.contrato_arrendamiento import _buscar_mes
            m_texto = re.search(r"([A-Za-záéíóúñ]{3,12})\s+(\d{4})", resto)
            if m_texto:
                mes = _buscar_mes(m_texto.group(1))
                if mes:
                    fecha_terminacion = f"01/{mes:02d}/{m_texto.group(2)}"

    conf_fecha = CONFIANZA_CLAUDE if es_claude and fecha_inicio else 0.55
    fi_val, fi_conf, fi_src = _roi_o_fallback(roi, "vigencia.fecha_inicio", fecha_inicio, 0.62, conf_fecha, fuente)
    ft_val, ft_conf, ft_src = _roi_o_fallback(roi, "vigencia.fecha_terminacion", fecha_terminacion, 0.58, 0.45, fuente)

    vm_roi = roi.get("vigencia.vigencia_meses")
    if vm_roi and vm_roi.isdigit():
        vigencia_meses = int(vm_roi)

    vigencia_cruce = _verificar_cruce_vigencia(fi_val, ft_val, vigencia_meses)

    return DatosVigencia(
        fecha_inicio=_campo(fi_val, fi_conf, fi_src),
        fecha_terminacion=_campo(ft_val, ft_conf, ft_src),
        vigencia_meses=_campo_num(
            str(vigencia_meses) if vigencia_meses else None,
            vigencia_meses,
            0.65 if vigencia_meses else 0.0,
            fuente,
        ),
        vigencia_cruce_ok=vigencia_cruce,
    )


# ---------------------------------------------------------------------------
# Validación cruzada
# ---------------------------------------------------------------------------

def _validar_cruces(fin: DatosFinancieros, vig: DatosVigencia) -> list[str]:
    fallidas = []
    if fin.canon_cruce_ok is False:
        fallidas.append("canon_letras_vs_numeros")
    if vig.vigencia_cruce_ok is False:
        fallidas.append("vigencia_fechas_vs_meses")
    return fallidas


def _verificar_cruce_canon(canon_num: Optional[int], canon_letras: Optional[str]) -> Optional[bool]:
    if canon_num is None or not canon_letras:
        return None
    _PALABRAS = {"un": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5}
    m = re.search(r"(\w+)\s+mill[oó]n", canon_letras.lower())
    if not m:
        return None
    palabra = m.group(1)
    millones = _PALABRAS.get(palabra)
    if millones is None:
        return None
    return canon_num == millones * 1_000_000


def _verificar_cruce_vigencia(
    inicio: Optional[str], fin: Optional[str], meses: Optional[int],
) -> Optional[bool]:
    if not inicio or not meses:
        return None
    return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _buscar_regex(texto: str, patron: str) -> Optional[str]:
    m = re.search(patron, texto, re.IGNORECASE)
    if not m:
        return None
    val = m.group(1).strip() if m.lastindex else m.group(0).strip()
    val = re.sub(r"\s+", " ", val).strip()
    if len(val) < 2:
        return None
    return val


def _limpiar_email(raw: str) -> Optional[str]:
    raw = raw.replace(" ", "").replace("()", "@").replace("(@)", "@")
    raw = raw.replace("©", "@").replace("®", "@").replace("(2)", "@")
    m = re.search(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", raw)
    return m.group(0) if m else raw.strip()


def _limpiar_valor_tabla(valor: str) -> str:
    """Limpia valores extraídos de tablas DOCX que vienen con '|' y duplicados."""
    valor = re.sub(r"\s*\|\s*", " | ", valor).strip()
    partes = [p.strip() for p in valor.split("|") if p.strip()]
    if not partes:
        return valor
    vistos: list[str] = []
    for p in partes:
        if p.lower() not in [v.lower() for v in vistos]:
            vistos.append(p)
    return vistos[0] if len(vistos) == 1 else " | ".join(vistos)


def _deduplicar_valor(valor: str) -> str:
    """Si un valor numérico aparece duplicado (ej: '000738416000738416'), lo deduplica."""
    n = len(valor)
    if n >= 6 and n % 2 == 0:
        mitad = n // 2
        if valor[:mitad] == valor[mitad:]:
            return valor[:mitad]
    return valor


def _detectar_checkbox(texto: str, contexto: str, patron_si: str) -> CampoBooleano:
    bloque = re.search(contexto + r"[\s\S]{0,80}", texto, re.IGNORECASE)
    if not bloque:
        return _campo_bool(None, 0.0)
    fragmento = bloque.group(0)
    si = bool(re.search(patron_si, fragmento, re.IGNORECASE))
    return _campo_bool(si, 0.70)


def _detectar_servicio(texto: str, nombre_servicio: str) -> CampoBooleano:
    patron = nombre_servicio + r"[:\s]*Si\s*X"
    si = bool(re.search(patron, texto, re.IGNORECASE))
    if si:
        return _campo_bool(True, 0.75)
    patron_no = nombre_servicio + r"[:\s]*(?:Si\s+)?No\s*X"
    no = bool(re.search(patron_no, texto, re.IGNORECASE))
    if no:
        return _campo_bool(False, 0.75)
    return _campo_bool(None, 0.0)


def _recolectar_campos(
    arrendador: DatosParteContrato,
    arrendatario: DatosParteContrato,
    inmueble: DatosInmueble,
    financiero: DatosFinancieros,
    vigencia: DatosVigencia,
) -> list[tuple[str, CampoExtraido]]:
    campos: list[tuple[str, CampoExtraido]] = []

    for nombre_seccion, seccion in [("arrendador", arrendador), ("arrendatario", arrendatario)]:
        for nombre_campo in ["nombre", "cedula", "email", "celular", "ciudad", "direccion_notificacion"]:
            c = getattr(seccion, nombre_campo, None)
            if isinstance(c, CampoExtraido):
                campos.append((f"{nombre_seccion}.{nombre_campo}", c))

    for nombre_campo in ["direccion", "barrio", "ciudad"]:
        c = getattr(inmueble, nombre_campo, None)
        if isinstance(c, CampoExtraido):
            campos.append((f"inmueble.{nombre_campo}", c))
    campos.append(("inmueble.propiedad_horizontal", inmueble.propiedad_horizontal))
    for srv in ["agua", "gas", "energia", "telefono", "internet"]:
        c = getattr(inmueble.servicios, srv, None)
        if isinstance(c, CampoExtraido):
            campos.append((f"inmueble.servicios.{srv}", c))

    for nombre_campo in ["canon_mensual", "canon_letras", "admin_incluida", "nombre_propietario_cuenta",
                          "tipo_cuenta", "numero_cuenta", "banco"]:
        c = getattr(financiero, nombre_campo, None)
        if isinstance(c, CampoExtraido):
            campos.append((f"financiero.{nombre_campo}", c))

    for nombre_campo in ["fecha_inicio", "fecha_terminacion", "vigencia_meses"]:
        c = getattr(vigencia, nombre_campo, None)
        if isinstance(c, CampoExtraido):
            campos.append((f"vigencia.{nombre_campo}", c))

    return campos
