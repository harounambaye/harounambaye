"""Versions mobiles (440 px de large) des visuels du README.

Sur un téléphone, GitHub affiche le README sur ~360 px : une carte de 1200 px y serait réduite
au tiers et son texte deviendrait illisible. Le README sert ces variantes via
<source media="(max-width: 600px)">. Même contenu que build.py, mise en page empilée.
"""
import os, random, sys
from svgkit import Svg, measure, wrap, icon, ROOM_OFF, ROOM_ON, CREAM, CREAM2, MUTED, BRASS, BRASS3, LINE, SAGE, LIVE
from build import (FADE, LAMP_CSS, frame, border, d, brass_defs, lamp, PROJECTS, VALUES, TIMELINE, STACK, HEADERS)

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
MW, P = 440, 24          # largeur, marge intérieure
CW = MW - 2 * P          # largeur utile


def m_header(num, eyebrow, plain, italic, theme, width=760, size=54):
    """En-tête de section (affiché à sa taille naturelle, il se réduit seul sur mobile)."""
    ink, acc, line = (CREAM, BRASS3, BRASS) if theme == 'dark' else (ROOM_OFF, '#7a5a2e', '#8a6430')
    # Le titre s'écrit d'une traite (partie droite puis italique) et passe à la ligne si besoin
    words = [(w, 'S', ink) for w in plain.split()] + [(w, 'SI', acc) for w in italic.split()]
    lines, cur, cw = [], [], 0
    for w, f, c in words:
        ww = measure(w + ' ', f, size, -1)
        if cur and cw + measure(w, f, size, -1) > width - 8:
            lines.append(cur); cur, cw = [], 0
        cur.append((w, f, c, cw)); cw += ww
    lines.append(cur)
    lh = size * 1.06
    h = int(size * 1.85 + (len(lines) - 1) * lh + 24)
    s = Svg(width, h, f'{num} — {eyebrow}. {plain} {italic}')
    s.css.append(FADE)
    s.add(f'<g class="up"><line x1="2" y1="35" x2="28" y2="35" stroke="{line}" stroke-width="1.2"/>'
          + s.text(40, 40, f'{num} — {eyebrow.upper()}', 'M', 13, line, ls=3.2) + '</g>')
    out = []
    for i, ln in enumerate(lines):
        y = size * 1.85 + i * lh
        out += [s.text(x, y, w, f, size, c, ls=-1) for w, f, c, x in ln]
    s.add(f'<g class="up"{d(.12)}>' + ''.join(out) + '</g>')
    return s


