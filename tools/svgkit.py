"""Petit kit pour générer des SVG autonomes au texte vectorisé.

Les SVG affichés via <img> (cas de GitHub) ne chargent aucune ressource externe, et un SVG
statique n'est dessiné qu'une fois : une police embarquée arrive souvent trop tard.
Le texte est donc mis en forme par HarfBuzz (crénage, ligatures) puis converti en tracés :
rendu identique partout, sans dépendance aux polices. Le contenu reste décrit par <title>
et par le texte alternatif de l'image dans le README.
"""
import os
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILES = {
    'S': 'serif.ttf', 'SI': 'serif-italic.ttf', 'M': 'mono.ttf', 'N5': 'sans500.ttf', 'N7': 'sans700.ttf',
}
FALLBACK = {
    'S': "Georgia, 'Times New Roman', serif", 'SI': "Georgia, 'Times New Roman', serif",
    'M': "Consolas, 'Courier New', monospace", 'N5': "'Segoe UI', Helvetica, Arial, sans-serif",
    'N7': "'Segoe UI', Helvetica, Arial, sans-serif",
}
FONT_URLS = {
    'serif.ttf': 'https://fonts.gstatic.com/s/instrumentserif/v5/jizBRFtNs2ka5fXjeivQ4LroWlx-2zI.ttf',
    'serif-italic.ttf': 'https://fonts.gstatic.com/s/instrumentserif/v5/jizHRFtNs2ka5fXjeivQ4LroWlx-6zATiw.ttf',
    'mono.ttf': 'https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8-qxjPQ.ttf',
    'sans500.ttf': 'https://fonts.gstatic.com/s/manrope/v20/xn7_YHE41ni1AdIRqAuZuw1Bx9mbZk7PFO_F.ttf',
    'sans700.ttf': 'https://fonts.gstatic.com/s/manrope/v20/xn7_YHE41ni1AdIRqAuZuw1Bx9mbZk4aE-_F.ttf',
}
os.makedirs(os.path.join(HERE, 'fonts'), exist_ok=True)
for _name, _url in FONT_URLS.items():
    _path = os.path.join(HERE, 'fonts', _name)
    if not os.path.exists(_path):
        import urllib.request
        urllib.request.urlretrieve(_url, _path)

_fonts = {k: TTFont(os.path.join(HERE, 'fonts', v)) for k, v in FONT_FILES.items()}
_hb = {k: hb.Font(hb.Face(hb.Blob.from_file_path(os.path.join(HERE, 'fonts', v)))) for k, v in FONT_FILES.items()}
_gsets = {k: f.getGlyphSet() for k, f in _fonts.items()}
_orders = {k: f.getGlyphOrder() for k, f in _fonts.items()}


NTOS = lambda v: f'{v:.0f}' if float(v).is_integer() else f'{v:.1f}'


