import re
from dataclasses import dataclass
from typing import Optional

import fitz
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import io
import docx

Image.MAX_IMAGE_PIXELS = 300000000


@dataclass
class AnalisisContrato:
    fecha_firma: Optional[str] = None
    direccion: Optional[str] = None
    nomenclatura: Optional[str] = None
    arrendadores: Optional[str] = None
    canon_mensual: Optional[int] = None
    texto_completo: str = ""
    error: Optional[str] = None


_MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

_MESES_OCR = {
    **_MESES,
    "enere": 1, "enevo": 1, "ener": 1, "ene": 1,
    "febrere": 2, "febr": 2, "feb": 2,
    "marz": 3, "mar": 3,
    "abri": 4, "abr": 4,
    "maye": 5, "may": 5,
    "juni": 6, "jun": 6,
    "juli": 7, "jul": 7,
    "agost": 8, "ago": 8,
    "sept": 9, "sep": 9,
    "octub": 10, "oct": 10,
    "noviem": 11, "nov": 11,
    "diciem": 12, "dic": 12,
}


def _buscar_mes(palabra: str) -> Optional[int]:
    p = palabra.lower().strip().rstrip("o.")
    for clave, num in _MESES_OCR.items():
        if p.startswith(clave) or clave.startswith(p):
            return num
    return None


