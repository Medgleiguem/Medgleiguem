"""Shared SVG primitives, palette and tested static serializer."""
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INK, WHITE, GOLD, CYAN, MUTED = '#080d12', '#f2eee5', '#e2b76f', '#55dce3', '#a9bbc4'
LEVELS = [(0, '#14232c'), (4, '#214752'), (19, '#2b7480'), (49, '#42aab2'), (float('inf'), '#77e5e8')]

STYLE = '''
text{font-family:'Liberation Sans',Arial,sans-serif}
.mono{font-family:Consolas,'Liberation Mono',monospace}
.name{font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:900}
.flow{stroke-dasharray:2 98;animation:travel 10s linear infinite}
.sand{stroke-dasharray:14 86;animation:travel 18s linear infinite}
.slow{animation-duration:17s}.fast{animation-duration:7s}
.breathe{animation:breathe 8s ease-in-out infinite}
.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 90s linear infinite}
@keyframes travel{to{stroke-dashoffset:-100}}
@keyframes breathe{0%,100%{opacity:.3}50%{opacity:.85}}
@keyframes orbit{to{transform:rotate(360deg)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.flow,.sand{stroke-dasharray:none;opacity:.45}}
'''


def text(x, y, value, size=22, color=MUTED, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'


def diamond(x, y, size=5, color=GOLD):
    return f'<path d="M{x} {y-size}l{size} {size}-{size} {size}-{size}-{size}Z" fill="{INK}" stroke="{color}" stroke-width="1.2"/>'


def frame(width, height):
    result = f'<path d="M24 10H{width-24}l14 14V{height-24}l-14 14H24L10 {height-24}V24Z" fill="none" stroke="{GOLD}" stroke-opacity=".55"/>'
    for x, y in [(24, 10), (width-24, height-10)]:
        result += diamond(x, y, 6)
    return result


def document(width, height, title, description, body, framed=True):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><clipPath id="clip"><rect width="{width}" height="{height}" rx="4"/></clipPath>
<linearGradient id="shade"><stop stop-color="{INK}" stop-opacity=".85"/><stop offset=".48" stop-color="{INK}" stop-opacity=".35"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}"/></linearGradient>
</defs><style>{STYLE}</style><g clip-path="url(#clip)"><rect width="{width}" height="{height}" fill="{INK}"/>{body}{frame(width,height) if framed else ''}</g></svg>'''


def static_svg(source):
    """Freeze CSS and SMIL while retaining visible base states and valid markup."""
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
    ET.SubElement(root, ns+'style').text = '*{animation:none!important}.flow,.sand,.trace{stroke-dasharray:none!important;stroke-dashoffset:0!important;opacity:.45}.meter{opacity:1!important}'
    ET.register_namespace('', ns[1:-1])
    return ET.tostring(root, encoding='unicode')


def route(path, color=CYAN, delay=0, speed=''):
    return f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1" opacity=".18"/><path class="flow {speed}" pathLength="100" d="{path}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" style="animation-delay:-{delay}s"/>'
