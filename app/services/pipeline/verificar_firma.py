"""Verificación de firma en contratos de arrendamiento escaneados.

Detecta si hay firmas manuscritas en la última página del documento
analizando densidad de trazos en las zonas donde se esperan las firmas.
"""
from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Optional

import cv2
import fitz
import numpy as np
from PIL import Image


@dataclass
class ResultadoFirma:
    tiene_firma_arrendador: bool = False
    tiene_firma_arrendatario: bool = False
    confianza_arrendador: float = 0.0
    confianza_arrendatario: float = 0.0
    ambas_firmadas: bool = False


def verificar_firmas(ruta_pdf: str) -> ResultadoFirma:
    if not ruta_pdf.lower().endswith(".pdf"):
        return _verificar_por_texto(ruta_pdf)

    doc = fitz.open(ruta_pdf)
    if len(doc) == 0:
        doc.close()
        return ResultadoFirma()

    ultima = doc[-1]
    tiene_texto = bool(ultima.get_text().strip())

    if tiene_texto:
        texto = ultima.get_text()
        doc.close()
        return _analizar_texto_firma(texto)

    pix = ultima.get_pixmap(dpi=200)
    img = np.array(Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"))
    doc.close()

    return _analizar_imagen_firma(img)


def _verificar_por_texto(ruta: str) -> ResultadoFirma:
    """Para DOCX u otros formatos con texto, busca indicadores de firma."""
    try:
        import docx
        documento = docx.Document(ruta)
        texto = "\n".join(p.text for p in documento.paragraphs)
    except Exception:
        return ResultadoFirma()
    return _analizar_texto_firma(texto)


def _analizar_texto_firma(texto: str) -> ResultadoFirma:
    """Busca secciones de firma en texto extraído."""
    import re

    texto_lower = texto.lower()

    tiene_seccion_arrendador = bool(re.search(
        r"el\s+arrendador\s*\n\s*nombre", texto, re.IGNORECASE,
    ))
    tiene_seccion_arrendatario = bool(re.search(
        r"el\s+arrendatario\s*\n\s*nombre", texto, re.IGNORECASE,
    ))

    tiene_firma_arr = tiene_seccion_arrendador and bool(re.search(
        r"el\s+arrendador[\s\S]{0,300}firma", texto, re.IGNORECASE,
    ))
    tiene_firma_arrt = tiene_seccion_arrendatario and bool(re.search(
        r"el\s+arrendatario[\s\S]{0,300}firma", texto, re.IGNORECASE,
    ))

    conf_arr = 0.80 if tiene_firma_arr else (0.50 if tiene_seccion_arrendador else 0.0)
    conf_arrt = 0.80 if tiene_firma_arrt else (0.50 if tiene_seccion_arrendatario else 0.0)

    return ResultadoFirma(
        tiene_firma_arrendador=tiene_firma_arr,
        tiene_firma_arrendatario=tiene_firma_arrt,
        confianza_arrendador=conf_arr,
        confianza_arrendatario=conf_arrt,
        ambas_firmadas=tiene_firma_arr and tiene_firma_arrt,
    )


def _analizar_imagen_firma(img: np.ndarray) -> ResultadoFirma:
    """Detecta firmas manuscritas por densidad de trazos en zonas esperadas."""
    h, w = img.shape[:2]

    mitad_inferior = img[h // 3:, :]
    h2, w2 = mitad_inferior.shape[:2]

    zona_arrendador = mitad_inferior[:h2 // 2, :w2 // 2]
    zona_arrendatario = mitad_inferior[h2 // 2:, :w2 // 2]

    dens_arr = _densidad_trazos_manuscritos(zona_arrendador)
    dens_arrt = _densidad_trazos_manuscritos(zona_arrendatario)

    umbral_firma = 0.008
    tiene_arr = dens_arr > umbral_firma
    tiene_arrt = dens_arrt > umbral_firma

    conf_arr = min(1.0, dens_arr / 0.03) if tiene_arr else dens_arr / umbral_firma * 0.4
    conf_arrt = min(1.0, dens_arrt / 0.03) if tiene_arrt else dens_arrt / umbral_firma * 0.4

    return ResultadoFirma(
        tiene_firma_arrendador=tiene_arr,
        tiene_firma_arrendatario=tiene_arrt,
        confianza_arrendador=round(conf_arr, 3),
        confianza_arrendatario=round(conf_arrt, 3),
        ambas_firmadas=tiene_arr and tiene_arrt,
    )


def _densidad_trazos_manuscritos(zona: np.ndarray) -> float:
    """Calcula la densidad de trazos tipo firma (líneas curvas oscuras)."""
    if zona.size == 0:
        return 0.0

    gris = cv2.cvtColor(zona, cv2.COLOR_RGB2GRAY) if len(zona.shape) == 3 else zona

    blur = cv2.GaussianBlur(gris, (3, 3), 0)
    _, binaria = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel_texto = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    sin_texto = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel_texto)
    solo_firma = binaria - sin_texto

    contornos, _ = cv2.findContours(solo_firma, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    area_firma = 0
    for c in contornos:
        area = cv2.contourArea(c)
        _, _, cw, ch = cv2.boundingRect(c)
        if area > 50 and cw > 20 and ch > 5:
            area_firma += area

    return area_firma / zona.size if zona.size > 0 else 0.0
