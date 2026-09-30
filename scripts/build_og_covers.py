# -*- coding: utf-8 -*-
"""Build OG cover images in resume visual language (system fonts)."""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AVATAR_SRC = r"C:\Users\Лидия\Yandex.Disk\Резюме\mialkina-lv-00.jpg"
AVATAR_FALLBACK = os.path.join(ROOT, "avatar.jpg")

PAPER = (249, 249, 249)
WHITE = (255, 255, 255)
INK = (26, 28, 31)
MUTED = (92, 86, 104)
CHIP_BG = (243, 245, 247)
CHIP_TEXT = (75, 85, 99)
LIME_SOFT = (240, 250, 208)
LIME = (221, 253, 44)
BLUE = (91, 159, 208)
PEACH = (255, 179, 115)
VIOLET = (92, 92, 238)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEMIBOLD = r"C:\Windows\Fonts\seguisb.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"


def load_font(size: int, weight: int = 500) -> ImageFont.FreeTypeFont:
    path = FONT_REG
    if weight >= 700:
        path = FONT_BOLD
    elif weight >= 600:
        path = FONT_SEMIBOLD
    return ImageFont.truetype(path, size)


def soft_blob(size: tuple[int, int], color: tuple[int, int, int], alpha: int) -> Image.Image:
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = size
    d.ellipse((0, 0, w - 1, h - 1), fill=(*color, alpha))
    return layer.filter(ImageFilter.GaussianBlur(radius=min(w, h) // 5))


def make_avatar(size: int) -> Image.Image:
    src_path = AVATAR_SRC if os.path.exists(AVATAR_SRC) else AVATAR_FALLBACK
    src = Image.open(src_path).convert("RGB")
    w, h = src.size
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, (h - side) // 2 - int(side * 0.04))
    z = int(side * 0.94)
    left += (side - z) // 2
    top += int((side - z) * 0.10)
    crop = src.crop((left, top, left + z, top + z)).resize((size, size), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out.paste(crop, (0, 0), mask)
    return out


def draw_chip(base: Image.Image, xy, text: str, font, bg, fg, pad_x=18, pad_y=11, radius=12):
    draw = ImageDraw.Draw(base)
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w, h = tw + pad_x * 2, th + pad_y * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=bg)
    ty = y + (h - th) / 2 - bbox[1]
    draw.text((x + pad_x, ty), text, font=font, fill=fg)
    return w, h


def build_cover(lang: str) -> Image.Image:
    W, H = 1200, 630
    canvas = Image.new("RGBA", (W, H), (*PAPER, 255))
    canvas.alpha_composite(soft_blob((920, 520), LIME, 90), (-120, -180))
    canvas.alpha_composite(soft_blob((780, 460), PEACH, 95), (620, -80))
    canvas.alpha_composite(soft_blob((700, 420), BLUE, 55), (780, 280))
    canvas.alpha_composite(soft_blob((640, 360), VIOLET, 35), (40, 320))

    margin_x, margin_y = 72, 78
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (margin_x + 6, margin_y + 12, W - margin_x + 6, H - margin_y + 12),
        radius=28,
        fill=(26, 28, 31, 22),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))

    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle(
        (margin_x, margin_y, W - margin_x, H - margin_y), radius=28, fill=(*WHITE, 255)
    )
    canvas.alpha_composite(card)

    avatar_size = 248
    avatar = make_avatar(avatar_size)
    ax = margin_x + 56
    ay = (H - avatar_size) // 2
    canvas.alpha_composite(avatar, (ax, ay))

    if lang == "ru":
        kicker = "CV · Product"
        name = "Лидия Мялкина"
        role = "Продакт-менеджер · UX/UI · vibe-coding"
        chips = [("UX/UI · Figma · AI", True), ("BEANABOX · ТурГений", False)]
    else:
        kicker = "CV · Product"
        name = "Lidiia Mialkina"
        role = "Product manager · UX/UI · vibe-coding"
        chips = [("UX/UI · Figma · AI", True), ("BEANABOX · TourGenius", False)]

    font_kicker = load_font(22, 600)
    font_name = load_font(54, 600)
    font_role = load_font(28, 500)
    font_chip = load_font(20, 500)

    text_x = ax + avatar_size + 48
    text_top = ay + 22
    draw = ImageDraw.Draw(canvas)
    draw.text((text_x, text_top), kicker, font=font_kicker, fill=MUTED)
    name_y = text_top + 38
    draw.text((text_x, name_y), name, font=font_name, fill=INK)
    role_y = name_y + 74
    draw.text((text_x, role_y), role, font=font_role, fill=MUTED)

    chip_y = role_y + 54
    chip_x = text_x
    for label, accent in chips:
        bg = LIME_SOFT if accent else CHIP_BG
        fg = INK if accent else CHIP_TEXT
        cw, _ = draw_chip(canvas, (chip_x, chip_y), label, font_chip, bg, fg)
        chip_x += cw + 12

    return canvas.convert("RGB")


def main() -> None:
    for lang, name in (("ru", "og-cover-ru.jpg"), ("en", "og-cover-en.jpg")):
        img = build_cover(lang)
        out = os.path.join(ROOT, name)
        img.save(out, "JPEG", quality=92, optimize=True, progressive=True)
        print("wrote", out, os.path.getsize(out))


if __name__ == "__main__":
    main()
