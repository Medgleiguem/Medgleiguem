"""Evidence-based domain content and original vector artwork for the profile."""
import json
from desert_console import ROOT, INK, WHITE, GOLD, CYAN, MUTED, text, document, route

DOMAINS = {
    'ai': {
        'name': 'AI systems & retrieval',
        'methods': ['RAG & hybrid search', 'LLM integration · ML'],
        'tools': [('Python','python'),('FastAPI','fastapi'),('pgvector',None),('Docling',None),('SQLAlchemy','sqlalchemy')],
        'work': ['Health Ministry · BCM / RKF', 'ARE · National KB'],
    },
    'data': {
        'name': 'Data engineering',
        'methods': ['ELT & orchestration', 'Models & analytics'],
        'tools': [('Airflow','apacheairflow'),('dbt','dbt'),('PostgreSQL','postgresql'),('MySQL','mysql'),('MongoDB','mongodb'),('SQL',None)],
        'work': ['ANRPTS / BI Houwiyeti'],
    },
    'software': {
        'name': 'Full-stack systems',
        'methods': ['APIs & application UI', 'Roles & async work'],
        'tools': [('TypeScript','typescript'),('React','react'),('Next.js','nextdotjs'),('Django','django'),('Spring Boot','springboot'),('Flask','flask')],
        'work': ['Health · National KB · ANRPTS'],
    },
    'vision': {
        'name': 'Identity & vision',
        'methods': ['Capture & liveness', 'Matching & landmarks'],
        'tools': [('Python','python'),('MediaPipe','mediapipe'),('SQLite','sqlite'),('OCR',None),('Object storage',None)],
        'work': ['KYC Identity', 'Mauritanian Sign Language'],
    },
    'payments': {
        'name': 'Payments & workflows',
        'methods': ['Eligibility & wallets', 'Locks & integrations'],
        'tools': [('TypeScript','typescript'),('Next.js','nextdotjs'),('MongoDB','mongodb'),('Redis','redis'),('BullMQ','bullmq')],
        'work': ['Taazour Aoun · Taazour Pay'],
    },
    'nlp': {
        'name': 'Arabic & Hassaniya NLP',
        'methods': ['Corpus normalization', 'Metre & rhyme'],
        'tools': [('Python','python'),('Pydantic','pydantic'),('YAML','yaml'),('spaCy','spacy'),('scikit-learn','scikitlearn')],
        'work': ['Hassaniya Laghn'],
    },
    'security': {
        'name': 'Cybersecurity',
        'methods': ['CTFs & web testing', 'Vulnerability checks'],
        'tools': [('Burp Suite','burpsuite'),('Linux / Arch','linux'),('Python','python')],
        'work': ['CTF practice · web security'],
    },
    'workflow': {
        'name': 'Engineering workflow',
        'methods': ['Review · test · ship', 'CI & developer tools'],
        'tools': [('Docker','docker'),('Git','git'),('Actions','githubactions'),('Linux','linux'),('Claude Code','claude'),('Cursor','cursor')],
        'work': ['GitHub automation · code review'],
    },
}


def facade(x, y, scale=1):
    """Original geometric stone-facade motif; atmosphere, not a site depiction."""
    shape = '<path d="M6 136V25h12V11h14v14h15V11h14v14h15V11h14v14h18v111M0 136h116M43 136V85q15-22 31 0v51M33 46h50M33 57h50"/>'
    for row in range(3):
        for column in range(3):
            xx, yy = 10+column*35, 66+row*22
            if column!=1:
                shape += f'<path d="M{xx} {yy}l7-6 7 6-7 6Z"/>'
    result = f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{GOLD}" stroke-width="1.3" stroke-linejoin="round">{shape}</g>'
    result += f'<g transform="translate({x} {y}) scale({scale})">'+route('M43 135V85Q58 63 74 85v50', CYAN, 3)+'</g>'
    return result


