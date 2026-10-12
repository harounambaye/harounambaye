"""Génère les visuels SVG du README de profil GitHub (identité « la lampe »)."""
import os, random, sys
from svgkit import (Svg, measure, wrap, icon, ROOM_OFF, ROOM_ON, INK2, CREAM, CREAM2, MUTED,
                    BRASS, BRASS1, BRASS2, BRASS3, LINE, SAGE, LIVE)

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
W = 1200
# Le texte reste visible à tout instant (aperçus figés, lecteurs sans animation) :
# l'entrée n'est qu'un léger glissement, jamais un fondu depuis l'invisible.
FADE = ('.up{animation:up .9s cubic-bezier(.22,1,.36,1) both;}'
        '@keyframes up{from{transform:translateY(10px);}to{transform:none;}}')


def frame(s, w, h, fill=ROOM_OFF, rx=28):
    """Carte sombre aux coins arrondis + liseré fin, avec un clip pour le contenu."""
    s.defs.append(f'<clipPath id="card"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    s.add(f'<rect width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>')


def border(s, w, h, rx=28):
    s.add(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{LINE}"/>')


def d(delay):
    return f' style="animation-delay:{delay:.2f}s"'


def brass_defs(s):
    s.defs.append(f'<linearGradient id="brass" x1="0" y1="0" x2="1" y2="0.2"><stop offset="0" stop-color="{BRASS1}"/>'
                  f'<stop offset=".3" stop-color="{BRASS2}"/><stop offset=".5" stop-color="{BRASS3}"/>'
                  f'<stop offset=".7" stop-color="{BRASS2}"/><stop offset="1" stop-color="{BRASS1}"/></linearGradient>')
    s.defs.append(f'<radialGradient id="bead" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="{BRASS3}"/>'
                  f'<stop offset=".5" stop-color="{BRASS2}"/><stop offset="1" stop-color="{BRASS1}"/></radialGradient>')


def lamp(s, x, y, k, lit_cls='on'):
    """Lampe champignon (repère 240x330 du site), allumée via la classe lit_cls."""
    s.defs.append('<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgb(255,214,150)" stop-opacity=".42"/>'
                  '<stop offset="1" stop-color="rgb(255,214,150)" stop-opacity="0"/></linearGradient>'
                  '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>')
    return (f'<g transform="translate({x},{y}) scale({k})">'
            f'<path class="{lit_cls}" d="M34 114 L206 114 L292 330 L-52 330 Z" fill="url(#cone)"/>'
            f'<ellipse class="{lit_cls}" cx="120" cy="80" rx="120" ry="60" fill="rgba(255,214,150,.45)" filter="url(#blur)"/>'
            '<rect x="114" y="112" width="12" height="180" rx="3" fill="#c4baa8"/>'
            '<rect x="66" y="288" width="108" height="11" rx="5.5" fill="#c4baa8"/>'
            '<path d="M22 113 C22 60 66 34 120 34 C174 34 218 60 218 113 Z" fill="#cfc5b3"/>'
            f'<path class="{lit_cls}" d="M22 113 C22 60 66 34 120 34 C174 34 218 60 218 113 Z" fill="#fbf2e0"/>'
            '<ellipse cx="120" cy="113" rx="98" ry="6" fill="#a89e8c"/>'
            f'<ellipse class="{lit_cls}" cx="120" cy="113" rx="98" ry="6" fill="#fff7e3"/>'
            '<g class="cord"><line x1="176" y1="113" x2="176" y2="200" stroke="#b9ae9a" stroke-width="1.5"/>'
            '<circle cx="176" cy="206" r="6.5" fill="url(#bead)"/></g></g>')


LAMP_CSS = ('.on{animation:on 2.4s .4s both;}'
            '@keyframes on{0%,30%{opacity:0;}34%{opacity:.85;}37%{opacity:.2;}42%{opacity:1;}46%{opacity:.55;}50%,100%{opacity:1;}}'
            '.cord{transform-box:fill-box;animation:tug 1s .75s both;}'
            '@keyframes tug{0%{transform:none;}25%{transform:translateY(16px);}60%{transform:translateY(-3px);}100%{transform:none;}}')


# ---------------------------------------------------------------- HERO
def hero():
    h = 500
    s = Svg(W, h, "Harouna MBAYE — Data Scientist & BI Analyst, spécialisé en IA. Dakar, Sénégal.")
    brass_defs(s)
    s.defs.append('<radialGradient id="halo" gradientUnits="userSpaceOnUse" cx="955" cy="150" r="560">'
                  '<stop offset="0" stop-color="rgb(255,200,130)" stop-opacity=".30"/>'
                  '<stop offset=".4" stop-color="rgb(255,200,130)" stop-opacity=".08"/>'
                  '<stop offset="1" stop-color="rgb(255,200,130)" stop-opacity="0"/></radialGradient>')
    s.css += [LAMP_CSS, FADE,
              '.ring{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out infinite;}'
              '@keyframes ring{from{transform:scale(1);opacity:.7;}to{transform:scale(2.6);opacity:0;}}']
    frame(s, W, h)
    s.add('<g clip-path="url(#card)">',
          f'<rect class="on" width="{W}" height="{h}" fill="{ROOM_ON}"/>',
          f'<rect class="on" width="{W}" height="{h}" fill="url(#halo)"/>',
          lamp(s, 835, 52, 1.04),
          '</g>')
    x = 72
    s.add(f'<g class="up"{d(.1)}><line x1="{x}" y1="99" x2="{x+30}" y2="99" stroke="{BRASS}" stroke-width="1.2"/>'
          + s.text(x + 44, 104, 'PORTFOLIO — DAKAR, SÉNÉGAL', 'M', 14, BRASS, ls=3.5) + '</g>')
    s.add(f'<g class="up"{d(.2)}>' + s.text(x - 4, 232, 'Harouna', 'S', 128, CREAM, ls=-3) + '</g>')
    s.add(f'<g class="up"{d(.3)}>' + s.text(x + 6, 350, 'MBAYE', 'SI', 128, 'url(#brass)', ls=-1) + '</g>')
    s.add(f'<g class="up"{d(.45)}>' + s.text(x, 412, 'Data Scientist & BI Analyst', 'N7', 30, CREAM, ls=-.4) + '</g>')
    s.add(f'<g class="up"{d(.55)}>' + s.text(x, 448, 'Intelligence Artificielle · Machine Learning · Deep Learning · XAI', 'N5', 18, MUTED) + '</g>')
    # Pastille « ouvert à un poste »
    label = 'Ouvert à un poste · Data · BI · IA'
    pw = measure(label, 'N7', 15) + 64
    px, py = W - 56 - pw, 416
    s.add(f'<g class="up"{d(1.4)}><rect x="{px}" y="{py}" width="{pw:.1f}" height="40" rx="20" fill="rgba(18,20,23,.75)" stroke="rgba(214,178,115,.55)"/>'
          f'<circle class="ring" cx="{px+24}" cy="{py+20}" r="5" fill="{LIVE}"/><circle cx="{px+24}" cy="{py+20}" r="5" fill="{LIVE}"/>'
          + s.text(px + 42, py + 25.5, label, 'N7', 15, CREAM) + '</g>')
    border(s, W, h)
    return s


# ---------------------------------------------------------------- BOUTONS
def button(label, ico, primary=False):
    size, pad, ih, h = 16, 26, 18, 52
    w = pad * 2 + measure(label, 'N7', size) + ih + 10
    s = Svg(round(w), h, label)
    if primary:
        brass_defs(s)
        s.defs.append('<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                      '<stop offset=".5" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                      f'<clipPath id="b"><rect width="{w:.1f}" height="{h}" rx="{h/2}"/></clipPath>')
        s.css.append('.sh{animation:sh 3.6s 1s ease-in-out infinite;}@keyframes sh{0%{transform:translateX(-120px);}40%,100%{transform:translateX(' + str(round(w + 40)) + 'px);}}')
        s.add(f'<rect width="{w:.1f}" height="{h}" rx="{h/2}" fill="url(#brass)"/>',
              f'<g clip-path="url(#b)"><rect class="sh" x="0" y="0" width="70" height="{h}" fill="url(#sheen)" transform="skewX(-20)"/></g>',
              f'<rect x=".5" y=".5" width="{w-1:.1f}" height="{h-1}" rx="{h/2}" fill="none" stroke="rgba(255,250,235,.45)"/>')
        color = '#1b150b'
    else:
        s.add(f'<rect x=".5" y=".5" width="{w-1:.1f}" height="{h-1}" rx="{h/2}" fill="{ROOM_ON}" stroke="rgba(237,228,211,.28)"/>')
        color = CREAM
    s.add(icon(ico, pad, (h - ih) / 2, ih, color), s.text(pad + ih + 10, h / 2 + size * .36, label, 'N7', size, color))
    return s


# ---------------------------------------------------------------- EN-TÊTES DE SECTION (clair / sombre)
def header(num, eyebrow, plain, italic, theme):
    ink, acc, line = (CREAM, BRASS3, BRASS) if theme == 'dark' else (ROOM_OFF, '#7a5a2e', '#8a6430')
    s = Svg(W, 140, f'{num} — {eyebrow}. {plain} {italic}')
    s.css.append(FADE)
    s.add(f'<g class="up"><line x1="4" y1="45" x2="34" y2="45" stroke="{line}" stroke-width="1.2"/>'
          + s.text(48, 50, f'{num} — {eyebrow.upper()}', 'M', 14, line, ls=3.5) + '</g>')
    x2 = measure(plain + ' ', 'S', 56, -1)
    s.add(f'<g class="up"{d(.12)}>' + s.text(0, 118, plain, 'S', 56, ink, ls=-1)
          + s.text(x2, 118, italic, 'SI', 56, acc, ls=-1) + '</g>')
    return s


# ---------------------------------------------------------------- CE QUE J'APPORTE
VALUES = [
    ('01', 'Analyser', "Explorer, nettoyer et modéliser les données avec Python, Pandas et scikit-learn, puis rendre les modèles explicables.", 'ML · DEEP LEARNING · XAI'),
    ('02', 'Décider', "Concevoir entrepôts et tableaux de bord sur Microsoft Fabric et Power BI, modélisés en Data Vault 2.0.", 'BI · FABRIC · ETL/ELT'),
    ('03', 'Livrer', "Intégrer analyses et modèles dans des applications réelles : développement fullstack, API REST, Docker.", 'NODE.JS · API · DOCKER'),
    ('04', 'Transmettre', "Former et encadrer : programmation, IA et développement web, avec une exigence de qualité du code.", '3 ÉTABLISSEMENTS'),
]


def values():
    items = VALUES
    h, cw, gap = 330, 285, 20
    s = Svg(W, h, "Ce que j'apporte : " + ' ; '.join(f'{t} — {x}' for _, t, x, _ in items))
    s.css += [FADE, '.bar{transform-box:fill-box;transform-origin:left;animation:bar 1s cubic-bezier(.22,1,.36,1) both;}@keyframes bar{from{transform:scaleX(0);}to{transform:none;}}']
    for i, (n, t, txt, tag) in enumerate(items):
        x = i * (cw + gap)
        g = [f'<g class="up"{d(.1 + i * .12)}>',
             f'<rect x="{x+.5}" y=".5" width="{cw-1}" height="{h-1}" rx="24" fill="{ROOM_OFF}" stroke="{LINE}"/>',
             f'<rect class="bar"{d(.4 + i * .12)} x="{x+28}" y="28" width="36" height="2" fill="{BRASS}"/>',
             s.text(x + 28, 66, n, 'M', 13, BRASS, ls=2),
             s.text(x + 28, 114, t, 'S', 38, CREAM, ls=-.5)]
        for j, ln in enumerate(wrap(txt, 'N5', 15.5, cw - 56)):
            g.append(s.text(x + 28, 152 + j * 24, ln, 'N5', 15.5, CREAM2))
        g.append(s.text(x + 28, h - 30, tag, 'M', 11.5, BRASS, ls=1.6))
        g.append('</g>')
        s.add(*g)
    return s


# ---------------------------------------------------------------- CARTES PROJETS
def project(key, idx, kind, title, sub, desc, tags, status, visual, side='left'):
    h, vw = 450, 560
    s = Svg(W, h, f'{title} — {sub}. {desc} Stack : {", ".join(tags)}.')
    brass_defs(s)
    s.css += [FADE, '.blink{animation:blink 1.4s infinite;}@keyframes blink{0%,100%{opacity:.25;}50%{opacity:1;}}']
    frame(s, W, h)
    vx = 0 if side == 'left' else W - vw
    s.defs.append(f'<clipPath id="vis"><rect x="{vx}" width="{vw}" height="{h}"/></clipPath>')
    s.add('<g clip-path="url(#card)"><g clip-path="url(#vis)">', f'<g transform="translate({vx},0)">', visual(s), '</g></g>',
          f'<line x1="{vx + (vw if side == "left" else 0)}" y1="0" x2="{vx + (vw if side == "left" else 0)}" y2="{h}" stroke="{LINE}"/></g>')
    tx = vw + 56 if side == 'left' else 56
    tw = W - vw - 112
    s.add(f'<g class="up"{d(.15)}>' + s.text(tx, 70, f'{idx} — {kind.upper()}', 'M', 13, BRASS, ls=2.6) + '</g>')
    s.add(f'<g class="up"{d(.25)}>' + s.text(tx - 2, 130, title, 'S', 52, CREAM, ls=-.8) + '</g>')
    y = 130
    if sub:
        y += 36
        s.add(f'<g class="up"{d(.32)}>' + s.text(tx, y, sub, 'N7', 18, CREAM) + '</g>')
    y += 38
    lines = wrap(desc, 'N5', 16.5, tw)
    s.add(f'<g class="up"{d(.4)}>' + ''.join(s.text(tx, y + i * 26, ln, 'N5', 16.5, CREAM2) for i, ln in enumerate(lines)) + '</g>')
    y += (len(lines) - 1) * 26 + 22
    p, ph = s.pills(tx, y, tags, tw)
    s.add(f'<g class="up"{d(.5)}>{p}</g>')
    # Statut en pied de carte
    label, live = status
    sy = h - 44
    if label is None:
        assert y + ph < sy, f'{key}: débordement'
        border(s, W, h)
        return s
    dot = (f'<circle class="blink" cx="{tx+5}" cy="{sy-4}" r="4.5" fill="{LIVE}"/>' if live
           else f'<circle cx="{tx+5}" cy="{sy-4}" r="4" fill="none" stroke="{BRASS}" stroke-width="1.4"/>')
    s.add(f'<g class="up"{d(.6)}>' + dot + s.text(tx + 20, sy, label.upper(), 'M', 12, CREAM2 if live else MUTED, ls=1.8) + '</g>')
    assert y + ph < sy - 24, f'{key}: débordement ({y+ph} >= {sy-24})'
    border(s, W, h)
    return s


def v_teranga(s):
    s.defs.append('<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="rgba(237,228,211,.05)"/></pattern>')
    s.css.append('.dvt{font-size:11px;}')
    out = ['<rect width="560" height="440" fill="#16191d"/><rect width="560" height="440" fill="url(#grid)"/>',
           '<g transform="translate(14,40) scale(.83)">']
    for z, zx in (('INGESTION', 150), ('DATA VAULT 2.0', 300), ('RESTITUTION', 520)):
        out.append(s.text(zx, 44, z, 'M', 10, MUTED, ls=2))
    wires = ['M120 210 H150', 'M205 232 V300', 'M260 322 C280 322 280 132 300 132', 'M260 322 C280 322 280 210 300 210',
             'M260 322 C280 322 280 288 300 288', 'M346 154 V188', 'M346 266 V232', 'M392 132 C402 132 402 80 412 80',
             'M392 288 C402 288 402 340 412 340', 'M392 210 H520']
    out += [f'<path d="{w}" fill="none" stroke="rgba(214,178,115,.38)" stroke-width="1.3"/>' for w in wires]
    out.append('<path d="M205 120 V188" fill="none" stroke="rgba(214,178,115,.38)" stroke-width="1.3" stroke-dasharray="4 4"/>')
    for i, pth in enumerate(['M120 210 H205 V322 H260 C280 322 280 210 300 210 H520',
                             'M120 210 H205 V322 H260 C280 322 280 132 300 132 H346 V210 H520',
                             'M120 210 H205 V322 H260 C280 322 280 288 300 288 H346 V210 H520']):
        out.append(f'<circle r="3.6" fill="{BRASS3}"><animateMotion dur="4.2s" begin="{i*1.4}s" repeatCount="indefinite" path="{pth}"/></circle>')
    nodes = [(16, 188, 104, 44, 'Sources', 'E-COMMERCE', LINE), (150, 76, 110, 44, 'Data Factory', 'ORCHESTRATION', LINE),
             (150, 188, 110, 44, 'OneLake', 'LAKEHOUSE', LINE), (150, 300, 110, 44, 'PySpark', 'INSERT-ONLY', LINE),
             (300, 110, 92, 44, 'HUB', 'CLÉ MÉTIER', BRASS), (300, 188, 92, 44, 'LINK', 'RELATION', SAGE),
             (300, 266, 92, 44, 'HUB', 'CLÉ MÉTIER', BRASS), (412, 60, 84, 40, 'SAT', 'HISTORIQUE', 'rgba(237,228,211,.32)'),
             (412, 320, 84, 40, 'SAT', 'HISTORIQUE', 'rgba(237,228,211,.32)'), (520, 188, 104, 44, 'Power BI', 'DIRECT LAKE', BRASS)]
    for x, y, w, hh, a, b, st in nodes:
        dash = ' stroke-dasharray="3 3"' if a == 'SAT' else ''
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="10" fill="rgba(24,27,32,.96)" stroke="{st}"{dash}/>'
                   + s.text(x + 12, y + 19, a, 'M', 11.5, CREAM) + s.text(x + 12, y + 34, b, 'M', 8.5, MUTED, ls=.8))
    out.append('</g>')
    return ''.join(out)


def v_esen(s):
    s.defs.append('<radialGradient id="eg" cx="1" cy="0" r="1"><stop offset="0" stop-color="rgb(255,200,130)" stop-opacity=".14"/>'
                  '<stop offset=".7" stop-color="rgb(255,200,130)" stop-opacity="0"/></radialGradient>')
    o = [f'<rect width="560" height="440" fill="{ROOM_ON}"/><rect width="560" height="440" fill="url(#eg)"/>']
    x0, x1 = 90, 470
    o.append(f'<g class="up"{d(.1)}><circle cx="{x0+17}" cy="92" r="17" fill="url(#brass)"/>'
             + s.text(x0 + 17, 96.5, 'eS', 'N7', 12, '#1b150b', anchor='middle')
             + s.text(x0 + 44, 88, 'eSenGuide', 'N7', 15, CREAM) + s.text(x0 + 44, 106, 'Assistant administratif', 'N5', 12, MUTED)
             + f'<line x1="{x0}" y1="128" x2="{x1}" y2="128" stroke="{LINE}"/></g>')
    q = wrap('Quelles démarches pour mon casier judiciaire ?', 'N5', 15, 230)
    bw = max(measure(l, 'N5', 15) for l in q) + 30
    bh = len(q) * 21 + 20
    o.append(f'<g class="up"{d(.5)}><path d="M{x1-bw} 150 h{bw-14} a14 14 0 0 1 14 14 v{bh-18} a4 4 0 0 1 -4 4 h{-(bw-14)} a14 14 0 0 1 -14 -14 v{-(bh-18)} a14 14 0 0 1 14 -14z" fill="{CREAM}"/>'
             + ''.join(s.text(x1 - bw + 15, 150 + 26 + i * 21, l, 'N5', 15, ROOM_OFF) for i, l in enumerate(q)) + '</g>')
    by = 150 + bh + 14
    o.append(f'<g class="up"{d(1)}><rect x="{x0}" y="{by}" width="150" height="46" rx="16" fill="rgba(255,246,228,.06)" stroke="{LINE}"/>'
             + ''.join(f'<circle class="blink" style="animation-delay:{i*.18}s" cx="{x0+28+i*14}" cy="{by+23}" r="4" fill="{BRASS}"/>' for i in range(3)) + '</g>')
    p, _ = s.pills(x0, by + 64, ['CNI', 'Casier judiciaire', 'Certificat de résidence'], x1 - x0, size=12.5, stroke='rgba(214,178,115,.5)', color=BRASS3, h=28)
    o.append(f'<g class="up"{d(1.5)}>{p}</g>')
    return ''.join(o)


def v_ceedrt(s):
    o = [f'<rect width="560" height="440" fill="{CREAM}"/>']
    rows = [('C', 'Collectif des'), ('E', 'Élèves et'), ('E', 'Étudiants pour le'), ('D', 'Développement de la'), ('R', 'Région de'), ('T', 'Tambacounda')]
    for i, (L, wd) in enumerate(rows):
        y = 92 + i * 54
        o.append(f'<g class="up"{d(.15 + i * .1)}>' + s.text(64, y, L, 'S', 50, ROOM_OFF) + s.text(118, y - 4, wd, 'S', 26, '#5f5a50') + '</g>')
    o.append(s.text(496, 410, 'CEEDRT.COM', 'M', 11, '#7a5a2e', anchor='end', ls=2))
    return ''.join(o)


def v_storm(s):
    o = ['<rect width="560" height="440" fill="#0e1013"/><g transform="translate(0,58)">']
    wires = ['M108 150 C180 150 190 80 232 80', 'M108 150 C180 150 190 220 232 220', 'M288 80 C350 80 370 150 412 150', 'M288 220 C350 220 370 150 412 150']
    o += [f'<path d="{w}" fill="none" stroke="rgba(237,228,211,.18)"/>' for w in wires]
    for i, (w, b) in enumerate(zip(wires + ['M468 150 H560'], [0, .5, .9, 1.2, .2])):
        o.append(f'<circle r="3.4" fill="{BRASS3}"><animateMotion dur="1.6s" begin="{b}s" repeatCount="indefinite" path="{w}"/></circle>')
    for cx, cy, lab, sp in ((80, 150, 'spout', True), (260, 80, 'bolt', False), (260, 220, 'bolt', False), (440, 150, 'bolt', False)):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="28" fill="#16191d" stroke="{BRASS if sp else "rgba(237,228,211,.25)"}"/>'
                 + s.text(cx, cy + 4, lab, 'M', 11, CREAM2, anchor='middle'))
    o.append('</g>' + s.text(28, 404, '$ storm topology · flux continu', 'M', 11, MUTED))
    return ''.join(o)


