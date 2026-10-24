#!/usr/bin/env python3
"""Build self-contained profile SVGs using only the Python standard library."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"


def text(x, y, value, size=18, color="#b1bccb", weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" {extra}>{escape(value)}</text>')


def document(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Custom artwork for Mohamed Gleiguem. Decorative motion stops when reduced motion is requested. All text remains visible without animation.</desc>
<defs>
  <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#101c2c"/><stop offset="1" stop-color="#080e17"/></linearGradient>
  <linearGradient id="edge"><stop stop-color="#70f0cb" stop-opacity=".55"/><stop offset=".6" stop-color="#9daaff" stop-opacity=".22"/><stop offset="1" stop-color="#70f0cb" stop-opacity=".1"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#70f0cb" stop-opacity=".1"/><stop offset="1" stop-color="#70f0cb" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#a5b9d3" opacity=".13"/></pattern>
  <clipPath id="frame"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20"/></clipPath>
</defs>
<style>
text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }}
.mono {{ font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }}
.flow {{ stroke-dasharray: 3 18; animation: flow 16s linear infinite; }}
.halo {{ transform-box: fill-box; transform-origin: center; animation: breathe 8s ease-in-out infinite; }}
@keyframes flow {{ to {{ stroke-dashoffset: -252; }} }}
@keyframes breathe {{ 50% {{ opacity: .45; transform: scale(.94); }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<g clip-path="url(#frame)">
<rect width="{width}" height="{height}" fill="url(#bg)"/>
<rect width="{width}" height="{height}" fill="url(#grid)"/>
{body}
</g>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="none" stroke="url(#edge)"/>
</svg>
'''


def architecture(x, y):
    s = f'<g transform="translate({x} {y})">'
    s += '<circle class="halo" cx="150" cy="160" r="188" fill="url(#glow)"/>'
    s += '<circle cx="150" cy="160" r="98" fill="none" stroke="#253748" stroke-dasharray="2 8"/>'
    s += '<circle cx="150" cy="160" r="130" fill="none" stroke="#203040"/>'
    for d in ['M28 50H85Q100 50 100 65V115Q100 130 120 130',
              'M272 50H215Q200 50 200 65V115Q200 130 180 130',
              'M150 186V250Q150 266 134 266H28',
              'M150 186V250Q150 266 166 266H272']:
        s += f'<path d="{d}" fill="none" stroke="#2e4f55" stroke-width="1.5"/>'
        s += f'<path class="flow" d="{d}" fill="none" stroke="#70f0cb" stroke-width="2"/>'
    for px, py, label in [(0, 26, 'SOURCES'), (218, 26, 'CONTEXT'),
                          (0, 244, 'PRODUCT'), (218, 244, 'ANSWERS')]:
        s += f'<rect x="{px}" y="{py}" width="84" height="46" rx="9" fill="#101d2b" stroke="#35475a"/>'
        s += text(px+42, py+28, label, 10, '#c5d1df', 600, 'text-anchor="middle" class="mono"')
    s += '<rect x="112" y="122" width="76" height="76" rx="22" fill="#142b30" stroke="#70f0cb" stroke-opacity=".7"/>'
    s += '<path d="m135 149 15-9 15 9-15 9z m-15 0v14l15 9 15-9v-14 m-15 9v14" fill="none" stroke="#70f0cb" stroke-width="2" stroke-linejoin="round"/>'
    s += text(150, 325, 'FROM CONTEXT TO SOMETHING USEFUL', 9, '#8eacc0', 500, 'text-anchor="middle" class="mono" letter-spacing="1"')
    return s + '</g>'


def banner(mobile=False):
    w, h = (600, 570) if mobile else (1200, 460)
    x = 40 if mobile else 56
    s = f'<ellipse cx="{w-40}" cy="20" rx="380" ry="300" fill="url(#glow)"/>'
    s += text(x, 57, 'MOHAMED GLEIGUEM', 17 if mobile else 15, '#70f0cb', 700, 'class="mono" letter-spacing="2.5"')
    s += text(x, 91, 'AI & SOFTWARE ENGINEERING', 12 if mobile else 11, '#9baabd', 500, 'class="mono" letter-spacing="2"')
    if mobile:
        s += text(x, 178, 'Intelligence.', 62, '#f0f3f5', 700, 'letter-spacing="-2"')
        s += text(x, 250, 'Engineered.', 62, '#70f0cb', 700, 'letter-spacing="-2"')
        s += text(x, 309, 'From source-cited AI to software', 22)
        s += text(x, 341, 'that people use.', 22)
        s += '<path class="flow" d="M40 396H560" stroke="#70f0cb" stroke-opacity=".6"/>'
        s += text(x, 444, 'AI / DATA / SECURITY', 17, '#d6dfe8', 600, 'class="mono"')
        s += text(x, 476, 'WEB / MOBILE / RESEARCH', 17, '#d6dfe8', 600, 'class="mono"')
        s += text(x, 535, 'NOUAKCHOTT, MAURITANIA · UTC+0', 13, '#a5b4c7', 500, 'class="mono"')
    else:
        s += text(x, 184, 'Intelligence.', 72, '#f0f3f5', 700, 'letter-spacing="-2.5"')
        s += text(x, 268, 'Engineered.', 72, '#70f0cb', 700, 'letter-spacing="-2.5"')
        s += text(x, 318, 'From source-cited AI to software that people use.', 20)
        s += text(x, 363, 'AI / DATA / SECURITY / WEB / MOBILE / RESEARCH', 12, '#d6dfe8', 600, 'class="mono" letter-spacing=".5"')
        s += architecture(824, 48)
        s += '<path d="M56 400H1144" stroke="#b5d2d8" stroke-opacity=".15"/>'
        s += text(x, 432, 'NOUAKCHOTT, MAURITANIA · UTC+0', 11, '#a5b4c7', 500, 'class="mono"')
        s += text(1144, 432, 'CONTEXT → SYSTEMS → IMPACT', 11, '#a5b4c7', 500, 'text-anchor="end" class="mono"')
    return document(w, h, 'Mohamed Gleiguem — Intelligence. Engineered.', s)


def footer(mobile=False):
    w, h = (600, 170) if mobile else (1200, 166)
    x = 40 if mobile else 56
    s = text(x, 47, 'LET’S BUILD', 12, '#70f0cb', 700, 'class="mono" letter-spacing="2"')
    s += text(x, 98, 'Something that matters.', 34 if mobile else 38, '#f0f3f5', 600, 'letter-spacing="-1"')
    s += text(x, 134, 'AI · Data · Security · Accessible software', 16, '#b1bccb')
    if not mobile:
        s += '<path class="flow" d="M780 83H1144" fill="none" stroke="#70f0cb" stroke-width="1.5"/>'
        s += '<circle cx="1144" cy="83" r="4" fill="#70f0cb"/>'
    return document(w, h, 'Let’s build something that matters.', s)


def main():
    OUT.mkdir(exist_ok=True)
    for name, svg in [('banner.svg', banner()), ('banner-mobile.svg', banner(True)),
                      ('footer.svg', footer()), ('footer-mobile.svg', footer(True))]:
        (OUT / name).write_text(svg, encoding='utf-8')
        print(f'{name}: {len(svg.encode())} bytes')


if __name__ == '__main__':
    main()
