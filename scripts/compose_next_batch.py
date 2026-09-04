from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import math
import shutil
import zipfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from fontTools.ttLib import TTFont


ROOT = Path("/workspace/scratch/9d2cf2528637")
OUT_ROOT = ROOT / "output/imagegen/next-batch"
FONT_CN = ROOT / "tmp/fonts/SimSun-PDF-Unicode.ttf"
FONT_LATIN = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_LATIN_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

W, H = 1080, 1920
WHITE = (255, 255, 255)


PRODUCTS = [
    {
        "key": "taosu",
        "dir": "qingke-taosu-detail",
        "name": "青稞桃酥",
        "eyebrow": "高原青稞烘焙",
        "tagline": "高原青稞 / 酥香松脆",
        "product_image": ROOT / "tmp/pdfs/extracted-images/img-002.png",
        "hero": ROOT / "generated_images/exec-afb5646a-80e3-4b96-9a8c-185a1e852602.png",
        "process": ROOT / "generated_images/exec-002a4d59-cf1b-4d7b-aeda-6474d71bea4e.png",
        "scene": ROOT / "generated_images/exec-97a4bb40-ae72-47ed-8994-f85d1ffc38dc.png",
        "dark": (45, 56, 15),
        "dark2": (25, 34, 8),
        "accent": (228, 188, 78),
        "cream": (249, 242, 218),
        "ink": (75, 43, 20),
        "badges": ["高原青稞", "现代烘焙", "酥松谷香"],
        "source_title": "高原青稞 原料之选",
        "source_subtitle": "来自青藏高原的谷物风味",
        "source_statement": ["甄选高原青稞", "谷物本香 融入烘焙"],
        "source_features": [("高原青稞", "谷物香气"), ("现代工艺", "烘焙成型"), ("双味可选", "原味 / 微麻")],
        "process_steps": [("青稞甄选", "原粮清理"), ("精制成粉", "细粉处理"), ("和面成型", "桃酥定型"), ("烘焙完成", "酥香成型")],
        "detail_title": "酥松纹理 品味好滋味",
        "detail_subtitle": "从外观到口感 层层展开",
        "detail_features": [("酥松质地", "入口松化"), ("青稞谷香", "烘焙香气"), ("颗粒表面", "纹理自然"), ("双味可选", "原味 / 微麻")],
        "spec_rows": [("产品类别", "零食 / 饼干"), ("产品规格", "180g / 盒"), ("口味选择", "原味 / 微麻"), ("产品特色", "高原青稞 / 桃酥风味"), ("食用方式", "开袋即食")],
        "nutrition_title": "营养成分说明",
        "nutrition_body": ["膳食纤维等营养资料", "请以实物营养成分表为准"],
        "scene_title": "多种场合 随时分享",
        "scene_subtitle": "居家 / 办公 / 家庭 / 伴手礼",
        "scenes": [("居家茶点", "搭配香茶"), ("办公加餐", "片刻酥香"), ("家庭分享", "一起品尝"), ("伴手礼赠", "分享高原风味")],
    },
    {
        "key": "lowgi",
        "dir": "qingke-lowgi-biscuit-detail",
        "name": "青稞低GI无糖饼干",
        "eyebrow": "高原青稞饼干",
        "tagline": "独立小包装 / 谷香酥脆",
        "product_image": ROOT / "tmp/pdfs/extracted-images/img-000.png",
        "hero": ROOT / "generated_images/exec-e4148d66-8644-426e-b586-409ab9c506ff.png",
        "process": ROOT / "generated_images/exec-ff497fcb-ad8e-4139-9498-d79852ab1c89.png",
        "scene": ROOT / "generated_images/exec-79800009-24f3-465e-bb4a-2fcdaa7a79b1.png",
        "dark": (0, 56, 72),
        "dark2": (0, 31, 43),
        "accent": (224, 188, 84),
        "cream": (247, 242, 221),
        "ink": (34, 55, 56),
        "badges": ["低GI标注", "无糖标注", "独立包装"],
        "source_title": "高原青稞 谷物本香",
        "source_subtitle": "原味饼干 清爽酥脆",
        "source_statement": ["高原青稞打底", "谷香清爽 口感酥脆"],
        "source_features": [("高原青稞", "谷物风味"), ("独立小袋", "轻便易带"), ("包装资料", "以实物为准")],
        "process_steps": [("青稞甄选", "挑选原粮"), ("精制粉料", "细腻均匀"), ("压片成型", "规整饼片"), ("低温烘焙", "谷香酥脆")],
        "detail_title": "方形饼体 谷香酥脆",
        "detail_subtitle": "独立包装 方便随身携带",
        "detail_features": [("方形饼体", "规整易取"), ("谷香酥脆", "原味清爽"), ("独立小袋", "携带方便"), ("原味配方", "风味纯粹")],
        "spec_rows": [("产品类别", "零食 / 饼干"), ("产品规格", "16g × 12 / 盒"), ("口味选择", "原味"), ("包装方式", "独立小包装"), ("产品标注", "低GI / 无糖")],
        "nutrition_title": "标注资料",
        "nutrition_body": ["低GI、无糖等产品标注", "以实物包装及检测材料为准"],
        "scene_title": "轻便随身 日常好搭配",
        "scene_subtitle": "早餐 / 办公 / 旅途 / 户外",
        "scenes": [("早餐搭配", "牛奶与饼干"), ("办公加餐", "独立小袋"), ("旅途携带", "轻便易带"), ("户外片刻", "随手分享")],
    },
    {
        "key": "yakmilk",
        "dir": "yakmilk-qingke-biscuit-detail",
        "name": "牦牛乳青稞饼干",
        "eyebrow": "高原风味烘焙",
        "tagline": "牦牛乳风味 / 青稞谷香",
        "product_image": ROOT / "tmp/pdfs/extracted-images/img-001.png",
        "hero": ROOT / "generated_images/exec-cde15095-5e83-410b-92b6-0ca47294be3e.png",
        "process": ROOT / "generated_images/exec-fbced9d0-3e68-427d-9c01-d4a51c6379f9.png",
        "scene": ROOT / "generated_images/exec-32574e76-5c83-4ccc-9b7a-d13b006fc414.png",
        "dark": (0, 59, 66),
        "dark2": (0, 33, 39),
        "accent": (225, 189, 88),
        "cream": (248, 243, 224),
        "ink": (28, 57, 56),
        "badges": ["高原青稞", "牦牛乳风味", "独立包装"],
        "source_title": "青稞与牦牛乳 风味相融",
        "source_subtitle": "高原食材灵感 融入烘焙",
        "source_statement": ["青稞与牦牛乳风味", "融合出层次口感"],
        "source_features": [("高原青稞", "自然谷香"), ("牦牛乳风味", "奶香柔和"), ("低温烘焙", "酥脆成型")],
        "process_steps": [("原料准备", "青稞与牦牛乳"), ("均匀混合", "充分调和"), ("压片成型", "饼片定型"), ("低温烘焙", "酥脆完成")],
        "detail_title": "奶香谷香 层次相融",
        "detail_subtitle": "酥脆不腻 独立小包装",
        "detail_features": [("奶香融合", "层次柔和"), ("青稞谷香", "自然烘焙"), ("酥脆口感", "不易腻口"), ("独立小袋", "随取随享")],
        "spec_rows": [("产品类别", "零食 / 饼干"), ("产品规格", "16g × 12 / 盒"), ("口味选择", "原味"), ("产品特色", "青稞 / 牦牛乳风味"), ("包装方式", "独立小包装")],
        "nutrition_title": "配料与营养说明",
        "nutrition_body": ["牦牛乳、青稞等具体添加量", "以实物配料表和包装为准"],
        "scene_title": "早餐加餐 轻松分享",
        "scene_subtitle": "早餐 / 办公 / 旅途 / 家庭",
        "scenes": [("早餐时光", "搭配牛奶"), ("办公加餐", "酥脆相伴"), ("旅途补给", "方便携带"), ("家庭分享", "一起品尝")],
    },
    {
        "key": "milktea",
        "dir": "qingke-milktea-detail",
        "name": "青稞奶茶",
        "eyebrow": "高原谷物冲饮",
        "tagline": "高原青稞谷香 / 暖意冲饮",
        "product_image": ROOT / "tmp/pdfs/extracted-images/img-009.png",
        "hero": ROOT / "generated_images/exec-d85ef9b1-2d14-474c-a99e-51f5dde82470.png",
        "process": ROOT / "generated_images/exec-80349b58-17c4-4125-8008-db7b78a401e4.png",
        "scene": ROOT / "generated_images/exec-b0de3e60-d85a-4687-8e3c-537a8c593b7f.png",
        "dark": (61, 30, 17),
        "dark2": (36, 18, 10),
        "accent": (220, 174, 99),
        "cream": (250, 241, 218),
        "ink": (82, 46, 27),
        "badges": ["青稞谷香", "原味咸味", "温暖冲饮"],
        "source_title": "高原青稞 融入奶茶",
        "source_subtitle": "谷物香气与奶茶风味交融",
        "source_statement": ["高原青稞谷香", "融入温润奶茶"],
        "source_features": [("高原青稞", "谷物香气"), ("双味选择", "原味 / 咸味"), ("袋装规格", "家庭分享")],
        "process_steps": [("青稞甄选", "清理原粮"), ("烘焙提香", "激发谷香"), ("细制调配", "均匀混合"), ("分装封口", "便捷冲饮")],
        "detail_title": "谷香奶香 温润相融",
        "detail_subtitle": "原味与咸味 两种风味选择",
        "detail_features": [("谷香奶香", "风味融合"), ("温暖冲泡", "香气舒展"), ("原味可选", "口感温润"), ("咸味可选", "风味有层次")],
        "spec_rows": [("产品类别", "饮料 / 奶茶"), ("产品规格", "460g / 袋"), ("口味选择", "原味 / 咸味"), ("食用方式", "冲调饮用"), ("产品特色", "青稞谷香 / 奶茶风味")],
        "nutrition_title": "冲调与包装说明",
        "nutrition_body": ["冲调方法、配料与营养数值", "请以实物包装说明为准"],
        "scene_title": "一份暖饮 多种时刻",
        "scene_subtitle": "早餐 / 办公 / 户外 / 分享",
        "scenes": [("早餐冲饮", "早餐相伴"), ("办公冲饮", "片刻放松"), ("户外片刻", "温暖随身"), ("好友分享", "围坐慢饮")],
    },
    {
        "key": "mulberry",
        "dir": "lagashan-mulberry-detail",
        "name": "拉尕山桑葚干果",
        "eyebrow": "甘南高原果干",
        "tagline": "甘南高原果实 / 酸甜醇厚",
        "product_image": ROOT / "tmp/pdfs/extracted-images/img-010.png",
        "hero": ROOT / "generated_images/exec-75b01e1b-1698-443f-9ea4-54139f167123.png",
        "process": ROOT / "generated_images/exec-21d6140f-c1a8-47eb-a77c-4f96ca79b113.png",
        "scene": ROOT / "generated_images/exec-1a154fc9-e48b-4e80-81b0-ccd2df9390a0.png",
        "dark": (71, 8, 31),
        "dark2": (39, 5, 18),
        "accent": (229, 190, 106),
        "cream": (250, 240, 220),
        "ink": (75, 24, 38),
        "badges": ["桑葚果干", "酸甜果香", "多样吃法"],
        "source_title": "甘南高原 生态桑葚",
        "source_subtitle": "成熟果实 经温和干燥处理",
        "source_statement": ["甄选甘南桑葚", "酸甜果香 自然醇厚"],
        "source_features": [("甘南高原", "生态产区"), ("成熟桑葚", "自然果香"), ("温和干燥", "果干口感")],
        "process_steps": [("成熟采摘", "甄选鲜果"), ("分选清洗", "去除杂质"), ("温和干燥", "保留果香"), ("质检装罐", "便携保存")],
        "detail_title": "深紫果粒 酸甜醇厚",
        "detail_subtitle": "果香自然 多种吃法随心搭配",
        "detail_features": [("深紫果粒", "成熟果色"), ("酸甜醇厚", "果香自然"), ("干爽耐嚼", "层次丰富"), ("多样搭配", "即食 / 泡饮")],
        "spec_rows": [("产品类别", "零食 / 干果"), ("产品规格", "75g / 罐"), ("原料特色", "甘南桑葚果实"), ("食用方式", "即食 / 泡水 / 搭配"), ("包装方式", "罐装")],
        "nutrition_title": "营养成分说明",
        "nutrition_body": ["桑葚果干的配料与营养数值", "请以实物包装为准"],
        "scene_title": "一罐多吃法 随心搭配",
        "scene_subtitle": "即食 / 泡水 / 配粥 / 分享",
        "scenes": [("开罐即食", "酸甜果香"), ("温水泡饮", "果味舒展"), ("搭配早餐", "配粥或酸奶"), ("茶桌分享", "自然果干")],
    },
]


