#!/usr/bin/env python3
"""Render the original anime observatory as self-contained GitHub image assets."""
import base64
from datetime import date, timedelta
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
INK = '#08121f'
SILVER = '#e8edf2'
GOLD = '#dbb277'
BLUE = '#a4d3ee'
MUTED = '#a7bacc'

STYLE = '''
text{font-family:Consolas,'Liberation Mono',monospace}
.serif{font-family:Georgia,'Liberation Serif',serif}
.camera{transform-origin:center;animation:camera 22s ease-in-out infinite alternate}
.flow{stroke-dasharray:10 210;animation:flow 10s linear infinite}
.fast{animation-duration:7s}.slow{animation-duration:13s}
.glow{animation:glow 8s ease-in-out infinite}
.rotor{transform-origin:1380px 223px;animation:rotor 48s linear infinite}
.trace{stroke-dasharray:600;animation:trace 11s ease-in-out infinite}
.meter{animation:meter 8s ease-in-out infinite}
@keyframes camera{to{transform:scale(1.025)}}
@keyframes flow{to{stroke-dashoffset:-660}}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:.9}}
@keyframes rotor{to{transform:rotate(360deg)}}
@keyframes trace{0%,12%{stroke-dashoffset:600;opacity:.35}55%,80%{stroke-dashoffset:0;opacity:.9}100%{stroke-dashoffset:-600;opacity:.35}}
@keyframes meter{0%,100%{opacity:.35}45%,65%{opacity:1}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.flow{stroke-dasharray:none;opacity:.4}.trace{stroke-dasharray:none;stroke-dashoffset:0}}
'''


