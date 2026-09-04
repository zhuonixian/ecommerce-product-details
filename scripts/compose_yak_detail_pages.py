from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path("/workspace/scratch/9d2cf2528637")
OUT = ROOT / "output/imagegen/gannan-yak-beef-detail"
FONT_CN = ROOT / "tmp/fonts/SimSun-PDF-Unicode.ttf"
FONT_LATIN = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_LATIN_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
PRODUCT = ROOT / "tmp/imagegen/product-group-cutout.png"

BACKGROUNDS = [
    ROOT / "generated_images/exec-d26e32da-4917-4ece-9465-f382e578c30d.png",
    ROOT / "generated_images/exec-10779274-775a-440a-b6c0-a7db0697b06b.png",
    ROOT / "generated_images/exec-e96bda32-8228-4b57-839b-2f941d913501.png",
    ROOT / "generated_images/exec-44738c9d-be1f-426a-8164-188a4384abec.png",
    ROOT / "generated_images/exec-e29e0873-9c82-44db-afe1-f3632dd6a805.png",
    ROOT / "generated_images/exec-e3d9b483-24de-4524-8ff0-e6a8d06dc982.png",
]

W, H = 1080, 1920
OLIVE = (48, 61, 18)
OLIVE_DARK = (32, 41, 11)
CREAM = (248, 242, 220)
GOLD = (218, 183, 89)
BROWN = (63, 35, 20)
WHITE = (255, 255, 255)


def cn(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_CN), size)


def latin(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_LATIN_BOLD if bold else FONT_LATIN), size)


