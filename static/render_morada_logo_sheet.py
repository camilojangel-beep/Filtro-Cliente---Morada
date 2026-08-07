from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1800, 1400
BG = "#f7f5fb"
WHITE = "#ffffff"
PANEL = "#ece8f5"
PRIMARY = "#4a2a8b"
ACCENT = "#8d38ff"
TEXT = "#241742"
SUBTLE = "#6d6680"
MUTED = "#817a94"
SOFT = "#f6f1ff"

ARIAL_ROUNDED = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
TREBUCHET = "/System/Library/Fonts/Supplemental/Trebuchet MS.ttf"


def font(path, size):
    return ImageFont.truetype(path, size=size)


F_TITLE = font(ARIAL_ROUNDED, 48)
F_SUBTITLE = font(TREBUCHET, 22)
F_SECTION = font(ARIAL_ROUNDED, 28)
F_LABEL = font(TREBUCHET, 22)
F_SMALL = font(TREBUCHET, 18)
F_MORADA = font(ARIAL_ROUNDED, 96)
F_CAPITAL = font(TREBUCHET, 42)
F_LETTERS_MAIN = font(ARIAL_ROUNDED, 66)
F_LETTERS_SUB = font(TREBUCHET, 40)
F_CHIP = font(TREBUCHET, 18)


def centered_text(draw, text, center_x, y, font_obj, fill):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    w = bbox[2] - bbox[0]
    draw.text((center_x - w / 2, y), text, font=font_obj, fill=fill)


def draw_spaced_text(draw, text, x, y, font_obj, fill, spacing):
    cursor = x
    for i, ch in enumerate(text):
        draw.text((cursor, y), ch, font=font_obj, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font_obj)
        cursor += (bbox[2] - bbox[0]) + spacing