def v_prestige(s):
    s.defs.append('<radialGradient id="pg" cx="0" cy="1" r="1"><stop offset="0" stop-color="#8fa7a0" stop-opacity=".2"/><stop offset=".7" stop-color="#8fa7a0" stop-opacity="0"/></radialGradient>'
                  '<clipPath id="brw"><rect x="56" y="78" width="370" height="260" rx="12"/></clipPath>')
    s.css.append('.lg{animation:lg 6s cubic-bezier(.22,1,.36,1) infinite;}@keyframes lg{0%,42%{transform:none;}50%,92%{transform:translateX(30px);}100%{transform:none;}}'
                 '.bub{animation:bub 5s ease-in infinite;}@keyframes bub{0%{transform:none;opacity:0;}15%{opacity:1;}100%{transform:translateY(-200px);opacity:0;}}'
                 '.fl{animation:fl 5s ease-in-out infinite;}@keyframes fl{0%,100%{transform:none;}50%{transform:translateY(-8px);}}')
    o = [f'<rect width="560" height="440" fill="{ROOM_ON}"/><rect width="560" height="440" fill="url(#pg)"/>',
         f'<rect x="56" y="78" width="370" height="260" rx="12" fill="#181b20" stroke="rgba(237,228,211,.22)"/>',
         f'<line x1="56" y1="108" x2="426" y2="108" stroke="{LINE}"/>']
    o += [f'<circle cx="{74+i*12}" cy="93" r="3.5" fill="rgba(237,228,211,.22)"/>' for i in range(3)]
    o.append(f'<rect x="352" y="84" width="62" height="18" rx="9" fill="none" stroke="{LINE}"/>'
             f'<rect class="lg" x="354" y="86" width="28" height="14" rx="7" fill="rgba(214,178,115,.45)"/>'
             + s.text(368, 97, 'FR', 'M', 9, CREAM, anchor='middle') + s.text(398, 97, 'EN', 'M', 9, CREAM, anchor='middle'))
    o.append('<rect x="92" y="150" width="210" height="15" rx="7.5" fill="rgba(237,228,211,.3)"/>'
             '<rect x="92" y="180" width="280" height="8" rx="4" fill="rgba(237,228,211,.13)"/>'
             '<rect x="92" y="198" width="220" height="8" rx="4" fill="rgba(237,228,211,.13)"/>'
             '<rect x="92" y="226" width="120" height="20" rx="10" fill="url(#brass)"/>')
    o.append('<g clip-path="url(#brw)">' + ''.join(
        f'<circle class="bub" style="animation-delay:{dl}s" cx="{cx}" cy="350" r="{r}" fill="none" stroke="rgba(237,228,211,.4)"/>'
        for cx, r, dl in ((130, 4, 0), (210, 3, 1.4), (300, 5, 2.6), (170, 6, 3.4), (350, 3.5, 4.1))) + '</g>')
    o.append('<g class="fl"><rect x="390" y="168" width="112" height="216" rx="18" fill="#1d2026" stroke="rgba(237,228,211,.25)"/>'
             '<rect x="408" y="206" width="60" height="11" rx="5.5" fill="rgba(237,228,211,.3)"/>'
             '<rect x="408" y="228" width="76" height="7" rx="3.5" fill="rgba(237,228,211,.13)"/>'
             '<rect x="408" y="243" width="56" height="7" rx="3.5" fill="rgba(237,228,211,.13)"/>'
             '<rect x="408" y="264" width="54" height="14" rx="7" fill="url(#brass)"/></g>')
    return ''.join(o)