def shape(text, font):
    """Glyphes et avances (unités de police) après mise en forme HarfBuzz."""
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(_hb[font], buf, {'kern': True, 'liga': True})
    return [(i.codepoint, p.x_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

# Palette (identique au site)
ROOM_OFF, ROOM_ON, INK2 = '#121417', '#1c1f24', '#24282e'
CREAM, CREAM2, MUTED = '#ede4d3', '#c9bfad', '#a39b8d'
BRASS, BRASS3, BRASS1, BRASS2 = '#d6b273', '#f1ddae', '#7a5a2e', '#c9a063'
LINE = 'rgba(237,228,211,0.13)'
SAGE = '#8fa7a0'
LIVE = '#3fa45b'


def measure(text, font, size, ls=0.0):
    upm = _fonts[font]['head'].unitsPerEm
    g = shape(text, font)
    return sum(adv for _, adv, _, _ in g) / upm * size + ls * len(g)


def wrap(text, font, size, maxw, ls=0.0):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if measure(t, font, size, ls) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.body, self.css, self.defs = [], [], []
        self.glyphs = {}

    # -- texte -------------------------------------------------------------
    def _glyph(self, font, gid):
        """Définit un glyphe une seule fois par fichier (réutilisé via <use>)."""
        key = f'g{font}{gid}'
        if key not in self.glyphs:
            pen = SVGPathPen(_gsets[font], ntos=NTOS)
            _gsets[font][_orders[font][gid]].draw(pen)
            self.glyphs[key] = pen.getCommands()
        return key

    def text(self, x, y, s, font='N5', size=16, fill=CREAM, anchor='start', ls=0, cls='', extra=''):
        upm = _fonts[font]['head'].unitsPerEm
        k = size / upm
        glyphs = shape(s, font)
        width = (sum(adv for _, adv, _, _ in glyphs) * k + ls * (len(glyphs) - 1)) if glyphs else 0
        x0 = x - {'start': 0, 'middle': width / 2, 'end': width}[anchor]
        c = f' class="{cls}"' if cls else ''
        tf = f'translate({x0:.1f},{y:.1f}) scale({k:.5f},{-k:.5f})'
        if fill.startswith('url('):
            # Dégradé : un seul tracé pour que le dégradé couvre tout le mot
            pen = SVGPathPen(_gsets[font], ntos=NTOS); cx = 0
            for gid, adv, xo, yo in glyphs:
                _gsets[font][_orders[font][gid]].draw(TransformPen(pen, (1, 0, 0, 1, cx + xo, yo)))
                cx += adv + ls / k
            return f'<path{c}{extra} fill="{fill}" transform="{tf}" d="{pen.getCommands()}"/>'
        uses, cx = [], 0
        for gid, adv, xo, yo in glyphs:
            if _orders[font][gid] not in ('space', 'uni00A0'):
                yy = f' y="{yo}"' if yo else ''
                uses.append(f'<use href="#{self._glyph(font, gid)}" x="{cx + xo:.0f}"{yy}/>')
            cx += adv + ls / k
        return f'<g{c}{extra} fill="{fill}" transform="{tf}">{"".join(uses)}</g>'

    def add(self, *parts):
        self.body.extend(parts)

    def pill(self, x, y, label, font='N5', size=13, pad=13, h=30, stroke='rgba(237,228,211,0.22)',
             fill='rgba(255,246,228,0.03)', color=CREAM2, cls=''):
        w = measure(label, font, size) + 2 * pad
        c = f' class="{cls}"' if cls else ''
        g = (f'<g{c}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}"/>'
             + self.text(x + pad, y + h / 2 + size * 0.36, label, font, size, color) + '</g>')
        return g, w

    def pills(self, x, y, labels, maxw, gap=8, row_gap=10, **kw):
        """Dispose des pastilles en lignes ; renvoie (svg, hauteur totale)."""
        out, cx, cy, h = [], x, y, kw.get('h', 30)
        for lab in labels:
            w = measure(lab, kw.get('font', 'N5'), kw.get('size', 13)) + 2 * kw.get('pad', 13)
            if cx + w > x + maxw and cx > x:
                cx = x; cy += h + row_gap
            g, w = self.pill(cx, cy, lab, **kw)
            out.append(g); cx += w + gap
        return ''.join(out), cy + h - y

    # -- rendu ---------------------------------------------------------------
    def render(self):
        css = ''.join(self.css) + '@media (prefers-reduced-motion: reduce){*{animation:none!important;}}'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">'
                f'<title>{escape(self.title)}</title><defs>{"".join(self.defs)}'
                f'{"".join(f'<path id="{k}" d="{d}"/>' for k, d in self.glyphs.items())}</defs>'
                f'<style>{css}</style>{"".join(self.body)}</svg>')

    def save(self, path):
        with open(path, 'w', encoding='utf8') as fh:
            fh.write(self.render())
        return os.path.getsize(path)


# Icônes Lucide (tracés officiels, 24x24)
ICONS = {
    'arrow': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    'linkedin': '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    'github': '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
    'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'globe': '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
}


def icon(name, x, y, size=20, color=CREAM, sw=1.8):
    s = size / 24
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw / s:.2f}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')