def m_hero():
    h = 600
    s = Svg(MW, h, "Harouna MBAYE — Data Scientist & BI Analyst, spécialisé en IA. Dakar, Sénégal.")
    brass_defs(s)
    s.defs.append('<radialGradient id="halo" gradientUnits="userSpaceOnUse" cx="345" cy="100" r="380">'
                  '<stop offset="0" stop-color="rgb(255,200,130)" stop-opacity=".32"/>'
                  '<stop offset=".45" stop-color="rgb(255,200,130)" stop-opacity=".08"/>'
                  '<stop offset="1" stop-color="rgb(255,200,130)" stop-opacity="0"/></radialGradient>')
    s.css += [LAMP_CSS, FADE, '.ring{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out infinite;}'
              '@keyframes ring{from{transform:scale(1);opacity:.7;}to{transform:scale(2.6);opacity:0;}}']
    frame(s, MW, h)
    s.add('<g clip-path="url(#card)">', f'<rect class="on" width="{MW}" height="{h}" fill="{ROOM_ON}"/>',
          f'<rect class="on" width="{MW}" height="{h}" fill="url(#halo)"/>', lamp(s, 262, 22, .66), '</g>')
    s.add(f'<g class="up"{d(.1)}><line x1="{P}" y1="55" x2="{P+22}" y2="55" stroke="{BRASS}" stroke-width="1.2"/>'
          + s.text(P + 32, 60, 'DAKAR · SÉNÉGAL', 'M', 12, BRASS, ls=3) + '</g>')
    s.add(f'<g class="up"{d(.2)}>' + s.text(P - 3, 330, 'Harouna', 'S', 90, CREAM, ls=-2) + '</g>')
    s.add(f'<g class="up"{d(.3)}>' + s.text(P + 3, 414, 'MBAYE', 'SI', 90, 'url(#brass)', ls=-1) + '</g>')
    s.add(f'<g class="up"{d(.45)}>' + s.text(P, 462, 'Data Scientist & BI Analyst', 'N7', 23, CREAM, ls=-.3) + '</g>')
    sub = wrap('Intelligence Artificielle · Machine Learning · Deep Learning · XAI', 'N5', 15.5, CW)
    s.add(f'<g class="up"{d(.55)}>' + ''.join(s.text(P, 492 + i * 22, l, 'N5', 15.5, MUTED) for i, l in enumerate(sub)) + '</g>')
    label = 'Ouvert à un poste · Data · BI · IA'
    pw = measure(label, 'N7', 14) + 58
    py = h - 62
    s.add(f'<g class="up"{d(1.4)}><rect x="{P}" y="{py}" width="{pw:.1f}" height="38" rx="19" fill="rgba(18,20,23,.75)" stroke="rgba(214,178,115,.55)"/>'
          f'<circle class="ring" cx="{P+22}" cy="{py+19}" r="4.5" fill="{LIVE}"/><circle cx="{P+22}" cy="{py+19}" r="4.5" fill="{LIVE}"/>'
          + s.text(P + 38, py + 24, label, 'N7', 14, CREAM) + '</g>')
    border(s, MW, h)
    return s


def m_values():
    cards, y = [], 0
    s = Svg(MW, 10, "Ce que j'apporte : " + ' ; '.join(f'{t} — {x}' for _, t, x, _ in VALUES))
    s.css.append(FADE)
    for i, (n, t, txt, tag) in enumerate(VALUES):
        lines = wrap(txt, 'N5', 16, CW)
        ch = 82 + len(lines) * 24 + 40
        g = [f'<g class="up"{d(.1 + i * .1)}>',
             f'<rect x=".5" y="{y+.5}" width="{MW-1}" height="{ch-1}" rx="22" fill="{ROOM_OFF}" stroke="{LINE}"/>',
             s.text(P, y + 50, n, 'M', 12.5, BRASS, ls=2), s.text(P + 38, y + 54, t, 'S', 34, CREAM, ls=-.4)]
        g += [s.text(P, y + 86 + j * 24, l, 'N5', 16, CREAM2) for j, l in enumerate(lines)]
        g += [s.text(P, y + ch - 24, tag, 'M', 11.5, BRASS, ls=1.6), '</g>']
        cards.append(''.join(g)); y += ch + 14
    s.h = int(y - 14)
    s.add(*cards)
    return s


def m_project(key, idx, kind, title, sub, desc, tags, status, visual):
    vh, k = 346, MW / 560
    s = Svg(MW, 10, f'{title} — {sub}. {desc} Stack : {", ".join(tags)}.')
    brass_defs(s)
    s.css += [FADE, '.blink{animation:blink 1.4s infinite;}@keyframes blink{0%,100%{opacity:.25;}50%{opacity:1;}}']
    y = vh + 46
    parts = [s.text(P, y, f'{idx} — {kind.upper()}', 'M', 12, BRASS, ls=2.2)]
    y += 50
    parts.append(s.text(P - 2, y, title, 'S', 44, CREAM, ls=-.6))
    if sub:
        for l in wrap(sub, 'N7', 17, CW):
            y += 30; parts.append(s.text(P, y, l, 'N7', 17, CREAM))
    y += 12
    for l in wrap(desc, 'N5', 16, CW):
        y += 25; parts.append(s.text(P, y, l, 'N5', 16, CREAM2))
    y += 20
    p, ph = s.pills(P, y, tags, CW, size=12.5, h=30)
    parts.append(p); y += ph
    label, live = status
    if label:
        y += 40
        dot = (f'<circle class="blink" cx="{P+5}" cy="{y-4}" r="4.5" fill="{LIVE}"/>' if live
               else f'<circle cx="{P+5}" cy="{y-4}" r="4" fill="none" stroke="{BRASS}" stroke-width="1.4"/>')
        parts.append(dot + s.text(P + 20, y, label.upper(), 'M', 11.5, CREAM2 if live else MUTED, ls=1.4))
    s.h = int(y + 34)
    frame(s, MW, s.h)
    s.add('<g clip-path="url(#card)">', f'<g transform="scale({k:.5f})">', visual(s), '</g>',
          f'<line x1="0" y1="{vh}" x2="{MW}" y2="{vh}" stroke="{LINE}"/></g>')
    s.add(f'<g class="up"{d(.2)}>', *parts, '</g>')
    border(s, MW, s.h)
    return s