@lru_cache(maxsize=None)
def cn(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_CN), size)


@lru_cache(maxsize=None)
def latin(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_LATIN_BOLD if bold else FONT_LATIN), size)


def cover(path: Path, blur: float = 0) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    image = ImageOps.fit(image, (W, H), method=Image.Resampling.LANCZOS)
    if blur:
        image = image.filter(ImageFilter.GaussianBlur(blur))
    return image


def layer() -> Image.Image:
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def add_solid(base: Image.Image, color: tuple[int, int, int], alpha: int) -> None:
    base.alpha_composite(Image.new("RGBA", (W, H), (*color, alpha)))


def add_top_gradient(base: Image.Image, color: tuple[int, int, int], height: int = 520, strength: int = 235) -> None:
    grad = layer()
    d = ImageDraw.Draw(grad)
    for y in range(height):
        t = 1 - y / max(1, height - 1)
        d.line((0, y, W, y), fill=(*color, round(strength * (t ** 1.55))))
    base.alpha_composite(grad)


def add_bottom_gradient(base: Image.Image, color: tuple[int, int, int], start: int = 1450, strength: int = 230) -> None:
    grad = layer()
    d = ImageDraw.Draw(grad)
    span = H - start
    for y in range(start, H):
        t = (y - start) / max(1, span - 1)
        d.line((0, y, W, y), fill=(*color, round(strength * (t ** 1.35))))
    base.alpha_composite(grad)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def fit_cn(draw: ImageDraw.ImageDraw, text: str, max_size: int, max_width: int, min_size: int = 24) -> ImageFont.FreeTypeFont:
    for size in range(max_size, min_size - 1, -2):
        f = cn(size)
        if text_width(draw, text, f) <= max_width:
            return f
    return cn(min_size)


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill, stroke: int = 0, stroke_fill=None) -> None:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (W - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill or fill)