def hero(mobile=False):
    width, height = (400, 242) if mobile else (1000, 250)
    if mobile:
        body = text(24, 61, 'Med Gleiguem', 46, WHITE, 'font-weight="700" letter-spacing="-1.5"')
        body += text(26, 103, '@Medgleiguem', 25, MUTED, 'class="mono"')
        body += text(26, 147, 'SOFTWARE / DATA / AI', 22, WHITE, 'class="mono"')
        body += text(26, 180, 'SECURITY / RESEARCH', 22, WHITE, 'class="mono"')
        body += facade(300, 131, .60)
    else:
        body = text(40, 91, 'Med Gleiguem', 70, WHITE, 'font-weight="700" letter-spacing="-2"')
        body += text(43, 135, '@Medgleiguem', 27, MUTED, 'class="mono"')
        body += text(43, 183, 'SOFTWARE / DATA / AI / SECURITY / RESEARCH', 23, WHITE, 'class="mono"')
        body += facade(809, 31, 1.20)
    body += f'<path d="M24 16h36" stroke="{GOLD}" stroke-width="3"/>'
    base_y = height-18
    body += f'<path d="M0 {base_y}Q{width*.20} {base_y-18} {width*.47} {base_y+1}T{width} {base_y-4}" fill="none" stroke="#36434a"/>'
    body += route(f'M0 {base_y}Q{width*.20} {base_y-18} {width*.47} {base_y+1}T{width} {base_y-4}', GOLD, 0, 'slow')
    return document(width, height, 'Med Gleiguem — software, data, AI, security and research', 'Med Gleiguem. Software, data, AI, security and research, with an etched geometric facade and moving dune line.', body, framed=False)


def method_glyph(slug):
    """Each domain uses its own small animated engineering sketch."""
    ink = f'fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if slug=='ai':
        body = '<path d="M8 17h25v33H8ZM45 8h25v33H45ZM19 65h26v29H19ZM72 70l17 17M83 67a13 13 0 1 0-26 0 13 13 0 0 0 26 0Z"/><path d="M13 26h15M13 33h15M50 17h15M50 25h15"/>'
        flow = route('M30 49Q50 49 65 60', CYAN, 0)+route('M58 41L66 53', GOLD, 4)+route('M45 79Q56 80 63 74', CYAN, 6)
    elif slug=='data':
        body = '<path d="M7 15h22v22H7ZM7 46h22v22H7ZM7 77h22v22H7ZM54 40h34v35H54ZM63 75v20M50 95h43"/><path d="M29 26h12v30h13M29 57h25M29 88h12V57"/>'
        flow = route('M8 26H41V57H86', CYAN, 0)+route('M8 57H86', GOLD, 3)+route('M8 88H41V57H86', CYAN, 5)
    elif slug=='software':
        body = '<rect x="3" y="13" width="78" height="58" rx="3"/><path d="M3 26h78M13 19h2m6 0h2m6 0h2M27 37l-9 9 9 9m22-18 9 9-9 9M41 34l-7 24M17 84h69v16H17Z"/>'
        flow = route('M7 26H79V69H5V26', CYAN, 3)+route('M20 92H84', GOLD, 0)
    elif slug=='vision':
        body = '<path d="M4 38V13h24M66 13h25v25M91 73v25H67M28 98H4V73M29 34h35v43H29Z"/><path d="M35 65l8-21 8 13 8-18 16 28"/>'
        flow = route('M13 53H83', CYAN, 2)+route('M35 65L43 44 51 57 59 39 75 67', GOLD, 4)
    elif slug=='payments':
        body = '<path d="M5 26h76v56H5ZM5 39h76M63 49h27v24H63Z"/><circle cx="74" cy="61" r="2"/><path d="M24 25V14a15 15 0 0 1 30 0v11M34 88h26M40 97h15"/>'
        flow = route('M7 38H81V81H5V38', CYAN, 4)+route('M26 92H62', GOLD, 1)
    elif slug=='nlp':
        body = '<path d="M47 21Q25 9 5 18v64q20-9 42 3 22-12 42-3V18q-20-9-42 3v64M16 32h20M16 43h16M58 32h19M58 43h16M15 64h7v-9h8v9h7M58 63h8v-9h8v9h7"/>'
        flow = route('M14 64H22V55H30V64H38', GOLD, 0, 'fast')+route('M57 64H65V55H73V64H81', CYAN, 3, 'fast')
    elif slug=='security':
        body = '<path d="M47 6L84 21v31q-1 27-37 47Q11 79 10 52V21ZM31 40l-10 10 10 10m31-20 10 10-10 10M54 34L40 67"/>'
        flow = route('M47 7L84 21V52Q83 79 47 98Q11 79 10 52V21Z', GOLD, 2)+route('M15 72L79 29', CYAN, 4)
    else:
        body = '<path d="M15 18v65M15 45q50 0 50-27M15 65h65"/><circle cx="15" cy="13" r="6"/><circle cx="65" cy="13" r="6"/><circle cx="15" cy="89" r="6"/><rect x="56" y="52" width="30" height="27" rx="3"/><path d="M62 65l6 6 12-15"/>'
        flow = route('M15 22V81', CYAN, 1)+route('M63 23Q62 43 16 45V65H80', GOLD, 4)
    return f'<g {ink}>{body}</g>'+flow