def text(x, y, value, size=20, color=MUTED, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'


def document(width, height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><clipPath id="frame"><rect width="{width}" height="{height}"/></clipPath>
<linearGradient id="shade"><stop stop-color="#030b17" stop-opacity=".84"/><stop offset=".6" stop-color="#030b17" stop-opacity=".17"/><stop offset="1" stop-color="#030b17" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}"/></linearGradient></defs>
<style>{STYLE}</style><g clip-path="url(#frame)"><rect width="{width}" height="{height}" fill="{INK}"/>{body}</g></svg>'''


def bitmap(name):
    data = base64.b64encode((OUT / 'artwork' / 'observatory' / (name+'.jpg')).read_bytes()).decode()
    return f'<image href="data:image/jpeg;base64,{data}" width="2000" height="800" preserveAspectRatio="xMidYMid slice"/>'


def signals(name):
    if name == 'observatory':
        return '''<g fill="none" stroke="#c6e9ff" stroke-width="2"><path class="flow slow" d="M740 65Q940 130 1130 180T1390 220"/><path class="flow" style="animation-delay:-4s" d="M850 350Q1080 365 1210 280T1390 220"/><path class="flow slow" style="animation-delay:-7s" d="M1000 15Q1070 210 1390 220"/></g><g class="rotor" fill="none" stroke="#f4d4a0" stroke-width="1.2" opacity=".6"><circle cx="1380" cy="223" r="101" stroke-dasharray="2 18"/><path d="M1380 114v17M1489 223h-17M1380 332v-17M1271 223h17"/></g><g fill="#e9cb94"><circle cx="1390" cy="220" r="4" opacity=".7"><animate attributeName="opacity" values=".35;.9;.35" dur="9s" repeatCount="indefinite"/></circle><circle class="glow" cx="1125" cy="180" r="3"/><circle class="glow" style="animation-delay:-5s" cx="840" cy="87" r="2"/></g>'''
    if name == 'exchange':
        return '''<g fill="none" stroke="#b2e3ff" stroke-width="4"><path class="flow fast" d="M770 95L1310 240L2000 64"/><path class="flow" style="animation-delay:-3s" d="M770 276L1320 325L2000 245"/><path class="flow slow" style="animation-delay:-6s" d="M770 412L1335 400L2000 400"/></g>'''
    return '''<g fill="none" stroke="#b8e4ff" stroke-width="2"><path class="trace" d="M880 344L933 284L991 331L1035 300L1061 377L1001 430L936 409Z M933 284L936 409L1035 300M880 344L1061 377"/><circle class="glow" cx="974" cy="350" r="102" stroke-dasharray="3 19"/><path class="trace" style="animation-delay:-4s" d="M1215 347L1260 296L1310 347L1260 400Z"/><circle class="glow" style="animation-delay:-3s" cx="1440" cy="346" r="18" stroke="#e5bd7c"/></g>'''


def scene(name, mobile=False):
    specs = {
        'observatory': ('observatory', 'Med Gleiguem — the observatory', 'Original fictional coastal anime observatory at night. Still illustration with animated signals, instrument highlights and restrained scene drift.'),
        'exchange': ('exchange-hall', 'Data with a destination', 'Original anime data exchange hall. Three separately phased signal lanes are a visual metaphor for data acquisition and analytical structure, not throughput measurements.'),
        'identity': ('identity-atelier', 'Identity, then the next step', 'Original anime identity atelier. Synthetic landmarks, credential and signal stages illustrate distinct checks, not a real verification or payment result.'),
    }
    art, title, description = specs[name]
    hero = name == 'observatory'
    width = 600 if mobile else 1000
    height = (600 if mobile else 430) if hero else (420 if mobile else 330)
    art_height = 380 if hero and mobile else height
    position = 'xMaxYMid slice' if mobile else 'xMidYMid slice'
    body = f'<svg width="{width}" height="{art_height}" viewBox="0 0 2000 800" preserveAspectRatio="{position}"><g class="camera">{bitmap(art)}{signals(name)}</g></svg>'
    body += f'<rect width="{width}" height="{art_height}" fill="url(#shade)"/>'
    if hero and mobile:
        body += '<rect y="230" width="600" height="160" fill="url(#fade)"/>'
    else:
        body += f'<rect y="{height-110}" width="{width}" height="110" fill="url(#fade)"/>'
    x = 32 if mobile else 42
    if hero:
        kicker_y, name_y = (348, 422) if mobile else (56, 147)
        body += text(x, kicker_y, 'ENGINEERING / FROM MAURITANIA', 18 if mobile else 14, GOLD, 'letter-spacing="2"')
        body += text(x, name_y, 'Med', 79 if mobile else 85, SILVER, 'class="serif" letter-spacing="-3"')
        body += text(x, name_y+82, 'Gleiguem.', 79 if mobile else 85, '#edcf9e', 'class="serif" letter-spacing="-3"')
        body += text(x, name_y+128, 'AI / DATA / IDENTITY', 21 if mobile else 17, MUTED)
        body += text(x, name_y+159, 'LANGUAGE / COMPUTER VISION', 20 if mobile else 17, MUTED)
        if not mobile:
            body += text(x, height-25, 'THE OBSERVATORY / AFTER HOURS', 12, MUTED, 'letter-spacing="1"')
    else:
        chapter, lines, caption = ('02 / THE EXCHANGE', ['Data with', 'a destination.'], 'SOURCE CONTRACTS / TRANSFORMATIONS / ANALYTICS') if name == 'exchange' else ('03 / THE ATELIER', ['Identity.', 'Then the next step.'], 'CAPTURE / LIVENESS / MATCHING / HAND-OFF')
        body += text(x, 48 if mobile else 44, chapter, 20 if mobile else 14, GOLD, 'letter-spacing="2"')
        for i, line in enumerate(lines):
            body += text(x, 118+i*55 if mobile else 107+i*49, line, 48 if mobile else 43, SILVER, 'class="serif"')
        if mobile:
            caption = 'SOURCE → TRANSFORM → ANALYTICS' if name == 'exchange' else 'CAPTURE / CHECKS / HAND-OFF'
        body += text(x, height-26, caption, 17 if mobile else 12, MUTED)
    return document(width, height, title, description, body)


def research(mobile=False):
    width, height = (600, 560) if mobile else (1000, 280)
    body = ''
    for index, name in enumerate(['HASSANIYA / METRE RULES', 'SIGNS / DATASET PREPARATION']):
        x, y = (24, 20+index*270) if mobile else (24+index*488, 18)
        w, h = (552, 242) if mobile else (464, 244)
        body += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0c1d2c" stroke="#2b4055"/>'
        body += text(x+20, y+34, name, 21 if mobile else 16, GOLD)
        if index == 0:
            for row in range(2):
                yy = y+93+row*55
                body += f'<path d="M{x+24} {yy}H{x+w-24}" stroke="#30495f"/>'
                for n in range(5):
                    xx = x+38+n*((w-88)/4)
                    path = f'M{xx} {yy-13}V{yy+13}M{xx+15} {yy-13}V{yy+13}' if (n+row)%2 == 0 else f'M{xx-3} {yy}h32'
                    body += f'<path class="meter" d="{path}" stroke="{GOLD}" stroke-width="3" style="animation-delay:-{n+row}s"/>'
            body += text(x+20, y+h-23, 'ILLUSTRATIVE PATTERN / RULE CHECKING', 17 if mobile else 13)
        else:
            scale = .82
            tx, ty = x+w/2-125*scale, y+41
            palm = 'M125 180L85 153L65 122L48 91L35 71M125 180L95 118L93 80L91 48L91 23M125 180L125 108L125 64L125 31L125 6M125 180L154 118L160 77L163 48L165 26M125 180L178 136L192 109L202 88L210 69M95 118L125 108L154 118L178 136'
            body += f'<g transform="translate({tx} {ty}) scale({scale})" fill="none" stroke="{BLUE}" stroke-width="1.7"><path d="{palm}" opacity=".45"/><path class="trace" d="{palm}"/>'
            for xx, yy in [(125,180),(95,118),(125,108),(154,118),(178,136),(35,71),(91,23),(125,6),(165,26),(210,69)]:
                body += f'<circle cx="{xx}" cy="{yy}" r="3" fill="{GOLD}" stroke="none"/>'
            body += '</g>'+text(x+20, y+h-23, 'SYNTHETIC LANDMARKS / SUBJECT SPLITS', 17 if mobile else 13)
    return document(width, height, 'Language, gesture, structure', 'Animated illustrative scansion marks and synthetic hand landmarks. These show research methods, not validated metre examples or recognition results.', body)


def static_svg(source):
    """Freeze both CSS and native SVG motion, preserving the visible base scene."""
    root = ET.fromstring(source)
    ns = '{http://www.w3.org/2000/svg}'

    def freeze_css(css):
        css = re.sub(r'@keyframes\s+[\w-]+\s*\{(?:[^{}]|\{[^{}]*\})*\}', '', css)
        return re.sub(r'animation(?:-[a-z-]+)?\s*:[^;}]+;?', '', css)

    for parent in root.iter():
        for child in list(parent):
            if child.tag.rsplit('}', 1)[-1] in ('animate', 'animateMotion', 'animateTransform', 'set'):
                parent.remove(child)
        if parent.tag == ns+'style':
            parent.text = freeze_css(parent.text or '')
        if 'style' in parent.attrib:
            parent.set('style', freeze_css(parent.get('style')))
    ET.SubElement(root, ns+'style').text = '*{animation:none!important}.flow,.trace{stroke-dasharray:none!important;stroke-dashoffset:0!important}.meter{opacity:1!important}'
    ET.register_namespace('', ns[1:-1])
    return ET.tostring(root, encoding='unicode')


def write_variants(name, renderer):
    for mobile in (False, True):
        source = renderer(mobile)
        suffix = '-mobile' if mobile else ''
        for static in (False, True):
            content = static_svg(source) if static else source
            ET.fromstring(content)
            path = OUT / (name+suffix+('-static' if static else '')+'.svg')
            path.write_text(content+'\n')
            print(path.name, len(content.encode()), 'bytes')


def main():
    OUT.mkdir(exist_ok=True)
    for name in ('observatory', 'exchange', 'identity'):
        write_variants(name, lambda mobile, name=name: scene(name, mobile))
    write_variants('research-methods', research)


if __name__ == '__main__':
    main()