def page_number(draw: ImageDraw.ImageDraw, number: int, accent) -> None:
    value = f"{number:02d} / 06"
    f = latin(23, True)
    tw = text_width(draw, value, f)
    draw.text((W - 58 - tw, 48), value, font=f, fill=accent)


def gold_rule(draw: ImageDraw.ImageDraw, y: int, accent, width: int = 188) -> None:
    x = (W - width) // 2
    draw.rounded_rectangle((x, y, x + width, y + 5), radius=2, fill=accent)


def pill(draw: ImageDraw.ImageDraw, box, text: str, p, font_size: int = 28, inverse: bool = False) -> None:
    x0, y0, x1, y1 = box
    fill = (*p["cream"], 235) if inverse else (*p["dark2"], 220)
    ink = p["ink"] if inverse else p["cream"]
    draw.rounded_rectangle(box, radius=(y1-y0)//2, fill=fill, outline=p["accent"], width=2)
    f = fit_cn(draw, text, font_size, x1-x0-30, 20)
    bb = draw.textbbox((0, 0), text, font=f)
    tx = x0 + ((x1-x0) - (bb[2]-bb[0]))//2
    ty = y0 + ((y1-y0) - (bb[3]-bb[1]))//2 - bb[1]
    draw.text((tx, ty), text, font=f, fill=ink, stroke_width=1, stroke_fill=ink)


def shadow_round(base: Image.Image, box, radius: int = 28, opacity: int = 120, offset=(12, 16), blur=20) -> None:
    x0, y0, x1, y1 = box
    mask = Image.new("L", (x1-x0, y1-y0), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, x1-x0, y1-y0), radius=radius, fill=opacity)
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    shade = Image.new("RGBA", mask.size, (0, 0, 0, 255))
    shade.putalpha(mask)
    base.alpha_composite(shade, (x0+offset[0], y0+offset[1]))


