import os
import urllib.request

import cairosvg
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

URL = "https://github.com/google/fonts/raw/main/ofl/reemkufi/ReemKufi%5Bwght%5D.ttf"
TEXT = "وسمي"
OUT = "assets/logo"
os.makedirs(OUT, exist_ok=True)

urllib.request.urlretrieve(URL, "rk.ttf")
font = TTFont("rk.ttf")
if "fvar" in font:
    font = instantiateVariableFont(font, {"wght": 700})
font.save("rk700.ttf")

face = hb.Face(hb.Blob.from_file_path("rk700.ttf"))
hbfont = hb.Font(face)
buf = hb.Buffer()
buf.add_str(TEXT)
buf.guess_segment_properties()
hb.shape(hbfont, buf)

gs = font.getGlyphSet()
order = font.getGlyphOrder()
x = 0
d_parts = []
bounds = BoundsPen(gs)
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    name = order[info.codepoint]
    tr = (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)
    pen = SVGPathPen(gs)
    gs[name].draw(TransformPen(pen, tr))
    d_parts.append(pen.getCommands())
    gs[name].draw(TransformPen(bounds, tr))
    x += pos.x_advance
xmin, ymin, xmax, ymax = bounds.bounds
w, h = xmax - xmin, ymax - ymin
pad = round(max(w, h) * 0.08)
vb = f"{xmin - pad:.0f} {ymin - pad:.0f} {w + 2 * pad:.0f} {h + 2 * pad:.0f}"
d = " ".join(d_parts)


def svg(fill, bg=None):
    rect = ""
    if bg:
        rect = f'<rect x="{xmin - pad:.0f}" y="{ymin - pad:.0f}" width="{w + 2 * pad:.0f}" height="{h + 2 * pad:.0f}" fill="{bg}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{rect}<path d="{d}" fill="{fill}"/></svg>'


variants = {
    "wasmi-logo": ("#5A331C", None),
    "wasmi-logo-sand": ("#5A331C", "#FAF3E6"),
    "wasmi-logo-white": ("#FAF3E6", None),
    "wasmi-logo-on-brown": ("#FAF3E6", "#5A331C"),
}
for name, (fill, bg) in variants.items():
    s = svg(fill, bg)
    open(f"{OUT}/{name}.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}.png", output_width=2000)
print("done", vb)