def tool_mark(label, key, icons, x, y, size=22):
    if key in icons:
        paths = ''.join(f'<path d="{path}"/>' for path in icons[key])
        return f'<g transform="translate({x} {y}) scale({size/24})" fill="{MUTED}">{paths}</g>'
    generic = '<path d="M3 2h14l5 5v15H3Z M16 2v6h6M7 12h11M7 17h8"/>'
    if label in ('pgvector','SQL','Object storage'):
        generic = '<ellipse cx="12" cy="5" rx="10" ry="4"/><path d="M2 5v14c0 6 20 6 20 0V5M2 12c0 6 20 6 20 0"/>'
    if label=='MediaPipe':
        generic = '<path d="M3 18L7 5l7 5 6-7M7 5l3 15 4-10 7 10"/><circle cx="7" cy="5" r="2"/><circle cx="14" cy="10" r="2"/>'
    if label=='BullMQ':
        generic = '<path d="M1 3h7v7H1ZM16 3h7v7h-7ZM8 16h8v7H8ZM5 10v4h14v-4M12 14v3"/>'
    if label=='dbt':
        generic = '<path d="M3 4l9 8-9 8M12 12h10M12 3v18"/><circle cx="3" cy="4" r="2"/><circle cx="3" cy="20" r="2"/><circle cx="22" cy="12" r="2"/>'
    return f'<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-linejoin="round">{generic}</g>'


def domain_row(slug, mobile=False, compact=False):
    item = DOMAINS[slug]
    width, height = (400, 390) if mobile else ((700, 284) if compact else (1000, 220))
    left = 24 if mobile else (128 if compact else 145)
    body = text(left, 44, item['name'], 30 if mobile else 32, WHITE, 'font-weight="700" letter-spacing="-.4"')
    body += f'<path d="M24 {height-10}H{width-24}" stroke="#25343e"/>'
    body += '<path d="M24 12h20" stroke="'+GOLD+'" stroke-width="2"/>'
    body += text(362 if mobile else width-38, 367 if mobile else 44, '↗', 25, GOLD)
    body += f'<g transform="translate({24 if mobile else 28} {72 if mobile else 62}) scale({.65 if mobile else (.8 if compact else 1)})">'+method_glyph(slug)+'</g>'
    for index, phrase in enumerate(item['methods']):
        body += text(111 if mobile else left, (97 if mobile else 87)+index*34, phrase, 27 if mobile else 24, MUTED)
    icons = json.loads((ROOT/'assets/artwork/desert/tool-icons.json').read_text())
    for index, (label, key) in enumerate(item['tools']):
        x = (24 if index%2==0 else 211) if mobile else (568 if index%2==0 else 790)
        y = (190 if mobile else 72)+(index//2)*(45 if mobile else 43)
        if compact and not mobile:
            x, y = 128+(index%3)*184, 176+(index//3)*42
        body += tool_mark(label, key, icons, x, y-20, 23)
        body += text(x+31, y, label, 27 if mobile else (24 if compact else 23), WHITE)
    if mobile:
        for index, label in enumerate(item['work']):
            body += text(24, 336+index*29, label, 25, GOLD)
    else:
        body += text(left, 262 if compact else 195, ' · '.join(item['work']), 22, GOLD)
    description = item['name']+'. '+'. '.join(item['methods'])+'. Relevant toolkit: '+', '.join(label for label, _ in item['tools'])+'. Work/practice: '+'; '.join(item['work'])+'. Open the domain for native text and individual project links.'
    return document(width, height, item['name'], description, body, framed=False)
