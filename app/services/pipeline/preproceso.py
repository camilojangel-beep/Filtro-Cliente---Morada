"""Preprocesamiento de imágenes de contratos escaneados.

Pipeline: PDF → páginas PNG → recorte de hoja → deskew → contraste → binarización.
"""
from __future__ import annotations

import io
from typing import Optional

import cv2
import fitz
import numpy as np
from PIL import Image


def pdf_a_imagenes(ruta_pdf: str, dpi: int = 300) -> list[np.ndarray]:
    doc = fitz.open(ruta_pdf)
    imagenes = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        imagenes.append(np.array(img.convert("RGB")))
    doc.close()
    return imagenes


def preprocesar(img: np.ndarray) -> np.ndarray:
    recortada = _recortar_hoja(img)
    enderezada = _deskew(recortada)
    gris = cv2.cvtColor(enderezada, cv2.COLOR_RGB2GRAY)
    mejorada = _mejorar_contraste(gris)
    return mejorada


def _recortar_hoja(img: np.ndarray) -> np.ndarray:
    """Detecta los bordes de la hoja blanca y recorta el fondo (mesa/escritorio)."""
    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return img

    mayor = max(contornos, key=cv2.contourArea)
    area_img = img.shape[0] * img.shape[1]

    if cv2.contourArea(mayor) < area_img * 0.3:
        return img

    epsilon = 0.02 * cv2.arcLength(mayor, True)
    approx = cv2.approxPolyDP(mayor, epsilon, True)

    if len(approx) == 4:
        corregida = _corregir_perspectiva(img, approx)
        if corregida is not None:
            return corregida

    x, y, w, h = cv2.boundingRect(mayor)
    margen = 10
    x = max(0, x - margen)
    y = max(0, y - margen)
    w = min(img.shape[1] - x, w + 2 * margen)
    h = min(img.shape[0] - y, h + 2 * margen)
    return img[y:y+h, x:x+w]


def _corregir_perspectiva(img: np.ndarray, pts: np.ndarray) -> Optional[np.ndarray]:
    """Corrección de perspectiva dado un cuadrilátero de 4 puntos."""
    pts = pts.reshape(4, 2).astype(np.float32)

    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()
    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(d)]
    bl = pts[np.argmax(d)]

    w1 = np.linalg.norm(br - bl)
    w2 = np.linalg.norm(tr - tl)
    ancho = int(max(w1, w2))

    h1 = np.linalg.norm(tr - br)
    h2 = np.linalg.norm(tl - bl)
    alto = int(max(h1, h2))

    if ancho < 200 or alto < 200:
        return None

    src = np.array([tl, tr, br, bl], dtype=np.float32)
    dst = np.array([[0, 0], [ancho, 0], [ancho, alto], [0, alto]], dtype=np.float32)

    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, M, (ancho, alto))


def _deskew(img: np.ndarray) -> np.ndarray:
    """Corrige inclinación menor usando detección de líneas."""
    if len(img.shape) == 3:
        gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gris = img.copy()

    bordes = cv2.Canny(gris, 50, 150, apertureSize=3)
    lineas = cv2.HoughLinesP(bordes, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if lineas is None or len(lineas) < 3:
        return img

    angulos = []
    for linea in lineas:
        x1, y1, x2, y2 = linea[0]
        angulo = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angulo) < 15:
            angulos.append(angulo)

    if not angulos:
        return img

    angulo_mediana = float(np.median(angulos))

    if abs(angulo_mediana) < 0.3:
        return img

    h, w = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo_mediana, 1.0)
    rotada = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotada


def _mejorar_contraste(gris: np.ndarray) -> np.ndarray:
    """CLAHE + binarización adaptativa para texto manuscrito sobre fondo impreso."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    mejorada = clahe.apply(gris)
    return mejorada


def binarizar(gris: np.ndarray) -> np.ndarray:
    """Binarización adaptativa — útil para checkboxes y separar tinta de plantilla."""
    return cv2.adaptiveThreshold(
        gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10,
    )
