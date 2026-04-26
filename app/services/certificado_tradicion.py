import re
import tempfile
from datetime import date, datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import httpx
import fitz


@dataclass
class DatosCompraventa:
    numero_anotacion: int
    fecha: str
    comprador: str
    identificacion_comprador: str
    valor_acto: str
    especificacion: str


@dataclass
class AnalisisCTL:
    pin: str
    matricula: str
    oficina_registro: str
    fecha_expedicion: str
    nomenclatura: str
    direcciones: List[str]
    area_construida: Optional[str]
    area_privada: Optional[str]
    coeficiente: Optional[str]
    ultima_compraventa: Optional[DatosCompraventa]
    tiene_embargo: bool
    detalle_embargos: List[str]
    total_anotaciones: int
    texto_completo: str = ""
    error: Optional[str] = None


_WATERMARK = (
    "SUPERINTENDENCIA DE NOTARIADO Y REGISTRO LA GUARDA DE LA FE PUBLICA"
)


def _limpiar_texto(texto: str) -> str:
    lineas = texto.split("\n")
    limpias = []
    for linea in lineas:
        if _WATERMARK in linea:
            continue
        if linea.strip().startswith("OFICINA DE REGISTRO DE INSTRUMENTOS"):
            continue
        if linea.strip() == "CERTIFICADO DE TRADICION":
            continue
        if linea.strip() == "MATRICULA INMOBILIARIA":
            continue
        limpias.append(linea)
    return "\n".join(limpias)


def _extraer_cabida_linderos(texto: str) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
    match = re.search(
        r"DESCRIPCION:\s*CABIDA Y LINDEROS\s*\n(.+?)(?=\nAREA Y COEFICIENTE|\nCOMPLEMENTACION:|\nDIRECCION)",
        texto, re.DOTALL,
    )
    nomenclatura = match.group(1).strip() if match else ""

    area_construida = None
    area_privada = None
    coeficiente = None

    m = re.search(r"A\.CONSTRUIDA:\s*([\d.,]+)\s*MTS2", texto)
    if m:
        area_construida = m.group(1)

    m = re.search(r"A\.PRIVADA:\s*([\d.,]+)\s*MTS2", texto)
    if m:
        area_privada = m.group(1)

    m = re.search(r"COEFICIENTE\s*(?:DE)?\s*([\d.,]+)\s*%", texto)
    if m:
        coeficiente = m.group(1)

    return nomenclatura, area_construida, area_privada, coeficiente


def _extraer_direcciones(texto: str) -> List[str]:
    seccion = re.search(
        r"DIRECCION DEL INMUEBLE.*?(?=DETERMINACION|MATRICULA ABIERTA|\n\n)",
        texto, re.DOTALL,
    )
    if not seccion:
        return []
    bloque = seccion.group(0)
    direcciones = []
    for m in re.finditer(r"\d+\)\s*(.+)", bloque):
        d = m.group(1).strip()
        d = re.sub(r"\s*\(DIRECCION CATASTRAL\)", "", d)
        if d and d not in direcciones:
            direcciones.append(d)
    return direcciones


def _parsear_anotaciones(texto: str) -> list:
    bloques = re.split(r"(?=ANOTACION:\s*Nro\s+\d+)", texto)
    anotaciones = []
    for bloque in bloques:
        m_head = re.match(
            r"ANOTACION:\s*Nro\s+(\d+)\s+Fecha:\s+([\d-]+)",
            bloque,
        )
        if not m_head:
            continue

        numero = int(m_head.group(1))
        fecha = m_head.group(2)

        m_valor = re.search(r"VALOR ACTO:\s*\$\s*([\d.,]*)", bloque)
        valor = m_valor.group(1).strip() if m_valor else ""

        m_esp = re.search(r"ESPECIFICACION:\s*(.+?)(?=\nPERSONAS QUE|\Z)", bloque, re.DOTALL)
        especificacion = " ".join(m_esp.group(1).split()) if m_esp else ""

        compradores = []
        for m_a in re.finditer(
            r"^A:\s*(.+)$",
            bloque, re.MULTILINE,
        ):
            nombre = m_a.group(1).strip()
            resto = bloque[m_a.end():]
            m_id = re.match(r"\s*(CC#|NIT#?|CE#)\s*([\d.\-]+)", resto)
            tipo_id = m_id.group(1) if m_id else ""
            num_id = m_id.group(2) if m_id else ""
            compradores.append((nombre, tipo_id, num_id))

        anotaciones.append({
            "numero": numero,
            "fecha": fecha,
            "valor": valor,
            "especificacion": especificacion,
            "compradores": compradores,
            "texto_completo": bloque,
        })
    return anotaciones


