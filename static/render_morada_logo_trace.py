from PIL import Image, ImageDraw, ImageFont


SCALE = 4
WIDTH, HEIGHT = 1200 * SCALE, 900 * SCALE
BG = "#f7f5fb"
WHITE = "#ffffff"
PRIMARY = "#4b2c92"
ACCENT = "#8f39ff"
TEXT = "#2a1c4f"
SUBTLE = "#6f6786"
PANEL = "#ece8f5"

ARIAL_ROUNDED = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
TREBUCHET = "/System/Library/Fonts/Supplemental/Trebuchet MS.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=size * SCALE)


F_TITLE = font(ARIAL_ROUNDED, 26)
F_SUB = font(TREBUCHET, 15)
F_MORADA = font(ARIAL_ROUNDED, 74)
F_CAPITAL = font(TREBUCHET, 32)
F_LABEL = font(TREBUCHET, 18)


def pt(x, y):
    return (x * SCALE, y * SCALE)


def qbez(p0, p1, p2, n=20):
    points = []
    for i in range(n + 1):
        t = i / n
        x = ((1 - t) ** 2) * p0[0] + 2 * (1 - t) * t * p1[0] + (t**2) * p2[0]
        y = ((1 - t) ** 2) * p0[1] + 2 * (1 - t) * t * p1[1] + (t**2) * p2[1]
        points.append((x, y))
    return points


def centered(draw, text, cx, y, font_obj, fill):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), text, font=font_obj, fill=fill)


def spaced(draw, text, cx, y, font_obj, fill, spacing):
    widths = [draw.textbbox((0, 0), ch, font=font_obj)[2] for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for idx, ch in enumerate(text):
        draw.text((x, y), ch, font=font_obj, fill=fill)
        x += widths[idx] + spacing


def draw_logo_icon(draw, cx, cy, color):
    stroke = 12 * SCALE

    roof_left = [
        pt(cx, cy - 130),
        pt(cx - 58, cy - 74),
        pt(cx - 100, cy - 34),
    ]
    wall_left = [pt(cx - 100, cy - 34), pt(cx - 100, cy + 46)]
    lobe_left = qbez(pt(cx - 100, cy + 46), pt(cx - 100, cy + 84), pt(cx - 74, cy + 100), n=18)
    toe_left = qbez(pt(cx - 74, cy + 100), pt(cx - 48, cy + 112), pt(cx - 26, cy + 92), n=16)

    roof_right = [
        pt(cx, cy - 130),
        pt(cx + 58, cy - 74),
        pt(cx + 100, cy - 34),
    ]
    wall_right = [pt(cx + 100, cy - 34), pt(cx + 100, cy + 46)]
    lobe_right = qbez(pt(cx + 100, cy + 46), pt(cx + 100, cy + 84), pt(cx + 74, cy + 100), n=18)
    toe_right = qbez(pt(cx + 74, cy + 100), pt(cx + 48, cy + 112), pt(cx + 26, cy + 92), n=16)

    left_path = roof_left + wall_left[1:] + lobe_left[1:] + toe_left[1:]
    right_path = roof_right + wall_right[1:] + lobe_right[1:] + toe_right[1:]
    draw.line(left_path, fill=color, width=stroke, joint="curve")
    draw.line(right_path, fill=color, width=stroke, joint="curve")

    inner_stroke = 10 * SCALE
    left_inner = [pt(cx - 54, cy + 2), pt(cx - 54, cy + 60)]
    left_diag = [pt(cx - 54, cy + 4), pt(cx - 20, cy + 38)]
    right_inner = [pt(cx + 54, cy + 2), pt(cx + 54, cy + 60)]
    right_diag = [pt(cx + 54, cy + 4), pt(cx + 20, cy + 38)]
    cross_left = [pt(cx - 12, cy + 58), pt(cx - 34, cy + 80)]
    cross_right = [pt(cx + 12, cy + 58), pt(cx + 34, cy + 80)]

    for segment in (left_inner, left_diag, right_inner, right_diag, cross_left, cross_right):
        draw.line(segment, fill=color, width=inner_stroke, joint="curve")


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((pt(28, 28), pt(1172, 872)), radius=28 * SCALE, fill=WHITE)
    draw.text(pt(76, 62), "Copia trazada desde la referencia anexada", font=F_TITLE, fill=TEXT)
    draw.text(
        pt(76, 95),
        "No es un logo nuevo: es una reconstruccion visual para validar si corresponde al existente.",
        font=F_SUB,
        fill=SUBTLE,
    )

    draw.rounded_rectangle((pt(76, 136), pt(1124, 734)), radius=24 * SCALE, outline=PANEL, width=2 * SCALE, fill=WHITE)

    draw_logo_icon(draw, 600, 300, PRIMARY)
    centered(draw, "Morada", 600 * SCALE, 470 * SCALE, F_MORADA, PRIMARY)
    spaced(draw, "Capital", 600 * SCALE, 585 * SCALE, F_CAPITAL, ACCENT, 12 * SCALE)

    draw.text(pt(120, 774), 'Texto de marca detectado: "Morada"', font=F_LABEL, fill=TEXT)
    draw.text(pt(620, 774), 'Subtitulo detectado: "Capital"', font=F_LABEL, fill=TEXT)
    draw.text(pt(120, 808), "Si esta silueta ya coincide, de aqui saco la version final limpia.", font=F_SUB, fill=SUBTLE)

    img = img.resize((1200, 900), Image.Resampling.LANCZOS)
    img.save("static/morada_logo_trace_preview.png")


if __name__ == "__main__":
    main()
