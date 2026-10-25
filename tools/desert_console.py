"""Shared SVG primitives and truthful GitHub contribution-calendar rendering."""
from datetime import date, timedelta
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


def calendar_days(data):
    end = date.fromisoformat(data['window']['end'])
    start = max(date.fromisoformat(data['window']['start']), end-timedelta(days=139))
    counts = {date.fromisoformat(item['date']): item['count'] for item in data['calendar']}
    return [(start+timedelta(days=i), counts.get(start+timedelta(days=i), 0)) for i in range((end-start).days+1)]


def source_icon(kind, x, y):
    shapes = {
        'manuscript': '<rect x="3" y="1" width="22" height="28" rx="2"/><path d="M8 8h12M8 14h12M8 20h8"/>',
        'branch': '<path d="M7 8v17M7 20q15 0 15-12"/><circle cx="7" cy="5" r="3"/><circle cx="22" cy="5" r="3"/><circle cx="7" cy="27" r="3"/>',
        'code': '<path d="M8 6L0 15l8 9m14-18 8 9-8 9M18 2l-6 26"/>',
        'book': '<path d="M15 5Q7 0 1 4v23q7-4 14 0 7-4 14 0V4q-6-4-14 1v22"/>',
    }
    return f'<g transform="translate({x} {y})" stroke="{WHITE}" stroke-width="1.6" fill="none" stroke-linejoin="round">{shapes[kind]}</g>'


def signals(mobile=False):
    body = ''
    # This is decorative signal flow, separate from the data-bearing calendar.
    for i, kind in enumerate(('manuscript', 'branch', 'code', 'book')):
        y = 18+i*54
        body += source_icon(kind, 0, y-15)
        body += diamond(43, y, 3)
        body += route(f'M52 {y}C130 {y} 158 99 300 99', GOLD if i%3==0 else CYAN, i*2, 'fast' if i==2 else '')
        body += route(f'M52 {y+8}C125 {y+5} 198 155 306 127', CYAN, i*2+3, 'slow')
    body += '<circle class="breathe" cx="300" cy="99" r="4" fill="'+CYAN+'"/>'
    return f'<g transform="translate({38 if not mobile else 38} {96 if not mobile else 90})'+(' scale(.95 .60)' if mobile else '')+'">'+body+'</g>'


def render_workbench(data, mobile=False, animated=True, compact=False):
    days = calendar_days(data)
    first, last = days[0][0], days[-1][0]
    total, active = sum(count for _, count in days), sum(count>0 for _, count in days)
    width, height = (400, 710) if mobile else ((700, 480) if compact else (1000, 480))
    body = text(29 if mobile else 40, 55, 'GITHUB ACTIVITY', 28 if mobile else 26, WHITE, 'class="mono" letter-spacing="2"')
    body += ('<g transform="translate(5 25) scale(.66)">'+signals()+'</g>') if compact and not mobile else signals(mobile)
    if mobile:
        metric_y, label_y, left, right = 290, 324, 28, 232
        grid_x, grid_y, step, cell = 29, 363, 16.5, 12
    elif compact:
        metric_y, label_y, left, right = 345, 383, 30, 192
        grid_x, grid_y, step, cell = 295, 108, 17.4, 13
    else:
        metric_y, label_y, left, right = 345, 383, 40, 273
        grid_x, grid_y, step, cell = 457, 108, 23.3, 17.4
    for x, value, key, label in [(left, total, 'contributions', 'contributions'), (right, active, 'active-days', 'active days')]:
        value_y, caption_y = metric_y, label_y
        if compact and not mobile:
            x = 30
            value_y, caption_y = (277, 313) if key == 'contributions' else (383, 420)
        body += text(x, value_y, f'{value:,}', 47 if mobile else 48, WHITE, f'data-metric="{key}"')
        body += text(x, caption_y, label, 26, GOLD)
    offset = (first.weekday()+1)%7
    for index, (day, count) in enumerate(days):
        column, row = divmod(index+offset, 7)
        color = next(color for ceiling, color in LEVELS if count <= ceiling)
        label = f'{day.isoformat()}: {count} contributions'
        body += f'<rect x="{grid_x+column*step:.2f}" y="{grid_y+row*step:.2f}" width="{cell}" height="{cell}" rx="1.6" fill="{color}" data-date="{day.isoformat()}" data-count="{count}"><title>{escape(label)}</title></rect>'
    # The legend explicitly defines the color buckets; calendar cells never animate.
    legend_x, legend_y = (29, 550) if mobile else ((295, 256) if compact else (457, 295))
    for i, (_, color) in enumerate(LEVELS):
        x = legend_x+i*(70 if mobile or compact else 95)
        body += f'<rect x="{x}" y="{legend_y}" width="20" height="14" rx="2" fill="{color}"/>'
        if mobile or compact:
            body += text(x+10, legend_y+42, ['0','1–4','5–19','20–49','50+'][i], 26 if mobile else 24, MUTED, 'text-anchor="middle"')
        else:
            body += text(x+25, legend_y+15, ['0','1–4','5–19','20–49','50+'][i], 22)
    window = f'{first.isoformat()} → {last.isoformat()}'
    info_x = 28 if mobile else (295 if compact else 457)
    body += text(info_x, 512 if mobile else 365, window, 26, WHITE)
    body += text(info_x, 640 if mobile else 409, 'Snapshot '+data['updated_at'][:10]+' UTC', 26, MUTED)
    if not total:
        body += text(28 if mobile else 40, 681 if mobile else 451, 'No contributions in this window', 24, MUTED)
    elif mobile:
        body += text(28, 681, 'GitHub-visible contributions', 26, MUTED)
    else:
        body += text(30 if compact else 40, 451, 'GitHub-visible contributions', 24, MUTED)
    result = document(width, height, 'Med Gleiguem — actual GitHub activity', f'GitHub-visible contributions from {first.isoformat()} to {last.isoformat()}: {total} contributions across {active} active days. Snapshot {data["updated_at"]}. Calendar colors: 0, 1–4, 5–19, 20–49, 50 or more. Signals are decorative; counts are contributions, not hours or project quality.', body)
    return result if animated else static_svg(result)
