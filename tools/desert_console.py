"""Original desert artwork and animated, self-contained GitHub profile panels."""
import base64
from datetime import date, timedelta
from html import escape
import json
import math
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


def document(width, height, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><clipPath id="clip"><rect width="{width}" height="{height}" rx="4"/></clipPath>
<linearGradient id="shade"><stop stop-color="{INK}" stop-opacity=".85"/><stop offset=".48" stop-color="{INK}" stop-opacity=".35"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}"/></linearGradient>
</defs><style>{STYLE}</style><g clip-path="url(#clip)"><rect width="{width}" height="{height}" fill="{INK}"/>{body}{frame(width,height)}</g></svg>'''


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


def contours(cx, cy, radius):
    parts = []
    for ring in range(7):
        r = radius*(.30+ring*.115)
        points = []
        for step in range(101):
            angle = step*math.tau/100
            rr = r*(1+.035*math.sin(7*angle+ring)+.022*math.cos(11*angle))
            points.append(f'{cx+math.cos(angle)*rr:.2f},{cy+math.sin(angle)*rr*.68:.2f}')
        path = 'M'+'L'.join(points)+'Z'
        parts.append(f'<path d="{path}" fill="none" stroke="{GOLD}" opacity="{.16+ring*.045:.3f}" stroke-width=".8"/>')
        if ring in (2, 5):
            parts.append(f'<path class="flow slow" pathLength="100" d="{path}" fill="none" stroke="{GOLD}" stroke-width="1.5" style="animation-delay:-{ring}s"/>')
    return ''.join(parts)


def hero(mobile=False):
    width, height = (400, 490) if mobile else (1000, 530)
    bitmap = base64.b64encode((ROOT/'assets/artwork/desert/night-ksar.jpg').read_bytes()).decode()
    y, h = (130, 360) if mobile else (0, height)
    body = f'<image href="data:image/jpeg;base64,{bitmap}" x="0" y="{y}" width="{width}" height="{h}" preserveAspectRatio="xMaxYMid slice"/>'
    body += f'<rect width="{width}" height="{height}" fill="url(#shade)"/>'
    if mobile:
        body += '<rect width="400" height="180" fill="#080d12" opacity=".65"/>'
        body += '<g transform="translate(302 274) scale(.50)">'+contours(0, 0, 115)+'</g>'
        body += route('M30 304Q180 345 335 214', CYAN, 3)
        body += route('M35 425Q150 350 370 383', GOLD, 0, 'slow')
        body += text(27, 83, 'MED', 70, WHITE, 'class="name" letter-spacing="-2"')
        body += text(25, 151, 'GLEIGUEM', 69, WHITE, 'class="name" textLength="348" lengthAdjust="spacingAndGlyphs"')
        body += text(28, 193, '@Medgleiguem', 25, WHITE, 'class="mono"')
        body += text(28, 230, 'AI / DATA / LANGUAGE', 23, CYAN, 'class="mono"')
        body += '<path class="sand" pathLength="100" d="M18 456Q167 411 380 450" fill="none" stroke="#e8c17f" stroke-width="1.6"/>'
    else:
        body += '<g>'+contours(797, 116, 110)+'</g>'
        for i, path in enumerate(['M440 71Q586 20 808 125T963 94', 'M362 284Q560 290 667 170T957 64', 'M130 475Q420 380 724 450T973 409']):
            body += route(path, GOLD if i==2 else CYAN, i*3, 'slow' if i==2 else '')
        body += text(42, 127, 'MED', 116, WHITE, 'class="name" letter-spacing="-3"')
        body += text(39, 237, 'GLEIGUEM', 113, WHITE, 'class="name" textLength="520" lengthAdjust="spacingAndGlyphs"')
        body += text(45, 285, '@Medgleiguem', 27, WHITE, 'class="mono"')
        body += text(45, 327, 'AI / DATA / LANGUAGE', 24, CYAN, 'class="mono" letter-spacing="1"')
        body += '<path class="sand" pathLength="100" d="M27 452Q290 354 660 441T979 431" fill="none" stroke="#f0cb88" stroke-width="2"/>'
    body += f'<rect y="{height-85}" width="{width}" height="85" fill="url(#fade)"/>'
    return document(width, height, 'Med Gleiguem — AI, data and language', 'Original illustrated night dunes and historic-ksar-inspired architecture, with animated sand light, organic contours and cyan signals. No portrait.', body)


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


def render_workbench(data, mobile=False, animated=True):
    days = calendar_days(data)
    first, last = days[0][0], days[-1][0]
    total, active = sum(count for _, count in days), sum(count>0 for _, count in days)
    width, height = (400, 710) if mobile else (1000, 440)
    body = text(29 if mobile else 40, 55, 'GITHUB ACTIVITY', 28 if mobile else 26, WHITE, 'class="mono" letter-spacing="2"')
    body += signals(mobile)
    if mobile:
        metric_y, label_y, left, right = 290, 324, 28, 232
        grid_x, grid_y, step, cell = 29, 363, 16.5, 12
    else:
        metric_y, label_y, left, right = 345, 375, 40, 273
        grid_x, grid_y, step, cell = 457, 108, 23.3, 17.4
    for x, value, key, label in [(left, total, 'contributions', 'contributions'), (right, active, 'active-days', 'active days')]:
        body += text(x, metric_y, f'{value:,}', 47 if mobile else 48, WHITE, f'data-metric="{key}"')
        body += text(x, label_y, label, 23 if mobile else 22, GOLD)
    offset = (first.weekday()+1)%7
    for index, (day, count) in enumerate(days):
        column, row = divmod(index+offset, 7)
        color = next(color for ceiling, color in LEVELS if count <= ceiling)
        label = f'{day.isoformat()}: {count} contributions'
        body += f'<rect x="{grid_x+column*step:.2f}" y="{grid_y+row*step:.2f}" width="{cell}" height="{cell}" rx="1.6" fill="{color}" data-date="{day.isoformat()}" data-count="{count}"><title>{escape(label)}</title></rect>'
    # The legend explicitly defines the color buckets; calendar cells never animate.
    legend_x, legend_y = (29, 550) if mobile else (457, 295)
    for i, (_, color) in enumerate(LEVELS):
        x = legend_x+i*(70 if mobile else 30)
        body += f'<rect x="{x}" y="{legend_y}" width="20" height="14" rx="2" fill="{color}"/>'
        if mobile:
            body += text(x+10, legend_y+42, ['0','1–4','5–19','20–49','50+'][i], 22, MUTED, 'text-anchor="middle"')
    if not mobile:
        body += text(legend_x+160, legend_y+13, '0 / 1–4 / 5–19 / 20–49 / 50+', 15)
    window = f'{first.isoformat()} → {last.isoformat()}'
    body += text(28 if mobile else 457, 512 if mobile else 350, window, 23 if mobile else 21, WHITE)
    body += text(28 if mobile else 457, 640 if mobile else 383, 'Snapshot '+data['updated_at'][:10]+' UTC', 23 if mobile else 19)
    if not total:
        body += text(28 if mobile else 40, 681 if mobile else 412, 'No contributions in this window', 22 if mobile else 18, MUTED)
    elif mobile:
        body += text(28, 681, 'GitHub-visible contributions', 23, MUTED)
    else:
        body += text(40, 412, 'GitHub-visible contributions', 17, MUTED)
    result = document(width, height, 'Med Gleiguem — actual GitHub activity', f'GitHub-visible contributions from {first.isoformat()} to {last.isoformat()}: {total} contributions across {active} active days. Snapshot {data["updated_at"]}. Calendar colors: 0, 1–4, 5–19, 20–49, 50 or more. Signals are decorative; counts are contributions, not hours or project quality.', body)
    return result if animated else static_svg(result)


def tools_panel(mobile=False):
    width, height = (400, 380) if mobile else (1000, 230)
    body = text(29 if mobile else 40, 53, 'IN THE TOOLBOX', 28 if mobile else 26, WHITE, 'class="mono" letter-spacing="2"')
    icons = json.loads((ROOT/'assets/artwork/desert/tool-icons.json').read_text())
    for i, (label, key) in enumerate([('Python', 'python'), ('TypeScript', 'typescript'), ('SQL', None), ('PostgreSQL', 'postgresql')]):
        x = (104 if i%2==0 else 295) if mobile else 143+i*238
        y = 118+(i//2)*155 if mobile else 125
        if key:
            mark = ''.join(f'<path d="{path}"/>' for path in icons[key])
            body += f'<g transform="translate({x-24} {y-32}) scale(2)" fill="{CYAN}">{mark}</g>'
        else:
            body += f'<g transform="translate({x-22} {y-31})" stroke="{CYAN}" fill="none" stroke-width="2.3"><ellipse cx="22" cy="7" rx="21" ry="7"/><path d="M1 7v35c0 10 42 10 42 0V7M1 19c0 10 42 10 42 0M1 31c0 10 42 10 42 0"/></g>'
        body += text(x, y+52, label, 24 if mobile else 23, WHITE, 'text-anchor="middle"')
        path = f'M{x-72} {y+69}h144'
        body += route(path, GOLD, i*3, 'slow')
        body += diamond(x, y-49, 3)
    return document(width, height, 'Tools — Python, TypeScript, SQL and PostgreSQL', 'Four tools used in the work, with recognizable technical icons and independently phased sand-gold signal traces. This is a tool selection, not a ranking of public language bytes.', body)


def footer(mobile=False):
    width, height = (400, 120) if mobile else (1000, 165)
    body = ''
    for i in range(5):
        y = 57+i*16
        body += f'<path d="M0 {y}Q{width*.17:.1f} {y-40} {width*.43:.1f} {y+3}T{width} {y-15}V{height}H0Z" fill="'+['#18232b','#172028','#23272a','#121d25','#0b151d'][i]+'"/>'
        body += f'<path class="sand" style="animation-delay:-{i*3}s" pathLength="100" d="M0 {y}Q{width*.17:.1f} {y-40} {width*.43:.1f} {y+3}T{width} {y-15}" stroke="{GOLD}" stroke-width="1" fill="none"/>'
    body += route(f'M20 45Q{width*.35:.1f} 4 {width-20} 46', CYAN, 5, 'slow')
    return document(width, height, 'Night dunes — contact links below', 'Original vector dunes with traveling sand-gold highlights and a cyan signal. GitHub, LinkedIn and email are individual native links below this illustration.', body)