def consultar_pin_snr(pin: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        resp = client.get(
            "https://certificados.supernotariado.gov.co/certificado/external/validation/validate.snr"
        )
        cookies = resp.cookies

        m_vs = re.search(
            r'name="javax\.faces\.ViewState"[^>]*value="([^"]+)"',
            resp.text,
        )
        if not m_vs:
            return None, None, None, "No se pudo obtener ViewState del sitio SNR"
        viewstate = m_vs.group(1)

        data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formValidation:j_idt42",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "formValidation modalInformacionCertificado modalInformacionCertificadoAnterior",
            "formValidation:j_idt42": "formValidation:j_idt42",
            "formValidation": "formValidation",
            "formValidation:j_idt41": pin,
            "javax.faces.ViewState": viewstate,
        }

        resp2 = client.post(
            "https://certificados.supernotariado.gov.co/certificado/external/validation/validate.snr",
            data=data,
            headers={
                "Faces-Request": "partial/ajax",
                "X-Requested-With": "XMLHttpRequest",
            },
            cookies=cookies,
        )

        body = resp2.text

        if "no ha sido encontrado" in body:
            return None, None, None, f"Certificado con PIN {pin} no encontrado en el sistema SNR"

        m_mat = re.search(r"Matricula</span></td>\s*<td><span[^>]*>([^<]+)</span>", body)
        matricula = m_mat.group(1) if m_mat else ""

        m_of = re.search(r"Oficina de Registro</span></td>\s*<td><span[^>]*>([^<]+)</span>", body)
        oficina = m_of.group(1) if m_of else ""

        m_pdf = re.search(r'href="(/certificado/static/fileDispatcher/[^"]+\.pdf)"', body)
        if not m_pdf:
            return matricula, oficina, None, "No se encontró enlace de descarga del PDF"

        pdf_path = m_pdf.group(1)
        pdf_url = f"https://certificados.supernotariado.gov.co{pdf_path}"

        resp_pdf = client.get(pdf_url, cookies=cookies)
        if resp_pdf.status_code != 200:
            return matricula, oficina, None, f"Error descargando PDF: HTTP {resp_pdf.status_code}"

        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.write(resp_pdf.content)
        tmp.flush()

        return matricula, oficina, tmp.name, None


def analizar_certificado(pin: str) -> AnalisisCTL:
    matricula, oficina, pdf_path, error = consultar_pin_snr(pin)

    if error:
        return AnalisisCTL(
            pin=pin, matricula=matricula or "", oficina_registro=oficina or "",
            fecha_expedicion="", nomenclatura="", direcciones=[], area_construida=None,
            area_privada=None, coeficiente=None, ultima_compraventa=None,
            tiene_embargo=False, detalle_embargos=[], total_anotaciones=0, error=error,
        )

    doc = fitz.open(pdf_path)
    texto_completo = ""
    for page in doc:
        texto_completo += page.get_text() + "\n"
    doc.close()

    texto = _limpiar_texto(texto_completo)

    m_fecha = re.search(r"Impreso el (.+?)(?:\n|$)", texto)
    fecha_expedicion = m_fecha.group(1).strip() if m_fecha else ""

    nomenclatura, area_construida, area_privada, coeficiente = _extraer_cabida_linderos(texto)
    direcciones = _extraer_direcciones(texto)
    anotaciones = _parsear_anotaciones(texto)

    total_anotaciones = len(anotaciones)

    ultima_compraventa = None
    for anot in reversed(anotaciones):
        if "COMPRAVENTA" in anot["especificacion"].upper():
            comprador_nombre = ""
            comprador_id = ""
            if anot["compradores"]:
                c = anot["compradores"][0]
                comprador_nombre = c[0]
                comprador_id = f"{c[1]} {c[2]}".strip()
            ultima_compraventa = DatosCompraventa(
                numero_anotacion=anot["numero"],
                fecha=anot["fecha"],
                comprador=comprador_nombre,
                identificacion_comprador=comprador_id,
                valor_acto=anot["valor"] if anot["valor"] else "No registrado",
                especificacion=anot["especificacion"],
            )
            break

    fecha_limite = date.today() - timedelta(days=730)
    embargos = []
    for anot in anotaciones:
        if "EMBARGO" in anot["especificacion"].upper():
            try:
                fecha_anot = datetime.strptime(anot["fecha"], "%d-%m-%Y").date()
            except ValueError:
                fecha_anot = date.today()
            if fecha_anot >= fecha_limite:
                embargos.append(
                    f"Anotación {anot['numero']} ({anot['fecha']}): {anot['especificacion']}"
                )

    return AnalisisCTL(
        pin=pin,
        matricula=f"50N-{matricula}" if matricula and not matricula.startswith("50N") else (matricula or ""),
        oficina_registro=oficina or "",
        fecha_expedicion=fecha_expedicion,
        nomenclatura=nomenclatura,
        direcciones=direcciones,
        area_construida=area_construida,
        area_privada=area_privada,
        coeficiente=coeficiente,
        ultima_compraventa=ultima_compraventa,
        tiene_embargo=len(embargos) > 0,
        detalle_embargos=embargos,
        total_anotaciones=total_anotaciones,
        texto_completo=texto,
    )