def v_archive(s):
    s.defs.append('<linearGradient id="cab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2d33"/><stop offset="1" stop-color="#1f2227"/></linearGradient>'
                  '<linearGradient id="drw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#363a41"/><stop offset="1" stop-color="#2a2d33"/></linearGradient>')
    s.css.append('.dr{animation:dr 5s cubic-bezier(.22,1,.36,1) infinite;}@keyframes dr{0%,20%{transform:none;}40%,75%{transform:translateX(40px);}95%,100%{transform:none;}}')
    o = [f'<rect width="560" height="440" fill="{ROOM_ON}"/>',
         '<rect x="150" y="62" width="200" height="300" rx="16" fill="url(#cab)" stroke="rgba(237,228,211,.22)"/>']
    for i, lab in enumerate(['A–F', 'G–M', 'N–Z']):
        y = 76 + i * 94
        cls = ' class="dr"' if i == 1 else ''
        o.append(f'<g{cls}><rect x="164" y="{y}" width="172" height="82" rx="9" fill="url(#drw)" stroke="rgba(237,228,211,.1)"/>'
                 f'<rect x="230" y="{y+38}" width="40" height="7" rx="3.5" fill="url(#brass)"/>'
                 + s.text(176, y + 20, lab, 'M', 10.5, MUTED) + '</g>')
    tree = [('▾ Armoire', 0, CREAM2), ('▾ Dossier', 16, MUTED), ('▸ Document', 32, MUTED)]
    for i, (t, ind, c) in enumerate(tree):
        o.append(s.text(384 + ind, 96 + i * 22, t, 'M', 11.5, c))
    o.append(f'<circle class="blink" cx="46" cy="400" r="4.5" fill="{LIVE}"/>' + s.text(60, 404, 'NAS · STOCKAGE SÉCURISÉ', 'M', 11, BRASS, ls=1.6))
    return ''.join(o)


