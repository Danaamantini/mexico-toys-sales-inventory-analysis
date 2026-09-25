from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "assets" / "final"
SIZE = 512
SCALE = 4
WHITE = (255, 255, 255, 255)


def scaled(points):
    if isinstance(points[0], (tuple, list)):
        return [(int(x * SCALE), int(y * SCALE)) for x, y in points]
    return tuple(int(v * SCALE) for v in points)


def canvas():
    base = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse(scaled((69, 77, 443, 451)), fill=(1, 37, 43, 44))
    shadow = shadow.filter(ImageFilter.GaussianBlur(13 * SCALE))
    base.alpha_composite(shadow)

    circle = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(circle)
    cd.ellipse(
        scaled((68, 68, 444, 444)),
        fill=(255, 255, 255, 52),
        outline=(255, 255, 255, 86),
        width=2 * SCALE,
    )
    base.alpha_composite(circle)
    return base


def line(draw, points, width=17, fill=WHITE, joint="curve"):
    draw.line(scaled(points), fill=fill, width=width * SCALE, joint=joint)


def rounded(draw, box, radius=18, fill=None, outline=WHITE, width=16):
    draw.rounded_rectangle(
        scaled(box),
        radius=radius * SCALE,
        fill=fill,
        outline=outline,
        width=width * SCALE,
    )


def inventory_cost():
    im = canvas()
    d = ImageDraw.Draw(im)

    # Price tag outline with a clipped corner and a small punched hole.
    tag = [(164, 208), (275, 167), (355, 247), (270, 354), (164, 270), (164, 208)]
    line(d, tag, width=17)
    d.ellipse(scaled((270, 198, 300, 228)), outline=WHITE, width=12 * SCALE)

    font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font = ImageFont.truetype(font_path, 88 * SCALE)
    d.text(scaled((208, 218)), "$", font=font, fill=WHITE, stroke_width=1 * SCALE)
    return im


def days_cover():
    im = canvas()
    d = ImageDraw.Draw(im)

    rounded(d, (159, 175, 353, 348), radius=22, width=17)
    line(d, [(159, 226), (353, 226)], width=17)
    line(d, [(204, 153), (204, 195)], width=17)
    line(d, [(308, 153), (308, 195)], width=17)

    # Clean calendar grid: three days highlighted without tiny text.
    for x in (198, 247, 296):
        d.rounded_rectangle(scaled((x - 13, 257, x + 13, 283)), radius=5 * SCALE, fill=WHITE)
    for x in (198, 247, 296):
        d.rounded_rectangle(scaled((x - 13, 300, x + 13, 326)), radius=5 * SCALE, fill=WHITE)
    return im


def stockouts_demand():
    im = canvas()
    d = ImageDraw.Draw(im)

    # Open carton: distinct flaps, visible rim and container body.
    line(d, [(163, 231), (221, 174), (256, 221), (291, 174), (349, 231)], width=16)
    line(d, [(163, 231), (214, 267), (256, 221), (298, 267), (349, 231)], width=16)
    line(d, [(178, 247), (178, 330), (256, 374), (334, 330), (334, 247)], width=16)
    line(d, [(256, 280), (256, 374)], width=16)

    # Warning mark floats above the box and remains readable at dashboard size.
    d.polygon(scaled([(256, 126), (304, 202), (208, 202)]), outline=WHITE)
    line(d, [(256, 151), (256, 176)], width=13)
    d.ellipse(scaled((249, 184, 263, 198)), fill=WHITE)
    return im


def no_sales_inventory_prohibited():
    im = canvas()
    d = ImageDraw.Draw(im)

    # Two cartons establish stored inventory without excessive detail.
    rounded(d, (150, 231, 309, 359), radius=14, width=17)
    line(d, [(150, 276), (309, 276)], width=17)
    line(d, [(229, 231), (229, 276)], width=17)
    rounded(d, (183, 164, 296, 238), radius=11, width=14)
    line(d, [(183, 199), (296, 199)], width=14)

    # A separate prohibition badge makes "no sales" instantly recognizable.
    d.ellipse(scaled((277, 218, 367, 308)), outline=WHITE, width=16 * SCALE)
    line(d, [(292, 293), (352, 233)], width=17)
    return im


def save(name, image):
    OUT.mkdir(parents=True, exist_ok=True)
    image.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(OUT / name)


save("kpi-inventory-cost.png", inventory_cost())
save("kpi-days-cover.png", days_cover())
save("kpi-stockouts-demand.png", stockouts_demand())
save("kpi-high-no-sales.png", no_sales_inventory_prohibited())