def _parsear_fecha(texto: str) -> Optional[str]:
    # Patrón para formularios: "Fecha de Inicio del Contrato" seguido de mes y año
    m = re.search(
        r"(?:Fecha\s+de\s+Inicio|Inicio\s+del\s+Contrato)[^\n]*?([A-Za-záéíóúñÁÉÍÓÚÑ]{3,12})\s+(\d{4})",
        texto, re.IGNORECASE,
    )
    if m:
        mes = _buscar_mes(m.group(1))
        if mes:
            return f"01/{mes:02d}/{m.group(2)}"

    # Variante OCR: "Fecha de Inicio" con ruido entre medio
    m = re.search(
        r"Inicio\s+del\s+Contrato[^\n]*?([A-Za-záéíóúñÁÉÍÓÚÑ]{3,12})\s*(\d{4})",
        texto, re.IGNORECASE,
    )
    if m:
        mes = _buscar_mes(m.group(1))
        if mes:
            return f"01/{mes:02d}/{m.group(2)}"

    # Patrón: "a los X días del mes de MONTH de YEAR"
    m = re.search(
        r"a\s+los\s+(\d{1,2})\s+d[ií]as?\s+del?\s+mes\s+de\s+(\w+)\s+de(?:l\s+a[ñn]o)?\s+(\d{4})",
        texto, re.IGNORECASE,
    )
    if m:
        mes = _buscar_mes(m.group(2))
        if mes:
            return f"{int(m.group(1)):02d}/{mes:02d}/{m.group(3)}"

    patrones = [
        r"(?:firmado|suscrito|celebrado|otorgado)\s+(?:en\s+\w+\s*,?\s*)?(?:el\s+)?(?:d[ií]a\s+)?(\d{1,2})\s+(?:del?\s+mes\s+de\s+|de\s+)(\w+)\s+(?:del?\s+a[ñn]o\s+)?(?:de\s+)?(\d{4})",
        r"fecha[:\s]+(\d{1,2})\s+(?:de\s+)(\w+)\s+(?:de\s+)?(\d{4})",
        r"(\d{1,2})\s+de\s+(\w+)\s+de(?:l\s+a[ñn]o)?\s+(\d{4})",
        r"(\d{1,2})/(\d{1,2})/(\d{4})",
        r"(\d{1,2})-(\d{1,2})-(\d{4})",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            dia, mes_str, anio = m.group(1), m.group(2), m.group(3)
            mes = _buscar_mes(mes_str)
            if mes:
                return f"{int(dia):02d}/{mes:02d}/{anio}"
            if mes_str.isdigit():
                return f"{int(dia):02d}/{int(mes_str):02d}/{anio}"
    return None


def _parsear_direccion(texto: str) -> tuple:
    direccion = None
    nomenclatura = None

    # Patrón para formularios: "Dirección Inmueble" seguido del valor en la línea
    m = re.search(
        r"Direcci[oó]n\s+[Ii]nmueble[:\s|]*([^\n]{5,80})",
        texto,
    )
    if m:
        d = m.group(1).strip().strip("|").strip()
        tiene_numero = bool(re.search(r"\d", d))
        tiene_via = bool(re.search(r"(?:calle|carrera|cra|cll|kra|kr|avenida|diagonal|transversal|manzana|lote)\b", d, re.IGNORECASE))
        if (d and len(d) > 8 and (tiene_numero or tiene_via)
            and not re.match(r"^(Barrio|El\s+inmueble|Si|No)", d, re.IGNORECASE)):
            direccion = re.sub(r"\s+", " ", d)

    if not direccion:
        patrones_dir = [
            r"(?:calle|carrera|avenida|diagonal|transversal|cra|cll|kra|kr)\s*\.?\s*\d+[^\n,;]{5,60}",
            r"(?:ubicado\s+en|situado\s+en)[:\s]+([^\n,;]{10,80})",
        ]
        for patron in patrones_dir:
            m = re.search(patron, texto, re.IGNORECASE)
            if m:
                d = m.group(1).strip() if m.lastindex else m.group(0).strip()
                d = re.sub(r"\s+", " ", d)
                if (len(d) > 8 and re.search(r"\d", d)
                        and not re.search(r"(?:regir|c[oó]digo|civil|ley|cl[aá]usula)", d, re.IGNORECASE)):
                    direccion = d
                    break

    # Buscar en sección INMUEBLE ubicado en
    if not direccion:
        m = re.search(
            r"INMUEBLE\s+[Uu]bicado\s+en\s*\n\s*(.+?)(?:\n|$)",
            texto,
        )
        if m:
            d = re.sub(r"\s+", " ", m.group(1).strip())
            if len(d) > 8 and re.search(r"\d", d) and not re.search(r"(?:regir|código|civil|ley)", d, re.IGNORECASE):
                direccion = d

    patrones_nom = [
        r"(?:nomenclatura|matr[ií]cula\s+catastral)[:\s]+([^\n,;]{5,60})",
        r"(?:apartamento|apto|casa|local|oficina|bodega)\s*(?:No\.?|N[uú]mero)?\s*\d+[^\n,;]{0,40}",
    ]
    for patron in patrones_nom:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            nomenclatura = m.group(1).strip() if m.lastindex else m.group(0).strip()
            nomenclatura = re.sub(r"\s+", " ", nomenclatura)
            break

    return direccion, nomenclatura


def _limpiar_nombre(nombre: str) -> str:
    nombre = re.sub(r"\s+", " ", nombre).strip()
    nombre = re.sub(r"[|,]+$", "", nombre).strip()
    return nombre


def _parsear_arrendadores(texto: str) -> Optional[str]:
    nombre_formulario = None
    cedula_formulario = None

    # Mejor fuente: sección de firma "EL ARRENDADOR\nNombre: XXX\nC.C.No.: XXX"
    m_firma = re.search(
        r"EL\s+ARRENDADOR\s*\n\s*Nombre[.:\s]*([^\n]{3,50})",
        texto, re.IGNORECASE,
    )
    if m_firma:
        nombre_formulario = _limpiar_nombre(m_firma.group(1))
        m_cc = re.search(r"C\.?C\.?\s*(?:No\.?)?\s*:?\s*([^\n]{3,20})", texto[m_firma.end():m_firma.end()+100])
        if m_cc:
            nums = re.findall(r"\d+", m_cc.group(1))
            if nums:
                cedula_formulario = "".join(nums)

    # Fallback: "Nombre del propietario del inmueble"
    if not nombre_formulario:
        m = re.search(
            r"[Nn]ombre\s+del\s+propietario\s+del\s+inmueble\s+([^\n]{3,60})",
            texto,
        )
        if m:
            nombre_formulario = _limpiar_nombre(m.group(1))

    # Fallback: "Nombre del Arrendador" del cuadro
    if not nombre_formulario:
        m = re.search(
            r"[Nn]ombre\s+del\s+[Aa]rrendador[:\s|>]*([^\n]{3,60})",
            texto,
        )
        if m:
            val = _limpiar_nombre(m.group(1))
            if val and len(val) > 2 and not re.match(r"^[\d\s|>]+$", val):
                nombre_formulario = val

    # Buscar identificación si no se encontró en firma
    if not cedula_formulario:
        m_id = re.search(
            r"[Cc][eé]dula\s+de\s+[Cc]iudadan[ií]a\s+No\.?\s*([^\n,]{3,20})",
            texto,
        )
        if m_id:
            nums = re.findall(r"\d+", m_id.group(1))
            if nums:
                cedula_formulario = "".join(nums)

    if nombre_formulario:
        if cedula_formulario:
            return f"{nombre_formulario} — CC {cedula_formulario}"
        return nombre_formulario

    # Patrón genérico ARRENDADOR
    patrones = [
        r"(?:EL\s+)?ARRENDADOR(?:\(A\))?[:\s]+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)(?:,?\s*(?:mayor|identificad|con\s+c[eé]dula|c\.?c\.?))",
        r"ARRENDADOR[:\s]*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)\s*(?:,\s*)?(?:identificad|con\s+c[eé]dula|c\.?c\.?)\s*(?:de\s+ciudadan[ií]a\s+)?(?:No\.?\s*)?(\d[\d.\s]+)",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            nombre = _limpiar_nombre(m.group(1))
            doc = re.sub(r"[\s.]", "", m.group(2)).strip() if m.lastindex >= 2 else ""
            if doc:
                return f"{nombre} — CC {doc}"
            return nombre

    # Patrón firma: "EL ARRENDADOR\nNombre: XXX\nC.C.No.: XXX"
    m = re.search(
        r"EL\s+ARRENDADOR\s*\n\s*Nombre[.:\s]*([^\n]{3,50})",
        texto, re.IGNORECASE,
    )
    if m:
        nombre = _limpiar_nombre(m.group(1))
        m_cc = re.search(r"C\.?C\.?\s*(?:No\.?)?\s*:?\s*(\d[\d\s.]+)", texto[m.end():m.end()+100])
        if m_cc:
            cc = re.sub(r"[\s.]", "", m_cc.group(1))
            return f"{nombre} — CC {cc}"
        return nombre

    return None


def _parsear_canon(texto: str) -> Optional[int]:
    # Patrón formulario: buscar "$X.XXX.XXX" cerca de "Valor" o "Canon"
    m = re.search(
        r"\$\s*([\d.,\s]+\d)",
        texto,
    )
    if m:
        valor_str = re.sub(r"[\s.,]", "", m.group(1))
        try:
            val = int(valor_str)
            if 100000 <= val <= 50000000:
                return val
        except ValueError:
            pass

    # Patrón texto: "un millón" / "dos millones" (tolerante a OCR)
    _PALABRAS_NUM = {
        "un": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    }
    m = re.search(
        r"(\w+)\s+mill[oó]n(?:es)?\s+de\s+pesos",
        texto, re.IGNORECASE,
    )
    if m:
        palabra = m.group(1).lower()
        if palabra in _PALABRAS_NUM:
            return _PALABRAS_NUM[palabra] * 1000000

    # OCR ruidoso: buscar "millón" con variantes OCR
    m = re.search(r"[Uu]n\s+m\w*\s+\w*\s+de\s+p", texto)
    if m:
        return 1000000

    # Buscar $(NÚMERO) o $NÚMERO con separadores
    m = re.search(r"\(\s*\$?\s*(\d[\d.,\s]*\d)\s*\)", texto)
    if not m:
        m = re.search(r"\$\s*\(?\s*(\d[\d.,\s]*\d)\s*\)?", texto)
    if m:
        valor_str = re.sub(r"[\s.,]", "", m.group(1))
        try:
            val = int(valor_str)
            if 100000 <= val <= 50000000:
                return val
        except ValueError:
            pass

    # Patrón con monto numérico
    patrones = [
        r"(?:canon\s+(?:de\s+arrendamiento\s+)?mensual|canon\s+mensual|valor\s+(?:del?\s+)?canon|renta\s+mensual)[:\s]*\$?\s*([\d.,\s]+\d)",
        r"(?:canon\s+(?:de\s+arrendamiento\s+)?mensual|canon\s+mensual|valor\s+(?:del?\s+)?canon|renta\s+mensual)[^\n]*?(?:\$|pesos)\s*([\d.,\s]+\d)",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            valor_str = re.sub(r"[\s.,]", "", m.group(1))
            try:
                valor = int(valor_str)
                if valor >= 100000:
                    return valor
            except ValueError:
                continue

    # Fallback: todos los montos con $
    montos = re.findall(r"\$\s*([\d.,\s]+\d)", texto)
    candidatos = []
    for monto_str in montos:
        limpio = re.sub(r"[\s.,]", "", monto_str)
        try:
            val = int(limpio)
            if 200000 <= val <= 20000000:
                candidatos.append(val)
        except ValueError:
            continue
    if candidatos:
        from collections import Counter
        conteo = Counter(candidatos)
        return conteo.most_common(1)[0][0]

    return None


def _ocr_pagina(page, dpi=300, contrast=1.5):
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    img = img.convert("L")
    img = img.filter(ImageFilter.SHARPEN)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    return pytesseract.image_to_string(img, lang="spa", config="--psm 6")


def _ocr_documento(ruta: str) -> str:
    doc = fitz.open(ruta)
    texto = ""
    for page in doc:
        texto += _ocr_pagina(page, dpi=300, contrast=1.5) + "\n"
    doc.close()
    return texto


def _ocr_multipasada_firma(ruta: str) -> dict:
    """Hace varias pasadas OCR en la última página (firmas) y la primera (formulario)
    para cruzar resultados del nombre y CC del arrendador."""
    doc = fitz.open(ruta)
    resultados = {"nombres": [], "cedulas": []}

    paginas_clave = [0, len(doc) - 1] if len(doc) > 1 else [0]
    configs = [(300, 1.5), (400, 1.8), (300, 1.0), (350, 1.3)]

    for page_idx in paginas_clave:
        page = doc[page_idx]
        for dpi, contrast in configs:
            text = _ocr_pagina(page, dpi, contrast)

            # Buscar nombre en firma
            m = re.search(
                r"EL\s+(?:_\s*)?ARRENDADOR\s*\n\s*Nombre[.:\s]*([^\n]{3,50})",
                text, re.IGNORECASE,
            )
            if m:
                resultados["nombres"].append(m.group(1).strip())

            # Buscar nombre propietario
            m = re.search(
                r"[Nn]ombre\s+del\s+propietario\s+del\s+inmueble\s+([^\n]{3,60})",
                text,
            )
            if m:
                resultados["nombres"].append(m.group(1).strip())

            # Buscar CC en firma
            m = re.search(
                r"EL\s+(?:_\s*)?ARRENDADOR\s*\n\s*Nombre[^\n]*\n\s*C\.?C\.?\s*(?:No\.?)?\s*:?\s*([^\n]{3,20})",
                text, re.IGNORECASE,
            )
            if m:
                resultados["cedulas"].append(m.group(1).strip())

            # Buscar CC en cuerpo
            m = re.search(
                r"[Cc][eé]dula\s+de\s+[Cc]iudadan[ií]a\s+No\.?\s*([^\n,]{3,20})",
                text,
            )
            if m:
                resultados["cedulas"].append(m.group(1).strip())

    doc.close()
    return resultados


def _mejor_nombre(nombres: list) -> Optional[str]:
    """Combina múltiples lecturas OCR del mismo nombre para reconstruirlo."""
    if not nombres:
        return None

    limpio = []
    for n in nombres:
        n = re.sub(r"[|>)(\d$:]+$", "", n).strip()
        n = re.sub(r"^[|>(]+", "", n).strip()
        # Limpiar caracteres no alfabéticos sueltos entre palabras
        partes = n.split()
        partes_limpias = []
        for p in partes:
            p = re.sub(r"[^A-Za-záéíóúñÁÉÍÓÚÑ]", "", p)
            if len(p) >= 2:
                partes_limpias.append(p)
        n = " ".join(partes_limpias)
        if len(n) > 3:
            limpio.append(n)

    if not limpio:
        return None

    # Combinar mejores palabras de todas las lecturas
    from collections import Counter
    todas_palabras_por_pos = {}
    for n in limpio:
        palabras = n.split()
        for i, p in enumerate(palabras):
            if i not in todas_palabras_por_pos:
                todas_palabras_por_pos[i] = []
            todas_palabras_por_pos[i].append(p)

    # Para cada posición, votar por la palabra más frecuente; si empate, la más larga
    resultado_partes = []
    for pos in sorted(todas_palabras_por_pos.keys()):
        palabras = todas_palabras_por_pos[pos]
        conteo = Counter(p.lower() for p in palabras)
        max_freq = conteo.most_common(1)[0][1]
        mas_frecuentes = [p for p in palabras if conteo[p.lower()] == max_freq]
        mas_frecuentes.sort(key=len, reverse=True)
        resultado_partes.append(mas_frecuentes[0])

    if resultado_partes:
        return " ".join(resultado_partes)

    return limpio[0] if limpio else None


def _mejor_cedula(cedulas: list) -> Optional[str]:
    """Extrae la cédula más consistente de múltiples lecturas OCR."""
    if not cedulas:
        return None

    extraidos = []
    for c in cedulas:
        # Limpiar texto después de "de " (nombre de ciudad)
        c = re.split(r"\s+de\s+", c)[0]
        # Reemplazar caracteres OCR comunes que confunden con dígitos
        c_limpio = c.replace("$", "5").replace("S", "5").replace("O", "0")
        c_limpio = c_limpio.replace("l", "1").replace("I", "1").replace("s", "5")
        nums = re.findall(r"\d+", c_limpio)
        if nums:
            joined = "".join(nums)
            if len(joined) >= 5:
                extraidos.append(joined)

    if not extraidos:
        return None

    # Votación: los primeros 2 dígitos más comunes
    from collections import Counter
    prefijos = Counter(e[:2] for e in extraidos if len(e) >= 2)
    mejor_prefijo = prefijos.most_common(1)[0][0]

    # Filtrar por mejor prefijo y tomar la más larga
    filtrados = [e for e in extraidos if e.startswith(mejor_prefijo)]
    if not filtrados:
        filtrados = extraidos
    filtrados.sort(key=len, reverse=True)
    return filtrados[0]


def _extraer_texto_docx(ruta: str) -> str:
    documento = docx.Document(ruta)
    parrafos = [p.text for p in documento.paragraphs if p.text.strip()]
    for tabla in documento.tables:
        for fila in tabla.rows:
            celdas = [c.text.strip() for c in fila.cells if c.text.strip()]
            if celdas:
                parrafos.append(" | ".join(celdas))
    return "\n".join(parrafos)


def analizar_contrato(ruta_pdf: str) -> AnalisisContrato:
    es_ocr = False
    texto = ""

    if ruta_pdf.lower().endswith((".docx", ".doc")):
        try:
            texto = _extraer_texto_docx(ruta_pdf)
        except Exception as e:
            return AnalisisContrato(error=f"No se pudo leer el documento Word: {e}")
    else:
        try:
            doc = fitz.open(ruta_pdf)
        except Exception as e:
            return AnalisisContrato(error=f"No se pudo abrir el archivo: {e}")

        for page in doc:
            texto += page.get_text() + "\n"
        doc.close()

        if not texto.strip():
            try:
                texto = _ocr_documento(ruta_pdf)
                es_ocr = True
            except Exception as e:
                return AnalisisContrato(error=f"No se pudo extraer texto (OCR falló): {e}")

    if not texto.strip():
        return AnalisisContrato(error="No se pudo extraer texto del documento")

    fecha = _parsear_fecha(texto)
    direccion, nomenclatura = _parsear_direccion(texto)
    arrendadores = _parsear_arrendadores(texto)
    canon = _parsear_canon(texto)

    # Para documentos escaneados, usar multi-pasada para mejorar nombre y CC
    if not arrendadores or (arrendadores and es_ocr):
        try:
            multi = _ocr_multipasada_firma(ruta_pdf)
            nombre_multi = _mejor_nombre(multi["nombres"])
            cedula_multi = _mejor_cedula(multi["cedulas"])
            if nombre_multi:
                if cedula_multi:
                    arrendadores = f"{nombre_multi} — CC {cedula_multi}"
                else:
                    arrendadores = nombre_multi
        except Exception:
            pass

    return AnalisisContrato(
        fecha_firma=fecha,
        direccion=direccion,
        nomenclatura=nomenclatura,
        arrendadores=arrendadores,
        canon_mensual=canon,
        texto_completo=texto,
    )