def v_hm(s):
    s.defs.append('<pattern id="ln" width="560" height="24" patternUnits="userSpaceOnUse"><path d="M0 .5H560" stroke="rgba(237,228,211,.05)"/></pattern>')
    s.css.append('.cl{animation:cl 4.5s ease-in-out infinite;}@keyframes cl{0%,100%{opacity:.35;}40%,60%{opacity:1;}}'
                 '.ck{animation:ck 6s infinite;}@keyframes ck{0%,35%{opacity:0;}45%,90%{opacity:1;}100%{opacity:0;}}')
    o = [f'<rect width="560" height="440" fill="{ROOM_ON}"/><rect width="560" height="440" fill="url(#ln)"/>']
    x0, cw, g = 112, 60, 8
    o.append(s.text(x0, 92, 'EMPLOI DU TEMPS', 'M', 11, MUTED, ls=2) + s.text(x0 + 5 * cw + 4 * g, 92, 'TP', 'M', 11, MUTED, anchor='end', ls=2))
    for i, L in enumerate('LMMJV'):
        o.append(s.text(x0 + i * (cw + g) + cw / 2, 122, L, 'M', 10.5, MUTED, anchor='middle'))
    grid = ['o.a.o', '.ao..', 'o..ao']
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            x, y = x0 + c * (cw + g), 134 + r * 38
            fill, st = {'o': ('rgba(214,178,115,.55)', 'rgba(214,178,115,.7)'), 'a': ('rgba(143,167,160,.45)', 'rgba(143,167,160,.6)'),
                        '.': ('rgba(237,228,211,.06)', 'rgba(237,228,211,.08)')}[v]
            cls = f' class="cl" style="animation-delay:{(r*5+c)*.22:.2f}s"' if v != '.' else ''
            o.append(f'<rect{cls} x="{x}" y="{y}" width="{cw}" height="28" rx="6" fill="{fill}" stroke="{st}"/>')
    items = [('Travaux pratiques', True), ('Emploi du temps', True), ('Ressources pédagogiques', False)]
    for i, (t, done) in enumerate(items):
        y = 278 + i * 30
        o.append(f'<rect x="{x0}" y="{y-12}" width="15" height="15" rx="3.5" fill="{BRASS if done else "none"}" stroke="{BRASS if done else "rgba(237,228,211,.3)"}"/>')
        if not done:
            o.append(f'<rect class="ck" x="{x0}" y="{y-12}" width="15" height="15" rx="3.5" fill="{BRASS}"/>')
        o.append(f'<path{" class=\"ck\"" if not done else ""} d="M{x0+3.5} {y-4.5} l3 3 l5 -6" fill="none" stroke="#1b150b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(s.text(x0 + 26, y, t, 'N5', 14.5, CREAM2))
    return ''.join(o)


# ---------------------------------------------------------------- MÉMOIRE
def thesis():
    h = 520
    s = Svg(W, h, "Mémoire de Master 2 : Attribution de Shapley approchée pour Half-Space Trees — expliquer les scores d'anomalie en flux (Explainable AI).")
    brass_defs(s)
    s.css += [FADE,
              '.pt{animation:pt .5s both;}@keyframes pt{from{opacity:.25;}to{opacity:1;}}'
              '.rg{transform-box:fill-box;transform-origin:center;animation:rg 2.2s 1.6s ease-out infinite;}@keyframes rg{0%{transform:scale(1);opacity:1;}100%{transform:scale(1.9);opacity:0;}}'
              '.bp{transform-box:fill-box;transform-origin:left;animation:bx 1s cubic-bezier(.22,1,.36,1) both;}'
              '.bn{transform-box:fill-box;transform-origin:right;animation:bx 1s cubic-bezier(.22,1,.36,1) both;}'
              '@keyframes bx{from{transform:scaleX(0);}to{transform:none;}}']
    frame(s, W, h)
    vx = 600
    s.add('<g clip-path="url(#card)">', f'<rect x="{vx}" width="{W-vx}" height="{h}" fill="#0f1114"/>',
          f'<line x1="{vx}" y1="0" x2="{vx}" y2="{h}" stroke="{LINE}"/>')
    k, ox, oy = .9, vx + 22, 112
    v = [f'<g transform="translate({ox},{oy}) scale({k})">',
         s.text(30, 30, 'FLUX · PARTITIONS', 'M', 11, BRASS, ls=2.4),
         '<rect x="30" y="50" width="280" height="220" fill="none" stroke="rgba(237,228,211,.2)"/>']
    for x1, y1, x2, y2 in ((200, 50, 200, 270), (30, 130, 200, 130), (255, 50, 255, 130), (200, 210, 310, 210)):
        v.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(214,178,115,.45)" stroke-dasharray="3 4"/>')
    random.seed(7); pts = []
    while len(pts) < 46:
        x, y = random.gauss(118, 38), random.gauss(190, 34)
        if 38 < x < 300 and 136 < y < 264: pts.append((x, y))
    v += [f'<circle class="pt" style="animation-delay:{.3 + i*.02:.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="2.8" fill="rgba(237,228,211,.6)"/>' for i, (x, y) in enumerate(pts)]
    v.append(f'<circle class="pt" style="animation-delay:1.4s" cx="275" cy="82" r="4" fill="{BRASS3}"/>'
             f'<circle class="rg" cx="275" cy="82" r="11" fill="none" stroke="{BRASS3}" stroke-width="1.5"/>'
             f'<circle cx="275" cy="82" r="11" fill="none" stroke="{BRASS3}" stroke-width="1.5" class="pt" style="animation-delay:1.4s"/>'
             + s.text(212, 66, 'anomalie', 'M', 11, MUTED))
    v.append(s.text(350, 30, 'ATTRIBUTION · SCORE', 'M', 11, BRASS, ls=2.4)
             + '<line x1="480" y1="50" x2="480" y2="270" stroke="rgba(237,228,211,.2)"/>')
    for i, (lab, x, w, cls, col) in enumerate((('x1', 480, 118, 'bp', BRASS), ('x2', 480, 64, 'bp', BRASS),
                                                ('x3', 446, 34, 'bn', SAGE), ('x4', 480, 22, 'bp', BRASS))):
        y = 80 + i * 50
        v.append(s.text(356, y + 14, lab, 'M', 12, MUTED)
                 + f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="3" fill="{col}"/>')
    v.append('</g>')
    s.add(*v)
    s.add(s.text(vx + 30, h - 30, "Illustration schématique : un point isolé du flux et la contribution de chaque variable à son score.", 'N5', 12.5, MUTED), '</g>')
    x = 56
    s.add(f'<g class="up"{d(.1)}>' + s.text(x, 74, 'MÉMOIRE DE MASTER 2 · 2026', 'M', 13, BRASS, ls=2.6) + '</g>')
    s.add(f'<g class="up"{d(.2)}>' + s.text(x - 2, 134, 'Attribution de Shapley', 'S', 46, CREAM, ls=-.6)
          + s.text(x - 2, 184, 'approchée pour', 'S', 46, CREAM, ls=-.6)
          + s.text(x - 2, 234, 'Half-Space Trees', 'SI', 46, 'url(#brass)', ls=-.6) + '</g>')
    s.add(f'<g class="up"{d(.3)}>' + s.text(x, 274, 'Master 2 Business Intelligence · UCAD, FST', 'N7', 15.5, CREAM) + '</g>')
    lines = wrap("Étude et conception d'une méthode d'attribution approchée visant à expliquer les scores d'anomalie produits par les Half-Space Trees dans un contexte de données en flux.", 'N5', 16, 488)
    s.add(f'<g class="up"{d(.4)}>' + ''.join(s.text(x, 312 + i * 25, l, 'N5', 16, CREAM2) for i, l in enumerate(lines)) + '</g>')
    p, ph = s.pills(x, 312 + len(lines) * 25, ['Explainable AI', "Détection d'anomalies", 'Data Stream Learning', 'Machine Learning'], 488)
    s.add(f'<g class="up"{d(.5)}>{p}</g>')
    assert 312 + len(lines) * 25 + ph < h - 30
    border(s, W, h)
    return s


# ---------------------------------------------------------------- PARCOURS
TIMELINE = [
    ('2026', 'Expérience', 'Développeur Fullstack', 'SIAGE Conseils, Dakar'),
    ('2026', 'Formation', 'Parcours en Intelligence Artificielle', 'Sonatel Academy · Orange Digital Center, Dakar'),
    ('2026', 'Formation', 'Master 2 Business Intelligence', 'Université Cheikh Anta Diop de Dakar, FST'),
    ('2025', 'Enseignement', 'Chargé de formation, IA & Programmation', "Centre d'Énergie Solaire, d'Hygiène et de la Formation Professionnelle"),
    ('2025', 'Engagement', 'Trésorier', 'Club des Étudiants de la Section Informatique'),
    ('2025', 'Formation', "Master 1 Systèmes d'Information Répartis", 'Université Cheikh Anta Diop de Dakar, FST'),
    ('2023 – 2025', 'Enseignement', 'Enseignant vacataire en informatique (BTS)', 'Institut International des Technologies et du Management'),
    ('2024', 'Formation', 'Licence Informatique', 'Université Cheikh Anta Diop de Dakar, FST'),
    ('2023', 'Enseignement', 'Chargé de formation Bureautique & Développement Web', 'Business Academy Formation'),
    ('2020', 'Formation', 'Baccalauréat S2, Sciences Expérimentales', 'Académia Limamoulaye, Dakar'),
]


def timeline():
    items = TIMELINE
    step, top = 76, 70
    h = top + len(items) * step + 20
    s = Svg(W, h, 'Parcours : ' + ' ; '.join(f'{a} — {c}, {o}' for a, _, c, o in items))
    s.css += [FADE, '.rail{stroke-dasharray:2000;stroke-dashoffset:2000;animation:rail 2.4s .2s cubic-bezier(.22,1,.36,1) forwards;}'
                    '@keyframes rail{to{stroke-dashoffset:0;}}']
    frame(s, W, h)
    rx = 262
    s.add(f'<line x1="{rx}" y1="{top-14}" x2="{rx}" y2="{h-40}" stroke="{LINE}"/>',
          f'<line class="rail" x1="{rx}" y1="{top-14}" x2="{rx}" y2="{h-40}" stroke="{BRASS}" stroke-width="1.5"/>')
    for i, (date, kind, title, org) in enumerate(items):
        y = top + i * step
        dl = .25 + i * .12
        if kind == 'Formation':
            mark = f'<rect x="{rx-5.5}" y="{y-5.5}" width="11" height="11" transform="rotate(45 {rx} {y})" fill="{ROOM_OFF}" stroke="{BRASS}" stroke-width="1.5"/>'
        elif kind == 'Engagement':
            mark = f'<circle cx="{rx}" cy="{y}" r="5.5" fill="{ROOM_OFF}" stroke="{SAGE}" stroke-width="1.5"/>'
        else:
            mark = f'<circle cx="{rx}" cy="{y}" r="6" fill="{BRASS}"/>'
        s.add(f'<g class="up"{d(dl)}>', mark,
              s.text(rx - 34, y + 5, date, 'M', 14, BRASS, anchor='end', ls=.6),
              s.text(rx - 34, y + 26, kind.upper(), 'N7', 10.5, MUTED, anchor='end', ls=1.6),
              s.text(rx + 34, y + 8, title, 'S', 28, CREAM, ls=-.3),
              s.text(rx + 34, y + 32, org, 'N5', 15, MUTED), '</g>')
    border(s, W, h)
    return s


# ---------------------------------------------------------------- COMPÉTENCES
STACK = [
    ('Data, IA & BI', ['Python', 'Pandas', 'NumPy', 'scikit-learn', 'Streamlit', 'Machine Learning', 'Deep Learning', 'NLP', 'LLM', 'IA générative', 'Excel avancé (Power Query, Power Pivot)'], 5),
    ('Microsoft Fabric & Cloud Data', ['Microsoft Fabric', 'Power BI', 'Data Factory', 'Lakehouse', 'Data Warehouse', 'ETL / ELT'], 2),
    ('Bases de données', ['SQL', 'PostgreSQL', 'MySQL', 'SQL Server', 'Oracle', 'MongoDB', 'Modélisation de données'], 1),
    ('Développement & API', ['Node.js', 'API REST', 'PHP', 'Java JEE', 'JavaScript', 'HTML / CSS'], 2),
    ('DevOps & Outils', ['Docker', 'Git', 'GitHub', 'GitLab', 'Linux'], 2),
    ('Conception & Collaboration', ['BPMN', 'UML', 'Figma', 'Trello'], 0),
]


def stack():
    groups = STACK
    s = Svg(W, 10, 'Compétences : ' + ' ; '.join(f'{g} — {", ".join(t)}' for g, t, _ in groups))
    s.css.append(FADE)
    tx, tw, y, rows = 470, W - 470 - 48, 40, []
    for i, (g, tags, key) in enumerate(groups):
        out, cx, cy = [], tx, y
        for j, t in enumerate(tags):
            kw = dict(stroke='rgba(214,178,115,.55)', color=CREAM) if j < key else {}
            w = measure(t, 'N5', 13.5) + 28
            if cx + w > tx + tw and cx > tx: cx, cy = tx, cy + 42
            p, w = s.pill(cx, cy, t, size=13.5, pad=14, h=32, **kw); out.append(p); cx += w + 8
        th = cy + 32 - y
        nl = wrap(g, 'S', 31, 360)
        nh = len(nl) * 36
        rh = max(th, nh) + 40
        ny = y + (th - nh) / 2 + 26 if th > nh else y + 26
        rows.append(f'<g class="up"{d(.1 + i * .1)}>'
                    + s.text(48, ny, f'0{i+1}', 'M', 12, BRASS)
                    + ''.join(s.text(88, ny + 2 + k * 36, l, 'S', 31, CREAM, ls=-.3) for k, l in enumerate(nl))
                    + ''.join(out) + (f'<line x1="48" y1="{y + rh - 20}" x2="{W-48}" y2="{y + rh - 20}" stroke="{LINE}"/>' if i < len(groups) - 1 else '')
                    + '</g>')
        y += rh
    s.h = int(y + 10)
    frame(s, W, s.h)
    s.add(*rows)
    border(s, W, s.h)
    return s


# ---------------------------------------------------------------- CONTACT
def footer():
    h = 330
    s = Svg(W, h, 'Parlons données — roonmbaye5@gmail.com — Dakar, Sénégal')
    brass_defs(s)
    s.defs.append('<radialGradient id="halo" gradientUnits="userSpaceOnUse" cx="990" cy="120" r="460">'
                  '<stop offset="0" stop-color="rgb(255,200,130)" stop-opacity=".26"/><stop offset=".45" stop-color="rgb(255,200,130)" stop-opacity=".06"/>'
                  '<stop offset="1" stop-color="rgb(255,200,130)" stop-opacity="0"/></radialGradient>')
    s.css += [LAMP_CSS, FADE]
    frame(s, W, h)
    s.add('<g clip-path="url(#card)">', f'<rect class="on" width="{W}" height="{h}" fill="{ROOM_ON}"/>',
          f'<rect class="on" width="{W}" height="{h}" fill="url(#halo)"/>', lamp(s, 905, 34, .78), '</g>')
    s.add(f'<g class="up"{d(.1)}>' + s.text(64, 82, '06 — CONTACT', 'M', 14, BRASS, ls=3.5) + '</g>')
    x2 = measure('Parlons ', 'S', 104, -2) + 60
    s.add(f'<g class="up"{d(.2)}>' + s.text(60, 186, 'Parlons', 'S', 104, CREAM, ls=-2)
          + s.text(x2, 186, 'données.', 'SI', 104, 'url(#brass)', ls=-2) + '</g>')
    s.add(f'<g class="up"{d(.35)}>' + icon('mail', 64, 222, 22, BRASS3) + s.text(98, 241, 'roonmbaye5@gmail.com', 'N7', 22, CREAM) + '</g>')
    s.add(f'<g class="up"{d(.45)}>' + s.text(64, 282, 'Dakar, Sénégal · harouna-mbaye.netlify.app', 'N5', 16, MUTED) + '</g>')
    border(s, W, h)
    return s


# ---------------------------------------------------------------- ASSEMBLAGE
PROJECTS = [
    ('teranga', 'P.01', 'Étude de cas · BI', 'Teranga Shop', 'Entrepôt de données e-commerce',
     "Entrepôt modélisé en Data Vault 2.0 sur Microsoft Fabric : ingestion dans OneLake, chargement PySpark insert-only (hubs, links, satellites), orchestration Data Factory, restitution Power BI en Direct Lake.",
     ['Data Vault 2.0', 'Microsoft Fabric', 'Data Factory', 'Lakehouse', 'PySpark', 'Power BI'], ('Code sur GitHub', False), v_teranga),
    ('esenguide', 'P.02', 'IA générative', 'eSenGuide', "Assistant administratif basé sur l'IA",
     "Assistant conversationnel qui guide les citoyens sénégalais dans leurs démarches administratives : CNI, casier judiciaire, certificat de résidence… De l'idée à un produit déployé.",
     ['LLM · Llama 3.3 70B (Groq)', 'React', 'FastAPI'], ('En ligne · esenguide.vercel.app', True), v_esen),
    ('ceedrt', 'P.03', 'Plateforme web · client réel', 'CEEDRT', 'Plateforme pour une organisation réelle',
     "Conception et développement de la plateforme web du Collectif des Élèves et Étudiants pour le Développement de la Région de Tambacounda, mené de bout en bout.",
     ['Plateforme web', 'Organisation réelle', 'Conception complète'], ('En ligne · ceedrt.com', True), v_ceedrt),
    ('storm', 'P.04', 'Big Data · temps réel', 'Apache Storm', 'Traitement de flux en temps réel',
     "Traitement de flux de données en temps réel dans le Big Data : topologie distribuée de spouts et de bolts intégrée dans un pipeline continu.",
     ['Apache Storm', 'Python', 'MongoDB', 'Streaming'], ('Code sur GitHub', False), v_storm),
    ('prestige', 'P.05', 'Site vitrine · client réel', 'Prestige Lavage', 'Lavage automobile premium à Saly',
     "Site vitrine bilingue et responsive livré pour un client réel, sans base de données ni serveur : simple, rapide et sécurisé.",
     ['Site statique', 'Bilingue FR / EN', 'Responsive', 'Thème clair / sombre'], ('En ligne · prestigelavage.com', True), v_prestige),
    ('archivedocpro', 'P.06', 'GED', 'ArchiveDocPro', 'Gestion électronique de documents',
     "Solution de GED avec armoire virtuelle interactive, hiérarchie documentaire et stockage sécurisé sur un NAS.",
     ['GED', 'Armoire virtuelle', 'Hiérarchie documentaire', 'NAS'], (None, False), v_archive),
    ('hmeducation', 'P.07', 'Plateforme éducative', 'HM Education', 'Gestion des TP et des emplois du temps',
     "Plateforme responsive qui aide les étudiants à gérer leurs TP, consulter leur emploi du temps et accéder aux ressources pédagogiques.",
     ['PHP', 'JavaScript', 'Responsive'], ('En ligne', True), v_hm),
]

HEADERS = (('01', 'apport', "Ce que j'apporte", 'De la donnée brute', 'à la décision.'), ('02', 'projets', 'Projets', 'Sept projets,', 'sept façons de les montrer.'), ('03', 'recherche', 'Recherche', 'Rendre l’IA', 'explicable.'), ('04', 'parcours', 'Parcours', 'De la licence', 'au terrain.'), ('05', 'stack', 'Compétences', 'Une boîte à outils,', 'du modèle au tableau de bord.'))

sizes = {}


def save(name, svg):
    sizes[name] = svg.save(os.path.join(OUT, name + '.svg'))


def main():

    save('hero', hero())
    save('btn-portfolio', button('Voir mon portfolio', 'globe', primary=True))
    save('btn-email', button('Email', 'mail'))
    save('btn-linkedin', button('LinkedIn', 'linkedin'))
    save('btn-whatsapp', button('WhatsApp', 'phone'))
    save('values', values())
    for i, (key, idx, kind, title, sub, desc, tags, status, vis) in enumerate(PROJECTS):
        save(f'p-{key}', project(key, idx, kind, title, sub, desc, tags, status, vis, 'left' if i % 2 == 0 else 'right'))
    save('thesis', thesis())
    save('timeline', timeline())
    save('stack', stack())
    save('footer', footer())
    for k, v in sizes.items():
        print(f'{k:24s} {v/1024:6.1f} Ko')
    print('TOTAL', round(sum(sizes.values()) / 1024), 'Ko')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    main()