def cover(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    scale = max(W / image.width, H / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    image = image.resize(size, Image.Resampling.LANCZOS)
    left = (image.width - W) // 2
    top = (image.height - H) // 2
    return image.crop((left, top, left + W, top + H))


def rgba_layer() -> Image.Image:
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def add_top_gradient(image: Image.Image, height: int = 390, strength: int = 220) -> None:
    gradient = rgba_layer()
    pixels = gradient.load()
    for y in range(height):
        t = 1 - y / max(1, height - 1)
        alpha = round(strength * (t ** 1.6))
        for x in range(W):
            pixels[x, y] = (*OLIVE_DARK, alpha)
    image.alpha_composite(gradient)


def add_bottom_gradient(image: Image.Image, start: int, strength: int = 220) -> None:
    gradient = rgba_layer()
    pixels = gradient.load()
    span = H - start
    for y in range(start, H):
        t = (y - start) / max(1, span - 1)
        alpha = round(strength * (t ** 1.4))
        for x in range(W):
            pixels[x, y] = (*OLIVE_DARK, alpha)
    image.alpha_composite(gradient)


def text_center(draw: ImageDraw.ImageDraw, y: int, text: str, font, fill, stroke: int = 0, stroke_fill=None):
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    width = box[2] - box[0]
    draw.text(
        ((W - width) // 2, y),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke,
        stroke_fill=stroke_fill or fill,
    )


def page_number(draw: ImageDraw.ImageDraw, number: int) -> None:
    text = f"{number:02d} / 06"
    f = latin(24, bold=True)
    box = draw.textbbox((0, 0), text, font=f)
    draw.text((W - 58 - (box[2] - box[0]), 50), text, font=f, fill=GOLD)


def gold_rule(draw: ImageDraw.ImageDraw, y: int, width: int = 190) -> None:
    x = (W - width) // 2
    draw.rounded_rectangle((x, y, x + width, y + 5), radius=2, fill=GOLD)


def pill(draw: ImageDraw.ImageDraw, xy, text: str, font_size=30, dark=True, outline=False):
    x0, y0, x1, y1 = xy
    fill = (*OLIVE_DARK, 225) if dark else (*CREAM, 232)
    line = GOLD if outline else None
    draw.rounded_rectangle(xy, radius=(y1 - y0) // 2, fill=fill, outline=line, width=2)
    f = cn(font_size)
    box = draw.textbbox((0, 0), text, font=f)
    tx = x0 + ((x1 - x0) - (box[2] - box[0])) // 2
    ty = y0 + ((y1 - y0) - (box[3] - box[1])) // 2 - box[1]
    draw.text((tx, ty), text, font=f, fill=CREAM if dark else BROWN, stroke_width=1, stroke_fill=CREAM if dark else BROWN)


def paste_product(base: Image.Image, x: int, y: int, width: int, shadow_radius=22) -> tuple[int, int]:
    product = Image.open(PRODUCT).convert("RGBA")
    height = round(product.height * width / product.width)
    product = product.resize((width, height), Image.Resampling.LANCZOS)

    shadow_mask = product.getchannel("A").filter(ImageFilter.GaussianBlur(shadow_radius))
    shadow = Image.new("RGBA", product.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_mask.point(lambda value: round(value * 0.62)))
    shadow_layer = rgba_layer()
    shadow_layer.alpha_composite(shadow, (x + 14, y + 18))
    base.alpha_composite(shadow_layer)
    base.alpha_composite(product, (x, y))
    return width, height


def header(draw: ImageDraw.ImageDraw, number: int, title: str, subtitle: str, title_size=64):
    page_number(draw, number)
    text_center(draw, 62, title, cn(title_size), CREAM, stroke=1)
    text_center(draw, 148, subtitle, cn(30), GOLD)
    gold_rule(draw, 205)


def save(image: Image.Image, filename: str) -> None:
    image.convert("RGB").save(OUT / filename, quality=96)


def page_1() -> None:
    image = cover(BACKGROUNDS[0])
    add_top_gradient(image, 460, 235)
    add_bottom_gradient(image, 1700, 235)
    draw = ImageDraw.Draw(image, "RGBA")
    page_number(draw, 1)
    draw.text((66, 62), "高原甄选", font=cn(30), fill=GOLD, stroke_width=1, stroke_fill=GOLD)
    draw.text((62, 118), "甘南风干牦牛肉干", font=cn(72), fill=CREAM, stroke_width=2, stroke_fill=OLIVE_DARK)
    draw.rounded_rectangle((64, 226, 458, 284), radius=29, fill=(*OLIVE_DARK, 188), outline=GOLD, width=2)
    draw.text((92, 237), "雪域高原的自然风味", font=cn(28), fill=CREAM)

    paste_product(image, 365, 1162, 680, shadow_radius=20)

    features = [(55, 1760, 335, 1840, "精选后腿肉"), (400, 1760, 680, 1840, "传统风干"), (745, 1760, 1025, 1840, "紧实有嚼劲")]
    for x0, y0, x1, y1, label in features:
        pill(draw, (x0, y0, x1, y1), label, font_size=27, dark=True, outline=True)
    save(image, "01-商品首屏.png")


def page_2() -> None:
    image = cover(BACKGROUNDS[1])
    add_top_gradient(image, 400, 225)
    add_bottom_gradient(image, 1500, 235)
    draw = ImageDraw.Draw(image, "RGBA")
    header(draw, 2, "源自甘南高原", "源自海拔3000米以上雪域高原", 66)
    pill(draw, (60, 930, 430, 1002), "逐水草游牧", 29, dark=True, outline=True)
    pill(draw, (650, 930, 1020, 1002), "饮雪山融水", 29, dark=True, outline=True)
    draw.rounded_rectangle((58, 1635, 1022, 1840), radius=28, fill=(*OLIVE_DARK, 218), outline=GOLD, width=2)
    draw.text((94, 1676), "甄选牦牛后腿肉", font=cn(50), fill=CREAM, stroke_width=1, stroke_fill=CREAM)
    draw.text((96, 1750), "肉质高蛋白、低脂肪", font=cn(30), fill=GOLD)
    save(image, "02-产地与原料.png")


def process_label(draw, y: int, number: str, title: str, detail: str) -> None:
    draw.rounded_rectangle((42, y, 480, y + 112), radius=18, fill=(*OLIVE_DARK, 208), outline=GOLD, width=2)
    draw.ellipse((60, y + 21, 126, y + 87), fill=GOLD)
    nf = latin(26, bold=True)
    box = draw.textbbox((0, 0), number, font=nf)
    draw.text((93 - (box[2] - box[0]) // 2, y + 37), number, font=nf, fill=OLIVE_DARK)
    draw.text((150, y + 17), title, font=cn(34), fill=CREAM, stroke_width=1, stroke_fill=CREAM)
    draw.text((150, y + 65), detail, font=cn(23), fill=GOLD)


def page_3() -> None:
    image = cover(BACKGROUNDS[2])
    draw = ImageDraw.Draw(image, "RGBA")
    page_number(draw, 3)
    draw.text((54, 39), "传统工艺", font=cn(54), fill=CREAM, stroke_width=1, stroke_fill=CREAM)
    draw.text((320, 61), "从原料到成品的风味过程", font=cn(26), fill=GOLD)
    process_label(draw, 176, "01", "精切成条", "甄选后腿肉")
    process_label(draw, 638, "02", "传统腌制", "充分入味")
    process_label(draw, 1100, "03", "自然风干", "保留肉香")
    process_label(draw, 1547, "04", "手撕成型", "纹理清晰")
    save(image, "03-加工工艺.png")


def feature_card(draw, center_x: int, y: int, title: str, detail: str) -> None:
    title_font = cn(42)
    detail_font = cn(25)
    title_box = draw.textbbox((0, 0), title, font=title_font)
    detail_box = draw.textbbox((0, 0), detail, font=detail_font)
    draw.text((center_x - (title_box[2] - title_box[0]) // 2, y), title, font=title_font, fill=BROWN, stroke_width=1, stroke_fill=BROWN)
    draw.text((center_x - (detail_box[2] - detail_box[0]) // 2, y + 70), detail, font=detail_font, fill=OLIVE)
    draw.rounded_rectangle((center_x - 42, y + 125, center_x + 42, y + 129), radius=2, fill=GOLD)


def page_4() -> None:
    image = cover(BACKGROUNDS[3])
    add_top_gradient(image, 340, 225)
    draw = ImageDraw.Draw(image, "RGBA")
    header(draw, 4, "肉质纹理", "紧实有嚼劲  越嚼越香", 66)
    feature_card(draw, 286, 1035, "肉质紧实", "口感扎实有嚼劲")
    feature_card(draw, 797, 1035, "纹理清晰", "手撕纤维 清晰可见")
    feature_card(draw, 286, 1480, "咸香入味", "传统腌制 风味醇厚")
    feature_card(draw, 797, 1480, "越嚼越香", "膻味较轻 香气自然")
    save(image, "04-细节与口感.png")


def row(draw, y: int, label: str, value: str, value_size=30) -> None:
    draw.text((92, y), label, font=cn(28), fill=OLIVE_DARK, stroke_width=1, stroke_fill=OLIVE_DARK)
    draw.text((330, y - 2), value, font=cn(value_size), fill=BROWN)


def page_5() -> None:
    image = cover(BACKGROUNDS[4])
    draw = ImageDraw.Draw(image, "RGBA")
    page_number(draw, 5)
    draw.text((56, 38), "产品规格", font=cn(56), fill=CREAM, stroke_width=1, stroke_fill=CREAM)
    draw.text((330, 63), "PRODUCT DETAILS", font=latin(24, bold=True), fill=GOLD)
    paste_product(image, 178, 455, 724, shadow_radius=18)

    rows = [
        (880, "产品名称", "甘南风干牦牛肉干", 30),
        (1007, "产品类别", "零食/肉干", 30),
        (1134, "规格", "250g/袋", 32),
        (1285, "口味", "麻辣 / 五香", 32),
        (1412, "核心原料", "甘南牦牛后腿肉", 30),
        (1539, "营养特点", "高蛋白 / 低脂肪", 30),
    ]
    for args in rows:
        row(draw, *args)

    note = "具体配料、营养成分、生产日期、保质期及保存条件，以实物包装为准。"
    text_center(draw, 1770, note, cn(23), CREAM)
    save(image, "05-规格与营养.png")


def scene_label(draw, box, title: str, detail: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=(*OLIVE_DARK, 212), outline=GOLD, width=2)
    draw.text((x0 + 22, y0 + 13), title, font=cn(31), fill=CREAM, stroke_width=1, stroke_fill=CREAM)
    draw.text((x0 + 22, y0 + 58), detail, font=cn(22), fill=GOLD)


def page_6() -> None:
    image = cover(BACKGROUNDS[5])
    draw = ImageDraw.Draw(image, "RGBA")
    page_number(draw, 6)
    text_center(draw, 62, "随时随地 解馋补给", cn(64), CREAM, stroke=1)
    text_center(draw, 155, "休闲  |  办公  |  旅途  |  馈赠", cn(28), GOLD)
    gold_rule(draw, 214)

    scene_label(draw, (46, 1020, 478, 1122), "追剧游戏", "休闲解馋")
    scene_label(draw, (602, 1020, 1034, 1122), "办公加餐", "轻松补充")
    scene_label(draw, (46, 1781, 478, 1883), "旅途补给", "便携易食")
    scene_label(draw, (602, 1781, 1034, 1883), "节日馈赠", "分享高原风味")
    save(image, "06-食用场景.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for path in [*BACKGROUNDS, FONT_CN, PRODUCT]:
        if not path.exists():
            raise FileNotFoundError(path)

    page_1()
    page_2()
    page_3()
    page_4()
    page_5()
    page_6()
    print(f"wrote 6 pages to {OUT}")


if __name__ == "__main__":
    main()