def draw_logo_icon(draw, x, y, scale=1.0, variant="a", stroke=PRIMARY, background=None):
    sw = int(14 * scale)
    lw = int(13 * scale)
    if background:
        draw.ellipse((x - 85 * scale, y - 85 * scale, x + 85 * scale, y + 85 * scale), fill=background)

    if variant == "a":
        outer = [
            (x, y - 118 * scale),
            (x + 76 * scale, y - 44 * scale),
            (x + 92 * scale, y - 28 * scale),
            (x + 92 * scale, y + 42 * scale),
            (x + 92 * scale, y + 76 * scale),
            (x + 70 * scale, y + 98 * scale),
            (x + 36 * scale, y + 94 * scale),
            (x + 12 * scale, y + 70 * scale),
        ]
        outer2 = [
            (x, y - 118 * scale),
            (x - 76 * scale, y - 44 * scale),
            (x - 92 * scale, y - 28 * scale),
            (x - 92 * scale, y + 42 * scale),
            (x - 92 * scale, y + 76 * scale),
            (x - 70 * scale, y + 98 * scale),
            (x - 36 * scale, y + 94 * scale),
            (x - 12 * scale, y + 70 * scale),
        ]
    elif variant == "b":
        outer = [
            (x, y - 118 * scale),
            (x + 82 * scale, y - 40 * scale),
            (x + 96 * scale, y - 24 * scale),
            (x + 96 * scale, y + 42 * scale),
            (x + 96 * scale, y + 72 * scale),
            (x + 74 * scale, y + 96 * scale),
            (x + 40 * scale, y + 92 * scale),
            (x + 10 * scale, y + 68 * scale),
        ]
        outer2 = [
            (x, y - 118 * scale),
            (x - 82 * scale, y - 40 * scale),
            (x - 96 * scale, y - 24 * scale),
            (x - 96 * scale, y + 42 * scale),
            (x - 96 * scale, y + 72 * scale),
            (x - 74 * scale, y + 96 * scale),
            (x - 40 * scale, y + 92 * scale),
            (x - 10 * scale, y + 68 * scale),
        ]
    else:
        outer = [
            (x, y - 116 * scale),
            (x + 78 * scale, y - 42 * scale),
            (x + 98 * scale, y - 22 * scale),
            (x + 98 * scale, y + 48 * scale),
            (x + 98 * scale, y + 80 * scale),
            (x + 72 * scale, y + 102 * scale),
            (x + 34 * scale, y + 98 * scale),
            (x + 8 * scale, y + 72 * scale),
        ]
        outer2 = [
            (x, y - 116 * scale),
            (x - 78 * scale, y - 42 * scale),
            (x - 98 * scale, y - 22 * scale),
            (x - 98 * scale, y + 48 * scale),
            (x - 98 * scale, y + 80 * scale),
            (x - 72 * scale, y + 102 * scale),
            (x - 34 * scale, y + 98 * scale),
            (x - 8 * scale, y + 72 * scale),
        ]
        sw = int(15 * scale)
        lw = int(15 * scale)

    draw.line(outer, fill=stroke, width=sw, joint="curve")
    draw.line(outer2, fill=stroke, width=sw, joint="curve")
    draw.line(
        [(x - 52 * scale, y + 14 * scale), (x - 52 * scale, y + 72 * scale)],
        fill=stroke,
        width=lw,
    )
    draw.line(
        [(x + 52 * scale, y + 14 * scale), (x + 52 * scale, y + 72 * scale)],
        fill=stroke,
        width=lw,
    )
    draw.line(
        [(x - 52 * scale, y + 14 * scale), (x - 18 * scale, y + 48 * scale)],
        fill=stroke,
        width=lw,
    )
    draw.line(
        [(x + 52 * scale, y + 14 * scale), (x + 18 * scale, y + 48 * scale)],
        fill=stroke,
        width=lw,
    )


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((40, 40, 1760, 1360), radius=36, fill=WHITE)
    draw.text((110, 90), "Morada - reconstruccion preliminar del logo", font=F_TITLE, fill=TEXT)
    draw.text(
        (110, 145),
        "Lamina comparativa para validar isotipo, wordmark y letras antes de entregarlo a Claude.",
        font=F_SUBTITLE,
        fill=SUBTLE,
    )

    panels = [(110, 235, 610, 875), (650, 235, 1150, 875), (1190, 235, 1690, 875)]
    versions = [
        ("Version A", "Trazo mas cercano a la silueta del ejemplo", "a", "principal"),
        ("Version B", "Techo un poco mas abierto y centro mas ligero", "b", "abierta"),
        ("Version C", "M interna mas marcada y bases mas redondas", "c", "gruesa"),
    ]

    for (x1, y1, x2, y2), (title, subtitle, variant, chip) in zip(panels, versions):
        draw.rounded_rectangle((x1, y1, x2, y2), radius=28, fill=WHITE, outline=PANEL, width=2)
        draw.text((x1 + 40, y1 + 38), title, font=F_SECTION, fill=PRIMARY)
        draw.text((x1 + 40, y1 + 76), subtitle, font=F_SMALL, fill=MUTED)

        center_x = (x1 + x2) / 2
        draw_logo_icon(draw, center_x, y1 + 245, scale=1.0, variant=variant)
        centered_text(draw, "Morada", center_x, y1 + 470, F_MORADA, PRIMARY)
        draw_spaced_text(draw, "Capital", center_x - 80, y1 + 560, F_CAPITAL, ACCENT, 15)

        chip_x1 = x1 + 48
        chip_y1 = y1 + 570
        chip_x2 = chip_x1 + (140 if chip == "principal" else 130 if chip == "abierta" else 120)
        chip_y2 = chip_y1 + 36
        draw.rounded_rectangle((chip_x1, chip_y1, chip_x2, chip_y2), radius=18, fill=SOFT)
        draw.text((chip_x1 + 22, chip_y1 + 8), chip, font=F_CHIP, fill=PRIMARY)

    draw.rounded_rectangle((110, 930, 1690, 1260), radius=28, fill=WHITE, outline=PANEL, width=2)
    draw.text((150, 972), "Letras sugeridas para el logo", font=F_SECTION, fill=PRIMARY)
    draw.text(
        (150, 1012),
        'Referencia del brand board: palabra principal "Morada", subtitulo "Capital" y tipografia objetivo "Rubik Medium".',
        font=F_SUBTITLE,
        fill=SUBTLE,
    )
    draw.text((150, 1085), "Palabra principal", font=F_LABEL, fill="#4a4657")
    draw.text((150, 1140), "M o r a d a", font=F_LETTERS_MAIN, fill=PRIMARY)
    draw.text((880, 1085), "Subtitulo", font=F_LABEL, fill="#4a4657")
    draw_spaced_text(draw, "Capital", 880, 1145, F_LETTERS_SUB, ACCENT, 10)
    draw.text((150, 1210), "Color morado base aproximado: #4A2A8B", font=F_SMALL, fill=MUTED)
    draw.text((880, 1210), "Morado acento aproximado: #8D38FF", font=F_SMALL, fill=MUTED)

    draw_logo_icon(draw, 1588, 1092, scale=0.48, variant="a", stroke=WHITE, background=PRIMARY)
    draw.text(
        (150, 1310),
        "Objetivo de esta lamina: escoger la forma correcta del isotipo antes de sacar una version final mas fiel para entregar.",
        font=F_SMALL,
        fill=MUTED,
    )

    image.save("static/morada_logo_sheet.png")


if __name__ == "__main__":
    main()
