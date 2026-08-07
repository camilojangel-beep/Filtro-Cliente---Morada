"""Motor Tesseract mejorado: preproceso + per-ROI OCR + post-limpieza por tipo."""
from __future__ import annotations

import re
from typing import Optional

import cv2
import numpy as np
import pytesseract
from PIL import Image

from app.services.pipeline.template_registry import ROI, TipoCampo


def ocr_roi(crop: np.ndarray, roi: ROI) -> str:
    """Ejecuta OCR optimizado según el tipo de campo."""
    if roi.tipo == TipoCampo.CHECKBOX:
        return _detectar_marca(crop)

    psm = _psm_para_tipo(roi.tipo)
    config = f"--psm {psm}"
    if roi.tipo == TipoCampo.NUMERO:
        config += " -c tessedit_char_whitelist=0123456789"

    preparada = _preparar_para_ocr(crop, roi.tipo)

    texto = pytesseract.image_to_string(
        Image.fromarray(preparada), lang="spa", config=config,
    ).strip()

    return _limpiar_resultado(texto, roi.tipo)


def ocr_pagina_completa(img_gris: np.ndarray) -> str:
    return pytesseract.image_to_string(
        Image.fromarray(img_gris), lang="spa", config="--psm 6",
    )


def _psm_para_tipo(tipo: TipoCampo) -> int:
    if tipo == TipoCampo.NUMERO:
        return 7
    if tipo in (TipoCampo.EMAIL, TipoCampo.FECHA):
        return 7
    return 6


def _preparar_para_ocr(crop: np.ndarray, tipo: TipoCampo) -> np.ndarray:
    if len(crop.shape) == 3:
        gris = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    else:
        gris = crop.copy()

    h, w = gris.shape
    if w < 200:
        factor = max(2, 400 // w)
        gris = cv2.resize(gris, (w * factor, h * factor), interpolation=cv2.INTER_CUBIC)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
    gris = clahe.apply(gris)

    if tipo == TipoCampo.NUMERO:
        gris = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)
    else:
        gris = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)

    kernel = np.ones((2, 2), np.uint8)
    gris = cv2.morphologyEx(gris, cv2.MORPH_CLOSE, kernel)

    return gris


def _detectar_marca(crop: np.ndarray) -> str:
    """Detecta si hay una marca X en un checkbox usando densidad de tinta."""
    if len(crop.shape) == 3:
        gris = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    else:
        gris = crop.copy()

    _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    pixeles_tinta = np.count_nonzero(binaria)
    total = binaria.size
    densidad = pixeles_tinta / total if total > 0 else 0

    if densidad > 0.15:
        return "True"
    return "False"


def _limpiar_resultado(texto: str, tipo: TipoCampo) -> str:
    texto = texto.strip()
    texto = re.sub(r"\s+", " ", texto)

    if tipo == TipoCampo.NUMERO:
        texto = re.sub(r"[^\d]", "", texto)
    elif tipo == TipoCampo.EMAIL:
        texto = texto.replace(" ", "").replace("©", "@").replace("®", "@")
        texto = texto.replace("(2)", "@").replace("()", "@").replace("(@)", "@")
    elif tipo == TipoCampo.FECHA:
        texto = re.sub(r"[|_]+", "", texto).strip()

    return texto