def photo_card(base: Image.Image, source: Path, box, p, label: str | None = None, pad: int = 22) -> None:
    x0, y0, x1, y1 = box
    cw, ch = x1-x0, y1-y0
    shadow_round(base, box)
    card = Image.new("RGBA", (cw, ch), (*p["cream"], 255))
    photo = Image.open(source).convert("RGB")
    inner_h = ch - pad*2 - (44 if label else 0)
    photo.thumbnail((cw-pad*2, inner_h), Image.Resampling.LANCZOS)
    px = (cw-photo.width)//2
    py = pad + (inner_h-photo.height)//2 + (38 if label else 0)
    card.alpha_composite(photo.convert("RGBA"), (px, py))
    cd = ImageDraw.Draw(card, "RGBA")
    cd.rounded_rectangle((1, 1, cw-2, ch-2), radius=28, outline=p["accent"], width=3)
    if label:
        label_font = cn(22)
        label_width = min(cw-36, max(132, text_width(cd, label, label_font) + 42))
        cd.rounded_rectangle((18, 16, 18+label_width, 54), radius=19, fill=(*p["dark"], 225))
        cd.text((39, 21), label, font=label_font, fill=p["cream"], stroke_width=1, stroke_fill=p["cream"])
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw, ch), radius=28, fill=255)
    card.putalpha(mask)
    base.alpha_composite(card, (x0, y0))