def hst(s):
    """Schéma Half-Space Trees + attributions (repère 640x300, comme la version bureau)."""
    v = [s.text(30, 30, 'FLUX · PARTITIONS', 'M', 13, BRASS, ls=2.4),
         '<rect x="30" y="50" width="280" height="220" fill="none" stroke="rgba(237,228,211,.2)"/>']
    for x1, y1, x2, y2 in ((200, 50, 200, 270), (30, 130, 200, 130), (255, 50, 255, 130), (200, 210, 310, 210)):
        v.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(214,178,115,.45)" stroke-dasharray="3 4"/>')
    random.seed(7); pts = []
    while len(pts) < 46:
        x, y = random.gauss(118, 38), random.gauss(190, 34)
        if 38 < x < 300 and 136 < y < 264: pts.append((x, y))
    v += [f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="rgba(237,228,211,.6)"/>' for x, y in pts]
    v.append(f'<circle cx="275" cy="82" r="4.5" fill="{BRASS3}"/><circle class="rg" cx="275" cy="82" r="12" fill="none" stroke="{BRASS3}" stroke-width="1.6"/>'
             f'<circle cx="275" cy="82" r="12" fill="none" stroke="{BRASS3}" stroke-width="1.6"/>')
    v.append(s.text(350, 30, 'ATTRIBUTION', 'M', 13, BRASS, ls=2.4) + '<line x1="480" y1="50" x2="480" y2="270" stroke="rgba(237,228,211,.2)"/>')
    for i, (lab, x, w, col) in enumerate((('x1', 480, 118, BRASS), ('x2', 480, 64, BRASS), ('x3', 446, 34, SAGE), ('x4', 480, 22, BRASS))):
        y = 80 + i * 50
        v.append(s.text(356, y + 15, lab, 'M', 14, MUTED) + f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="3" fill="{col}"/>')
    return ''.join(v)


def m_thesis():
    s = Svg(MW, 10, "Mémoire de Master 2 : Attribution de Shapley approchée pour Half-Space Trees — expliquer les scores d'anomalie en flux.")
    brass_defs(s)
    s.css += [FADE, '.rg{transform-box:fill-box;transform-origin:center;animation:rg 2.2s ease-out infinite;}'
                    '@keyframes rg{0%{transform:scale(1);opacity:1;}100%{transform:scale(1.9);opacity:0;}}']
    y = 50
    parts = [s.text(P, y, 'MÉMOIRE DE MASTER 2 · 2026', 'M', 12, BRASS, ls=2.2)]
    for t, f, c in (('Attribution de Shapley', 'S', CREAM), ('approchée pour', 'S', CREAM), ('Half-Space Trees', 'SI', 'url(#brass)')):
        y += 44; parts.append(s.text(P - 2, y, t, f, 38, c, ls=-.5))
    for l in wrap('Master 2 Business Intelligence · UCAD, FST', 'N7', 15, CW):
        y += 32; parts.append(s.text(P, y, l, 'N7', 15, CREAM))
    y += 8
    for l in wrap("Étude et conception d'une méthode d'attribution approchée visant à expliquer les scores d'anomalie produits par les Half-Space Trees dans un contexte de données en flux.", 'N5', 16, CW):
        y += 25; parts.append(s.text(P, y, l, 'N5', 16, CREAM2))
    y += 20
    p, ph = s.pills(P, y, ['Explainable AI', "Détection d'anomalies", 'Data Stream Learning', 'Machine Learning'], CW, size=12.5)
    parts.append(p); y += ph + 28
    vy, vk = y, (MW - 16) / 640
    vh = 300 * vk + 24
    cap = wrap("Illustration schématique : un point isolé du flux et la contribution de chaque variable à son score.", 'N5', 12.5, CW)
    s.h = int(vy + vh + 18 + len(cap) * 18 + 18)
    frame(s, MW, s.h)
    s.add('<g clip-path="url(#card)">', f'<rect y="{vy}" width="{MW}" height="{s.h - vy}" fill="#0f1114"/>',
          f'<line x1="0" y1="{vy}" x2="{MW}" y2="{vy}" stroke="{LINE}"/>',
          f'<g transform="translate(0,{vy + 12}) scale({vk:.5f})">', hst(s), '</g>',
          ''.join(s.text(P, vy + vh + 18 + i * 18, l, 'N5', 12.5, MUTED) for i, l in enumerate(cap)), '</g>')
    s.add(f'<g class="up"{d(.15)}>', *parts, '</g>')
    border(s, MW, s.h)
    return s


def m_timeline():
    s = Svg(MW, 10, 'Parcours : ' + ' ; '.join(f'{a} — {c}, {o}' for a, _, c, o in TIMELINE))
    s.css += [FADE, '.rail{stroke-dasharray:3000;stroke-dashoffset:3000;animation:rail 2.4s .2s cubic-bezier(.22,1,.36,1) forwards;}'
                    '@keyframes rail{to{stroke-dashoffset:0;}}']
    rx, tx, tw = 34, 60, MW - 60 - P
    y, items = 46, []
    for i, (date, kind, title, org) in enumerate(TIMELINE):
        if kind == 'Formation':
            mark = f'<rect x="{rx-5}" y="{y-9}" width="10" height="10" transform="rotate(45 {rx} {y-4})" fill="{ROOM_OFF}" stroke="{BRASS}" stroke-width="1.5"/>'
        elif kind == 'Engagement':
            mark = f'<circle cx="{rx}" cy="{y-4}" r="5" fill="{ROOM_OFF}" stroke="{SAGE}" stroke-width="1.5"/>'
        else:
            mark = f'<circle cx="{rx}" cy="{y-4}" r="5.5" fill="{BRASS}"/>'
        dw = measure(date, 'M', 13, .5)
        g = [f'<g class="up"{d(.2 + i * .08)}>', mark, s.text(tx, y, date, 'M', 13, BRASS, ls=.5),
             s.text(tx + dw + 12, y, kind.upper(), 'N7', 10, MUTED, ls=1.4)]
        for l in wrap(title, 'S', 25, tw):
            y += 29; g.append(s.text(tx, y, l, 'S', 25, CREAM, ls=-.3))
        for l in wrap(org, 'N5', 14.5, tw):
            y += 21; g.append(s.text(tx, y, l, 'N5', 14.5, MUTED))
        g.append('</g>'); items.append(''.join(g))
        y += 40
    s.h = int(y - 10)
    frame(s, MW, s.h)
    s.add(f'<line x1="{rx}" y1="30" x2="{rx}" y2="{s.h - 30}" stroke="{LINE}"/>',
          f'<line class="rail" x1="{rx}" y1="30" x2="{rx}" y2="{s.h - 30}" stroke="{BRASS}" stroke-width="1.5"/>', *items)
    border(s, MW, s.h)
    return s


def m_stack():
    s = Svg(MW, 10, 'Compétences : ' + ' ; '.join(f'{g} — {", ".join(t)}' for g, t, _ in STACK))
    s.css.append(FADE)
    y, rows = 52, []
    for i, (g, tags, key) in enumerate(STACK):
        parts = [s.text(P, y, f'0{i+1}', 'M', 12, BRASS)]
        for j, l in enumerate(wrap(g, 'S', 27, CW - 36)):
            parts.append(s.text(P + 34, y + 2 + j * 32, l, 'S', 27, CREAM, ls=-.3))
        y += 2 + (len(wrap(g, 'S', 27, CW - 36)) - 1) * 32 + 20
        out, cx, cy = [], P, y
        for j, t in enumerate(tags):
            kw = dict(stroke='rgba(214,178,115,.55)', color=CREAM) if j < key else {}
            w = measure(t, 'N5', 13) + 26
            if cx + w > P + CW and cx > P: cx, cy = P, cy + 40
            p, w = s.pill(cx, cy, t, size=13, pad=13, h=31, **kw); out.append(p); cx += w + 7
        y = cy + 31
        sep = f'<line x1="{P}" y1="{y + 24}" x2="{MW-P}" y2="{y + 24}" stroke="{LINE}"/>' if i < len(STACK) - 1 else ''
        rows.append(f'<g class="up"{d(.1 + i * .08)}>' + ''.join(parts) + ''.join(out) + sep + '</g>')
        y += 64
    s.h = int(y - 30)
    frame(s, MW, s.h)
    s.add(*rows)
    border(s, MW, s.h)
    return s


def m_footer():
    h = 390
    s = Svg(MW, h, 'Parlons données — roonmbaye5@gmail.com — Dakar, Sénégal')
    brass_defs(s)
    s.defs.append('<radialGradient id="halo" gradientUnits="userSpaceOnUse" cx="370" cy="70" r="320">'
                  '<stop offset="0" stop-color="rgb(255,200,130)" stop-opacity=".28"/><stop offset=".5" stop-color="rgb(255,200,130)" stop-opacity=".06"/>'
                  '<stop offset="1" stop-color="rgb(255,200,130)" stop-opacity="0"/></radialGradient>')
    s.css += [LAMP_CSS, FADE]
    frame(s, MW, h)
    s.add('<g clip-path="url(#card)">', f'<rect class="on" width="{MW}" height="{h}" fill="{ROOM_ON}"/>',
          f'<rect class="on" width="{MW}" height="{h}" fill="url(#halo)"/>', lamp(s, 305, 18, .48), '</g>')
    s.add(f'<g class="up"{d(.1)}>' + s.text(P, 58, '06 — CONTACT', 'M', 12.5, BRASS, ls=3) + '</g>')
    s.add(f'<g class="up"{d(.2)}>' + s.text(P - 3, 196, 'Parlons', 'S', 80, CREAM, ls=-2)
          + s.text(P - 3, 270, 'données.', 'SI', 80, 'url(#brass)', ls=-2) + '</g>')
    s.add(f'<g class="up"{d(.35)}>' + icon('mail', P, 302, 20, BRASS3) + s.text(P + 30, 319, 'roonmbaye5@gmail.com', 'N7', 19, CREAM) + '</g>')
    s.add(f'<g class="up"{d(.45)}>' + s.text(P, 352, 'Dakar, Sénégal', 'N5', 15, MUTED) + '</g>')
    border(s, MW, h)
    return s


def main():
    sizes = {}
    def save(name, svg):
        sizes[name] = svg.save(os.path.join(OUT, name + '-m.svg'))
    save('hero', m_hero())
    for num, key, eb, plain, it in HEADERS:
        for th in ('dark', 'light'):
            # en-têtes uniques (sans suffixe -m) : 760 px, réduits automatiquement sur mobile
            sizes[f'h-{key}-{th}'] = m_header(num, eb, plain, it, th).save(os.path.join(OUT, f'h-{key}-{th}.svg'))
    save('values', m_values())
    for key, idx, kind, title, sub, desc, tags, status, vis in PROJECTS:
        save(f'p-{key}', m_project(key, idx, kind, title, sub, desc, tags, status, vis))
    save('thesis', m_thesis())
    save('timeline', m_timeline())
    save('stack', m_stack())
    save('footer', m_footer())
    for k, v in sizes.items():
        print(f'{k:24s} {v/1024:6.1f} Ko')
    print('TOTAL mobile', round(sum(sizes.values()) / 1024), 'Ko')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    main()
