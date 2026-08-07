"""Motor Claude Vision para extracción de datos de contratos manuscritos.

Envía las imágenes de las páginas clave (primera y última) a Claude
y le pide que extraiga los datos en JSON estructurado.

Requiere ANTHROPIC_API_KEY en variables de entorno.
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
from dataclasses import dataclass
from typing import Optional

import fitz
from PIL import Image


@dataclass
class ResultadoClaude:
    nombre_arrendador: Optional[str] = None
    cedula_arrendador: Optional[str] = None
    canon_mensual: Optional[int] = None
    fecha_inicio: Optional[str] = None
    tiene_firma_arrendador: Optional[bool] = None
    tiene_firma_arrendatario: Optional[bool] = None
    raw_response: str = ""


def esta_disponible() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def extraer_con_vision(ruta_pdf: str) -> Optional[ResultadoClaude]:
    if not esta_disponible():
        return None

    try:
        import anthropic
    except ImportError:
        return None

    imagenes = _paginas_a_base64(ruta_pdf, paginas=[0, -1], dpi=200, max_ancho=1200)
    if not imagenes:
        return None

    prompt = _construir_prompt()

    content = []
    for i, (b64, media_type) in enumerate(imagenes):
        content.append({
            "type": "text",
            "text": f"Página {i + 1} del contrato:",
        })
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": b64,
            },
        })
    content.append({"type": "text", "text": prompt})

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
    )

    texto_respuesta = response.content[0].text
    return _parsear_respuesta(texto_respuesta)


def _paginas_a_base64(
    ruta_pdf: str, paginas: list[int], dpi: int = 200, max_ancho: int = 1200,
) -> list[tuple[str, str]]:
    doc = fitz.open(ruta_pdf)
    resultado = []

    for idx in paginas:
        real_idx = idx if idx >= 0 else len(doc) + idx
        if real_idx < 0 or real_idx >= len(doc):
            continue

        pix = doc[real_idx].get_pixmap(dpi=dpi)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

        if img.width > max_ancho:
            ratio = max_ancho / img.width
            img = img.resize((max_ancho, int(img.height * ratio)), Image.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        b64 = base64.standard_b64encode(buffer.getvalue()).decode("utf-8")
        resultado.append((b64, "image/jpeg"))

    doc.close()
    return resultado


def _construir_prompt() -> str:
    return """Analiza este contrato de arrendamiento de vivienda urbana colombiano.
La primera imagen es la página 1 (datos del formulario) y la segunda es la última página (firmas).

Extrae EXACTAMENTE estos datos y devuelve SOLO un JSON sin texto adicional:

{
  "nombre_arrendador": "nombre completo tal como aparece escrito a mano",
  "cedula_arrendador": "solo dígitos, sin puntos ni espacios",
  "canon_mensual": 1000000,
  "fecha_inicio": "DD/MM/AAAA",
  "tiene_firma_arrendador": true,
  "tiene_firma_arrendatario": true
}

Instrucciones:
- El nombre del arrendador aparece en la tabla "DATOS DE LAS PARTES" y también en la sección de firma "EL ARRENDADOR".
- La cédula del arrendador aparece como "Identificación del arrendador" en la tabla y como "C.C. No." en la firma.
- El canon mensual aparece en la sección "VALOR" tanto en letras como en números. Usa el valor numérico.
- La fecha de inicio aparece como "Fecha de Inicio del Contrato" en la tabla VALOR.
- Para las firmas, verifica que haya trazos manuscritos (no solo texto impreso) en las secciones "EL ARRENDADOR" y "EL ARRENDATARIO".
- Si un campo no es legible, pon null.
- Para canon_mensual usa un número entero (sin decimales ni separadores).
- Responde SOLO con el JSON, sin explicaciones."""


def _parsear_respuesta(texto: str) -> ResultadoClaude:
    texto = texto.strip()
    m = re.search(r"\{[\s\S]*\}", texto)
    if not m:
        return ResultadoClaude(raw_response=texto)

    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return ResultadoClaude(raw_response=texto)

    canon = data.get("canon_mensual")
    if isinstance(canon, str):
        canon = int(re.sub(r"[^\d]", "", canon) or "0") or None

    fecha = data.get("fecha_inicio")
    if fecha and not re.match(r"\d{1,2}/\d{1,2}/\d{4}", str(fecha)):
        fecha = None

    return ResultadoClaude(
        nombre_arrendador=data.get("nombre_arrendador"),
        cedula_arrendador=_solo_digitos(data.get("cedula_arrendador")),
        canon_mensual=canon,
        fecha_inicio=fecha,
        tiene_firma_arrendador=data.get("tiene_firma_arrendador"),
        tiene_firma_arrendatario=data.get("tiene_firma_arrendatario"),
        raw_response=texto,
    )


def _solo_digitos(val: Optional[str]) -> Optional[str]:
    if not val:
        return None
    d = re.sub(r"[^\d]", "", str(val))
    return d if len(d) >= 5 else None