def header(draw: ImageDraw.ImageDraw, p, number: int, title: str, subtitle: str, y: int = 60, max_size: int = 62) -> None:
    page_number(draw, number, p["accent"])
    f = fit_cn(draw, title, max_size, W-120, 36)
    centered(draw, y, title, f, p["cream"], 1, p["dark2"])
    if subtitle and all(ord(ch) < 128 for ch in subtitle):
        sf = latin(25, True)
    else:
        sf = fit_cn(draw, subtitle, 28, W-160, 20)
    centered(draw, y+84, subtitle, sf, p["accent"])
    gold_rule(draw, y+138, p["accent"])


def save_page(image: Image.Image, out: Path, filename: str) -> None:
    target = out / filename
    temporary = out / f"{filename}.tmp"
    rgb = image.convert("RGB")
    try:
        rgb.save(temporary, "PNG", optimize=True)
        with Image.open(temporary) as check:
            check.verify()
    except Exception:
        if temporary.exists():
            temporary.unlink()
        rgb.save(temporary, "PNG", compress_level=6)
        with Image.open(temporary) as check:
            check.verify()
    temporary.replace(target)


def page_1(p, out: Path) -> None:
    image = cover(p["hero"])
    add_top_gradient(image, p["dark2"], 560, 245)
    add_bottom_gradient(image, p["dark2"], 1450, 245)
    draw = ImageDraw.Draw(image, "RGBA")
    page_number(draw, 1, p["accent"])
    draw.text((62, 58), p["eyebrow"], font=cn(29), fill=p["accent"], stroke_width=1, stroke_fill=p["accent"])
    title_font = fit_cn(draw, p["name"], 76, W-120, 48)
    draw.text((60, 120), p["name"], font=title_font, fill=p["cream"], stroke_width=2, stroke_fill=p["dark2"])
    tag_font = fit_cn(draw, p["tagline"], 30, 590, 22)
    tag_w = text_width(draw, p["tagline"], tag_font)
    draw.rounded_rectangle((60, 232, 100+tag_w, 290), radius=29, fill=(*p["dark2"], 190), outline=p["accent"], width=2)
    draw.text((80, 242), p["tagline"], font=tag_font, fill=p["cream"])

    photo_card(image, p["product_image"], (150, 1010, 930, 1535), p, label="商品原图", pad=22)

    x_boxes = [(45, 1700, 335, 1782), (395, 1700, 685, 1782), (745, 1700, 1035, 1782)]
    for box, label in zip(x_boxes, p["badges"]):
        pill(draw, box, label, p, 28)
    centered(draw, 1836, "包装以实物为准", cn(22), p["cream"])
    save_page(image, out, "01-商品首屏.png")


