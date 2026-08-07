"""Registro de plantillas de contratos y definición de ROIs.

Las coordenadas están normalizadas [0.0, 1.0] respecto al ancho/alto de la
página preprocesada, para que funcionen independientemente del DPI.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import numpy as np


class TipoCampo(str, Enum):
    TEXTO_MANUSCRITO = "texto_manuscrito"
    NUMERO = "numero"
    CHECKBOX = "checkbox"
    FECHA = "fecha"
    EMAIL = "email"


@dataclass
class ROI:
    nombre: str
    campo_path: str
    tipo: TipoCampo
    x: float
    y: float
    w: float
    h: float
    pagina: int = 0


@dataclass
class PlantillaContrato:
    nombre: str
    version: str
    rois: list[ROI] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Minuta estándar de arrendamiento de vivienda urbana
# Coordenadas normalizadas estimadas de la foto del contrato escaneado
# ---------------------------------------------------------------------------

MINUTA_ESTANDAR = PlantillaContrato(
    nombre="minuta_arrendamiento_vivienda_urbana",
    version="1.0",
    rois=[
        # === PÁGINA 0: DATOS DE LAS PARTES ===
        ROI("nombre_arrendador", "arrendador.nombre",
            TipoCampo.TEXTO_MANUSCRITO, 0.42, 0.065, 0.55, 0.025, pagina=0),
        ROI("cedula_arrendador", "arrendador.cedula",
            TipoCampo.NUMERO, 0.42, 0.090, 0.35, 0.025, pagina=0),
        ROI("nombre_arrendatario", "arrendatario.nombre",
            TipoCampo.TEXTO_MANUSCRITO, 0.42, 0.145, 0.55, 0.025, pagina=0),
        ROI("cedula_arrendatario", "arrendatario.cedula",
            TipoCampo.NUMERO, 0.42, 0.170, 0.35, 0.025, pagina=0),

        # === PÁGINA 0: DATOS DEL INMUEBLE ===
        ROI("direccion_inmueble", "inmueble.direccion",
            TipoCampo.TEXTO_MANUSCRITO, 0.42, 0.225, 0.55, 0.025, pagina=0),
        ROI("barrio", "inmueble.barrio",
            TipoCampo.TEXTO_MANUSCRITO, 0.42, 0.250, 0.55, 0.025, pagina=0),
        ROI("ciudad_inmueble", "inmueble.ciudad",
            TipoCampo.TEXTO_MANUSCRITO, 0.20, 0.280, 0.35, 0.025, pagina=0),

        # Checkboxes propiedad horizontal
        ROI("ph_si", "inmueble.propiedad_horizontal",
            TipoCampo.CHECKBOX, 0.60, 0.300, 0.06, 0.020, pagina=0),

        # Checkboxes servicios
        ROI("agua_si", "inmueble.servicios.agua",
            TipoCampo.CHECKBOX, 0.26, 0.325, 0.06, 0.020, pagina=0),
        ROI("gas_si", "inmueble.servicios.gas",
            TipoCampo.CHECKBOX, 0.62, 0.325, 0.06, 0.020, pagina=0),
        ROI("energia_si", "inmueble.servicios.energia",
            TipoCampo.CHECKBOX, 0.26, 0.350, 0.06, 0.020, pagina=0),
        ROI("telefono_si", "inmueble.servicios.telefono",
            TipoCampo.CHECKBOX, 0.62, 0.350, 0.06, 0.020, pagina=0),
        ROI("internet_si", "inmueble.servicios.internet",
            TipoCampo.CHECKBOX, 0.26, 0.375, 0.06, 0.020, pagina=0),

        # === PÁGINA 0: VALOR ===
        ROI("canon_letras", "financiero.canon_letras",
            TipoCampo.TEXTO_MANUSCRITO, 0.20, 0.415, 0.77, 0.025, pagina=0),
        ROI("fecha_inicio", "vigencia.fecha_inicio",
            TipoCampo.FECHA, 0.55, 0.440, 0.40, 0.025, pagina=0),
        ROI("fecha_terminacion", "vigencia.fecha_terminacion",
            TipoCampo.FECHA, 0.55, 0.462, 0.40, 0.025, pagina=0),

        # Admin checkbox
        ROI("admin_incluida", "financiero.admin_incluida",
            TipoCampo.CHECKBOX, 0.60, 0.485, 0.20, 0.020, pagina=0),

        # Cuenta bancaria
        ROI("nombre_propietario_cuenta", "financiero.nombre_propietario_cuenta",
            TipoCampo.TEXTO_MANUSCRITO, 0.55, 0.505, 0.42, 0.025, pagina=0),
        ROI("tipo_cuenta", "financiero.tipo_cuenta",
            TipoCampo.CHECKBOX, 0.20, 0.530, 0.50, 0.020, pagina=0),
        ROI("numero_cuenta", "financiero.numero_cuenta",
            TipoCampo.NUMERO, 0.20, 0.550, 0.40, 0.025, pagina=0),
        ROI("banco", "financiero.banco",
            TipoCampo.TEXTO_MANUSCRITO, 0.35, 0.575, 0.40, 0.025, pagina=0),

        # === PÁGINA 2: VIGENCIA ===
        ROI("vigencia_meses", "vigencia.vigencia_meses",
            TipoCampo.NUMERO, 0.65, 0.310, 0.10, 0.030, pagina=2),

        # === ÚLTIMA PÁGINA: FIRMAS ARRENDADOR ===
        ROI("firma_nombre_arrendador", "arrendador.nombre",
            TipoCampo.TEXTO_MANUSCRITO, 0.15, 0.315, 0.45, 0.025, pagina=-1),
        ROI("firma_cc_arrendador", "arrendador.cedula",
            TipoCampo.NUMERO, 0.15, 0.340, 0.35, 0.025, pagina=-1),
        ROI("firma_ciudad_arrendador", "arrendador.ciudad",
            TipoCampo.TEXTO_MANUSCRITO, 0.15, 0.405, 0.30, 0.025, pagina=-1),
        ROI("firma_celular_arrendador", "arrendador.celular",
            TipoCampo.NUMERO, 0.15, 0.425, 0.35, 0.025, pagina=-1),
        ROI("firma_email_arrendador", "arrendador.email",
            TipoCampo.EMAIL, 0.15, 0.445, 0.50, 0.025, pagina=-1),

        # === ÚLTIMA PÁGINA: FIRMAS ARRENDATARIO ===
        ROI("firma_nombre_arrendatario", "arrendatario.nombre",
            TipoCampo.TEXTO_MANUSCRITO, 0.15, 0.630, 0.45, 0.025, pagina=-1),
        ROI("firma_cc_arrendatario", "arrendatario.cedula",
            TipoCampo.NUMERO, 0.15, 0.655, 0.35, 0.025, pagina=-1),
        ROI("firma_ciudad_arrendatario", "arrendatario.ciudad",
            TipoCampo.TEXTO_MANUSCRITO, 0.15, 0.720, 0.30, 0.025, pagina=-1),
        ROI("firma_celular_arrendatario", "arrendatario.celular",
            TipoCampo.NUMERO, 0.15, 0.740, 0.35, 0.025, pagina=-1),
        ROI("firma_email_arrendatario", "arrendatario.email",
            TipoCampo.EMAIL, 0.15, 0.760, 0.50, 0.025, pagina=-1),
    ],
)


def detectar_plantilla(imagenes: list[np.ndarray]) -> Optional[PlantillaContrato]:
    """Detecta qué plantilla corresponde al documento.

    Por ahora solo soportamos la minuta estándar. En el futuro se puede
    comparar contra múltiples plantillas usando template matching.
    """
    if not imagenes:
        return None
    return MINUTA_ESTANDAR


def recortar_roi(imagen: np.ndarray, roi: ROI) -> np.ndarray:
    """Recorta una región de interés de la imagen, con margen de seguridad."""
    h_img, w_img = imagen.shape[:2]

    margen_x = roi.w * 0.05
    margen_y = roi.h * 0.15

    x0 = max(0, int((roi.x - margen_x) * w_img))
    y0 = max(0, int((roi.y - margen_y) * h_img))
    x1 = min(w_img, int((roi.x + roi.w + margen_x) * w_img))
    y1 = min(h_img, int((roi.y + roi.h + margen_y) * h_img))

    if x1 <= x0 or y1 <= y0:
        return imagen

    return imagen[y0:y1, x0:x1]