def page_2(p, out: Path) -> None:
    image = cover(p["hero"], blur=1.4)
    add_top_gradient(image, p["dark2"], 480, 238)
    add_bottom_gradient(image, p["dark2"], 1220, 248)
    draw = ImageDraw.Draw(image, "RGBA")
    header(draw, p, 2, p["source_title"], p["source_subtitle"], 60, 62)

    shadow_round(image, (92, 1010, 988, 1318), radius=32, opacity=120)
    draw.rounded_rectangle((92, 1010, 988, 1318), radius=32, fill=(*p["dark2"], 218), outline=p["accent"], width=2)
    centered(draw, 1062, p["source_statement"][0], fit_cn(draw, p["source_statement"][0], 54, 760, 36), p["cream"], 1)
    centered(draw, 1154, p["source_statement"][1], fit_cn(draw, p["source_statement"][1], 36, 760, 26), p["accent"])

    card_y0, card_y1 = 1460, 1766
    xs = [(42, 342), (390, 690), (738, 1038)]
    for idx, ((title, detail), (x0, x1)) in enumerate(zip(p["source_features"], xs), start=1):
        draw.rounded_rectangle((x0, card_y0, x1, card_y1), radius=26, fill=(*p["cream"], 235), outline=p["accent"], width=2)
        draw.ellipse((x0+112, card_y0+30, x0+188, card_y0+106), fill=p["accent"])
        num = f"0{idx}"
        nf = latin(21, True)
        nb = draw.textbbox((0, 0), num, font=nf)
        draw.text((x0+150-(nb[2]-nb[0])//2, card_y0+52), num, font=nf, fill=p["dark2"])
        tf = fit_cn(draw, title, 34, 250, 25)
        df = fit_cn(draw, detail, 25, 250, 20)
        tw = text_width(draw, title, tf)
        dw = text_width(draw, detail, df)
        draw.text((x0+(300-tw)//2, card_y0+136), title, font=tf, fill=p["ink"], stroke_width=1, stroke_fill=p["ink"])
        draw.text((x0+(300-dw)//2, card_y0+206), detail, font=df, fill=p["dark"])
    centered(draw, 1820, "原料与产区资料以产品包装标注为准", cn(22), p["cream"])
    save_page(image, out, "02-产地与原料.png")


def process_label(draw: ImageDraw.ImageDraw, p, y: int, index: int, title: str, detail: str) -> None:
    draw.rounded_rectangle((36, y, 458, y+118), radius=20, fill=(*p["dark2"], 220), outline=p["accent"], width=2)
    draw.ellipse((54, y+22, 124, y+92), fill=p["accent"])
    num = f"{index:02d}"
    nf = latin(23, True)
    nb = draw.textbbox((0, 0), num, font=nf)
    draw.text((89-(nb[2]-nb[0])//2, y+44), num, font=nf, fill=p["dark2"])
    tf = fit_cn(draw, title, 34, 276, 26)
    df = fit_cn(draw, detail, 23, 276, 19)
    draw.text((144, y+15), title, font=tf, fill=p["cream"], stroke_width=1, stroke_fill=p["cream"])
    draw.text((144, y+70), detail, font=df, fill=p["accent"])


def page_3(p, out: Path) -> None:
    image = cover(p["process"])
    overlay = Image.new("RGBA", (W, 150), (*p["dark2"], 225))
    image.alpha_composite(overlay, (0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    page_number(draw, 3, p["accent"])
    draw.text((50, 36), "加工过程", font=cn(52), fill=p["cream"], stroke_width=1, stroke_fill=p["cream"])
    draw.text((305, 58), "从原料到成品的工艺说明", font=cn(25), fill=p["accent"])
    for i, ((title, detail), y) in enumerate(zip(p["process_steps"], [225, 665, 1100, 1530]), start=1):
        process_label(draw, p, y, i, title, detail)
    draw.rounded_rectangle((626, 1836, 1038, 1886), radius=25, fill=(*p["dark2"], 190))
    draw.text((650, 1848), "工艺图片仅为说明，以真实生产为准", font=cn(19), fill=p["cream"])
    save_page(image, out, "03-加工工艺.png")


def page_4(p, out: Path) -> None:
    image = cover(p["hero"], blur=8)
    add_solid(image, p["dark2"], 92)
    add_top_gradient(image, p["dark2"], 420, 230)
    draw = ImageDraw.Draw(image, "RGBA")
    header(draw, p, 4, p["detail_title"], p["detail_subtitle"], 60, 61)
    photo_card(image, p["product_image"], (135, 330, 945, 820), p, label="商品与包装原图", pad=22)

    cards = [(50, 930, 510, 1250), (570, 930, 1030, 1250), (50, 1325, 510, 1645), (570, 1325, 1030, 1645)]
    for idx, ((title, detail), box) in enumerate(zip(p["detail_features"], cards), start=1):
        x0, y0, x1, y1 = box
        draw.rounded_rectangle(box, radius=28, fill=(*p["cream"], 235), outline=p["accent"], width=2)
        draw.ellipse((x0+32, y0+34, x0+106, y0+108), fill=p["accent"])
        num = f"{idx:02d}"
        nf = latin(22, True)
        nb = draw.textbbox((0, 0), num, font=nf)
        draw.text((x0+69-(nb[2]-nb[0])//2, y0+56), num, font=nf, fill=p["dark2"])
        tf = fit_cn(draw, title, 42, x1-x0-80, 28)
        df = fit_cn(draw, detail, 27, x1-x0-80, 22)
        draw.text((x0+34, y0+138), title, font=tf, fill=p["ink"], stroke_width=1, stroke_fill=p["ink"])
        draw.rounded_rectangle((x0+34, y0+210, x0+150, y0+215), radius=2, fill=p["accent"])
        draw.text((x0+34, y0+242), detail, font=df, fill=p["dark"])
    centered(draw, 1770, "风味与口感描述基于产品资料，具体以实物为准", cn(21), p["cream"])
    save_page(image, out, "04-细节与口感.png")


def gradient_background(p) -> Image.Image:
    img = Image.new("RGBA", (W, H), (*p["dark2"], 255))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        t = y / (H-1)
        c = tuple(round(p["dark2"][i]*(1-t) + p["dark"][i]*t) for i in range(3))
        d.line((0, y, W, y), fill=(*c, 255))
    for r, a in [(420, 22), (290, 16), (165, 12)]:
        d.ellipse((W-r-40, 100-r//2, W+40, 100+r//2), outline=(*p["accent"], a), width=3)
    return img


def page_5(p, out: Path) -> None:
    image = gradient_background(p)
    draw = ImageDraw.Draw(image, "RGBA")
    header(draw, p, 5, "规格与营养成分", "PRODUCT DETAILS", 48, 62)
    photo_card(image, p["product_image"], (185, 270, 895, 710), p, label="规格原图", pad=20)

    y = 790
    for label, value in p["spec_rows"]:
        draw.rounded_rectangle((68, y, 1012, y+96), radius=18, fill=(*p["cream"], 239), outline=(*p["accent"], 205), width=2)
        draw.text((96, y+28), label, font=cn(26), fill=p["dark"], stroke_width=1, stroke_fill=p["dark"])
        vf = fit_cn(draw, value, 29, 650, 21)
        draw.text((355, y+26), value, font=vf, fill=p["ink"], stroke_width=1, stroke_fill=p["ink"])
        y += 111

    draw.rounded_rectangle((68, 1375, 1012, 1645), radius=26, fill=(*p["accent"], 235))
    draw.text((102, 1410), p["nutrition_title"], font=cn(38), fill=p["dark2"], stroke_width=1, stroke_fill=p["dark2"])
    draw.rounded_rectangle((102, 1471, 252, 1476), radius=2, fill=p["dark2"])
    draw.text((102, 1510), p["nutrition_body"][0], font=fit_cn(draw, p["nutrition_body"][0], 28, 830, 22), fill=p["dark2"])
    draw.text((102, 1560), p["nutrition_body"][1], font=fit_cn(draw, p["nutrition_body"][1], 26, 830, 20), fill=p["dark2"])

    note = "具体配料、营养成分、生产日期、保质期及保存条件，以实物包装为准。"
    centered(draw, 1745, note, fit_cn(draw, note, 22, W-110, 17), p["cream"])
    save_page(image, out, "05-规格与营养.png")


def scene_box(draw: ImageDraw.ImageDraw, p, box, title: str, detail: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=20, fill=(*p["dark2"], 220), outline=p["accent"], width=2)
    draw.text((x0+20, y0+14), title, font=fit_cn(draw, title, 30, x1-x0-40, 22), fill=p["cream"], stroke_width=1, stroke_fill=p["cream"])
    draw.text((x0+20, y0+58), detail, font=fit_cn(draw, detail, 21, x1-x0-40, 18), fill=p["accent"])


def page_6(p, out: Path) -> None:
    image = cover(p["scene"])
    add_top_gradient(image, p["dark2"], 390, 230)
    draw = ImageDraw.Draw(image, "RGBA")
    header(draw, p, 6, p["scene_title"], p["scene_subtitle"], 58, 62)
    boxes = [(24, 420, 300, 520), (552, 420, 828, 520), (24, 1170, 300, 1270), (552, 1170, 828, 1270)]
    for box, (title, detail) in zip(boxes, p["scenes"]):
        scene_box(draw, p, box, title, detail)
    save_page(image, out, "06-食用场景.png")


def make_contact_sheet(out: Path) -> None:
    pages = [Image.open(out / f"{i:02d}-{name}.png").convert("RGB") for i, name in [
        (1, "商品首屏"), (2, "产地与原料"), (3, "加工工艺"), (4, "细节与口感"), (5, "规格与营养"), (6, "食用场景")
    ]]
    thumb_w = 270
    thumb_h = round(H * thumb_w / W)
    margin = 18
    sheet = Image.new("RGB", (thumb_w*3 + margin*4, thumb_h*2 + margin*3), (238, 233, 218))
    for idx, page in enumerate(pages):
        thumb = page.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = margin + (idx % 3) * (thumb_w + margin)
        y = margin + (idx // 3) * (thumb_h + margin)
        sheet.paste(thumb, (x, y))
    sheet.save(out / "00-全套预览.jpg", quality=92)

    long_w = 540
    long_h = round(H * long_w / W)
    long_img = Image.new("RGB", (long_w, long_h*6), WHITE)
    for idx, page in enumerate(pages):
        long_img.paste(page.resize((long_w, long_h), Image.Resampling.LANCZOS), (0, idx*long_h))
    long_img.save(out / "00-详情长图预览.jpg", quality=92)


def write_readme(p, out: Path) -> None:
    text = f"""# {p['name']}详情页制作说明

- 输出：6张PNG，单张1080×1920，9:16。
- 顺序：商品首屏、产地与原料、加工工艺、细节与口感、规格与营养、食用场景。
- 商品实拍：来自《2026年价格单》内嵌图片。
- 价格：未写入图片，便于在电商平台SKU字段独立维护。
- 规格：{dict(p['spec_rows']).get('产品规格', '')}。
- 文案限制：未虚构营养数值；配料、营养、日期、保质期与保存条件均提示以实物包装为准。
- 生成底图：商品广告摄影风格，严格无生成文字；中文标题与规格由后期排版生成。
"""
    (out / "制作说明.md").write_text(text, encoding="utf-8")


def validate_fonts() -> None:
    font = TTFont(str(FONT_CN))
    cmap = set()
    for table in font["cmap"].tables:
        cmap.update(table.cmap.keys())
    corpus = []
    for p in PRODUCTS:
        def collect(value):
            if isinstance(value, str):
                corpus.append(value)
            elif isinstance(value, dict):
                for item in value.values():
                    collect(item)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    collect(item)
        collect(p)
    fixed = "商品原图包装以实物为准加工过程从原料到成品的工艺说明工艺图片仅为说明，以真实生产为准商品与包装原图风味与口感描述基于产品资料，具体以实物为准规格与营养成分具体配料、营养成分、生产日期、保质期及保存条件，以实物包装为准。原料与产区资料以产品包装标注为准"
    corpus.append(fixed)
    missing = sorted({ch for ch in "".join(corpus) if ord(ch) > 127 and ord(ch) not in cmap})
    if missing:
        raise RuntimeError("Chinese font missing glyphs: " + "".join(missing))


def zip_product(p, out: Path) -> Path:
    zip_path = OUT_ROOT / f"{p['name']}-详情页-9x16.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as zf:
        for path in sorted(out.iterdir()):
            if path.is_file() and path.suffix != ".tmp":
                zf.write(path, arcname=f"{p['name']}/{path.name}")
    return zip_path


def make_batch_preview() -> None:
    previews = []
    for p in PRODUCTS:
        path = OUT_ROOT / p["dir"] / "00-全套预览.jpg"
        previews.append((p, Image.open(path).convert("RGB")))
    margin = 24
    label_h = 90
    cell_w = 900
    cell_h = 1100
    canvas = Image.new("RGB", (cell_w*2 + margin*3, cell_h*3 + margin*4), (32, 35, 24))
    draw = ImageDraw.Draw(canvas)
    for idx, (p, img) in enumerate(previews):
        img.thumbnail((cell_w-30, cell_h-label_h-30), Image.Resampling.LANCZOS)
        col, row = idx % 2, idx // 2
        x = margin + col*(cell_w+margin)
        y = margin + row*(cell_h+margin)
        draw.rounded_rectangle((x, y, x+cell_w, y+cell_h), radius=24, fill=(245, 240, 222), outline=p["accent"], width=3)
        tf = fit_cn(draw, p["name"], 42, cell_w-80, 30)
        draw.text((x+38, y+25), p["name"], font=tf, fill=p["dark"])
        canvas.paste(img, (x+(cell_w-img.width)//2, y+label_h))
    canvas.save(OUT_ROOT / "00-下一批5款-总览.jpg", quality=92)


def write_batch_readme() -> None:
    items = "\n".join(f"- {p['name']}：6张PNG，{dict(p['spec_rows']).get('产品规格', '')}" for p in PRODUCTS)
    text = f"""# 下一批5款商品详情页

{items}

统一规范：1080×1920（9:16）；每款6张；无固定价格；中文为后期排版；营养数值未虚构，标签信息以实物包装与检测材料为准。
"""
    (OUT_ROOT / "批次制作说明.md").write_text(text, encoding="utf-8")


def zip_batch() -> Path:
    zip_path = ROOT / "output/imagegen/下一批5款商品详情页-9x16.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as zf:
        for p in PRODUCTS:
            out = OUT_ROOT / p["dir"]
            for path in sorted(out.iterdir()):
                if path.is_file() and path.suffix != ".tmp":
                    zf.write(path, arcname=f"{p['name']}/{path.name}")
        zf.write(OUT_ROOT / "00-下一批5款-总览.jpg", arcname="00-下一批5款-总览.jpg")
        zf.write(OUT_ROOT / "批次制作说明.md", arcname="批次制作说明.md")
    return zip_path


def main() -> None:
    validate_fonts()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    required = [FONT_CN]
    for p in PRODUCTS:
        required.extend([p["product_image"], p["hero"], p["process"], p["scene"]])
    missing = [path for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))

    for p in PRODUCTS:
        out = OUT_ROOT / p["dir"]
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        page_1(p, out)
        page_2(p, out)
        page_3(p, out)
        page_4(p, out)
        page_5(p, out)
        page_6(p, out)
        make_contact_sheet(out)
        write_readme(p, out)
        zip_product(p, out)
        print(f"completed {p['name']}")

    make_batch_preview()
    write_batch_readme()
    zip_batch()
    print(f"completed batch at {OUT_ROOT}")


if __name__ == "__main__":
    main()
