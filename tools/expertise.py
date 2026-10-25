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


def hero(mobile=False):
    width, height = (400, 500) if mobile else (1000, 470)
    body = '<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#102830"/><stop offset="1" stop-color="#101a20"/></linearGradient><linearGradient id="sun" x2="0" y2="1"><stop stop-color="#f0cf92"/><stop offset="1" stop-color="#ad7047"/></linearGradient><linearGradient id="dune" x2="0" y2="1"><stop stop-color="#805637"/><stop offset="1" stop-color="#312b27"/></linearGradient></defs>'
    # A deliberately composed illustration, rather than a raster scene or dashboard.
    scene = '<rect width="1000" height="470" fill="url(#sky)"/>'
    for i in range(38):
        x, y = (i*173+61)%1000, (i*i*19+29)%248
        scene += f'<circle cx="{x}" cy="{y}" r="{.7+(i%3)*.3}" fill="{GOLD if i%4==0 else MUTED}" opacity=".5"/>'
    scene += '<circle cx="801" cy="132" r="92" fill="url(#sun)"/>'
    scene += '<g fill="none" stroke="#caa571" stroke-width=".7" opacity=".45"><circle cx="801" cy="132" r="112"/><path d="M671 132h24m213 0h24M801 1v22m0 219v22"/></g>'
    scene += '<path d="M0 345Q125 220 275 291T554 278Q716 195 1000 287V470H0Z" fill="#1e383b"/>'
    scene += '<path d="M0 352Q209 257 398 338T762 290Q890 266 1000 319V470H0Z" fill="#285153"/>'
    # Stone-built silhouettes, with ornamental geometry derived from the small facade.
    for x, y, w, h in [(660,229,52,98),(717,191,72,134),(801,214,63,117),(879,249,55,84)]:
        scene += f'<path d="M{x} {y+h}V{y}h{w*.18}v-9h{w*.18}v9h{w*.24}v-9h{w*.18}v9h{w*.22}v{h}Z" fill="#172a2d" stroke="#b58d59" stroke-width="1"/>'
        for yy in range(y+19,y+h-10,19):
            scene += f'<path d="M{x+10} {yy}l5-4 5 4-5 4ZM{x+w-20} {yy}l5-4 5 4-5 4Z" fill="none" stroke="#9e8159" stroke-width=".8"/>'
        scene += f'<path d="M{x+w*.38} {y+h}v-25q{w*.12}-15 {w*.24} 0v25" fill="#c28b4a" opacity=".7"/>'
    scene += '<path d="M0 390Q160 300 340 371T702 351Q836 323 1000 368V470H0Z" fill="url(#dune)"/>'
    scene += '<path d="M0 433Q208 348 408 416T802 391Q904 385 1000 412V470H0Z" fill="#142026"/>'
    for i in range(4):
        yy=396+i*13
        scene += f'<path d="M590 {yy}Q790 {yy-65} 1000 {yy-4}" fill="none" stroke="#9e7950" opacity="{.24-i*.04}"/>'
    scene += route('M475 374Q697 394 813 355T1000 365', GOLD, 0, 'slow')
    scene += route('M555 420Q777 377 1000 412', CYAN, 5, 'slow')
    scene += route('M638 44L749 90', GOLD, 3, 'slow')
    if mobile:
        body += '<g transform="translate(-220 112) scale(.75)">'+scene+'</g>'
        body += '<rect width="400" height="220" fill="url(#fade)" transform="rotate(180 200 110)"/>'
        body += text(25, 41, '@Medgleiguem', 24, GOLD, 'class="mono"')
        body += text(22, 109, 'Med', 65, WHITE, 'font-weight="800" letter-spacing="-2"')
        body += text(22, 174, 'Gleiguem', 65, WHITE, 'font-weight="800" letter-spacing="-2"')
        body += text(25, 433, 'SOFTWARE · DATA · AI', 25, WHITE, 'class="mono"')
        body += text(25, 471, 'SECURITY · RESEARCH', 25, GOLD, 'class="mono"')
    else:
        body += scene+'<rect width="690" height="470" fill="url(#shade)"/>'
        body += text(42, 66, '@Medgleiguem', 25, GOLD, 'class="mono" letter-spacing="1"')
        body += text(35, 159, 'Med', 91, WHITE, 'font-weight="800" letter-spacing="-3"')
        body += text(35, 253, 'Gleiguem', 108, WHITE, 'font-weight="800" letter-spacing="-4"')
        body += text(43, 318, 'SOFTWARE / DATA / AI', 25, WHITE, 'class="mono"')
        body += text(43, 357, 'SECURITY / RESEARCH', 25, GOLD, 'class="mono"')
        body += '<path d="M43 399h120" stroke="#e2b76f"/><path d="M175 399h8m8 0h8m8 0h8" stroke="#55dce3"/>'
    body += '<path d="M1 28V1h28M'+str(width-29)+' 1h28v27M1 '+str(height-29)+'v28h28M'+str(width-29)+' '+str(height-1)+'h28v-28" fill="none" stroke="'+GOLD+'" stroke-width="2"/>'
    return document(width, height, 'Med Gleiguem — software, data, AI, security and research', 'Med Gleiguem. Software, data, AI, security and research. Original night-desert illustration with geometric stone architecture, layered dunes and moving signals.', body, framed=False)


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


def method_scene(slug):
    """A 300 x 220 illustrated method plate; all signals are decorative."""
    body = '<path d="M12 18h276v184H12Z" fill="#10232a"/>'
    body += '<path d="M12 52V18h34m208 0h34v34M12 168v34h34m208 0h34v-34" fill="none" stroke="#456164" stroke-width="1"/>'
    # Small stonework diamonds tie the engineering drawings to the desert artwork.
    for y in (75,99,123,147):
        body += f'<path d="M12 {y}l4-4 4 4-4 4ZM280 {y}l4-4 4 4-4 4Z" fill="none" stroke="#796448" stroke-width=".8"/>'
    line = f'fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if slug=='ai':
        for i,(x,y) in enumerate(((39,38),(39,121),(224,81))):
            body += f'<g transform="translate({x} {y})"><path d="M0 0h29l10 10v45H0Z" fill="#1b3940" stroke="#7ba2a7"/><path d="M29 0v10h10M8 20h22M8 28h22M8 36h14" {line}/></g>'
        body += '<path d="M115 73l37-21 37 21v65l-37 21-37-21Z" fill="#1f4145" stroke="#cda86e" stroke-width="2"/>'
        for y in (82,101,120):
            body += f'<path d="M125 {y}l27 16 27-16" fill="none" stroke="#729b9d"/>'
        body += route('M78 65H95V83H116',CYAN,0,'fast')+route('M78 149H95V123H116',GOLD,3,'fast')+route('M190 105H223',CYAN,5,'fast')
        body += '<g class="orbit"><circle cx="152" cy="105" r="68" fill="none" stroke="#b19b70" stroke-dasharray="1 12" stroke-width="2"/></g>'
        body += '<circle class="breathe" cx="244" cy="108" r="6" fill="'+CYAN+'"/>'
        body += '<rect x="79" y="61" width="6" height="8" fill="'+CYAN+'"><animate attributeName="x" values="79;108;79" dur="5s" repeatCount="indefinite"/></rect>'
    elif slug=='data':
        for x,y in ((35,44),(35,115),(210,79)):
            body += f'<g transform="translate({x} {y})"><path d="M0 9v39c0 13 50 13 50 0V9" fill="#1b3940" stroke="#729b9d"/><ellipse cx="25" cy="9" rx="25" ry="9" fill="#23474b" stroke="#95afb0"/><path d="M0 28c0 13 50 13 50 0M0 45c0 13 50 13 50 0" fill="none" stroke="#729b9d"/></g>'
        body += '<path d="M123 52l39 22-39 22-39-22Z" fill="#826442" stroke="#e2b76f"/><path d="M84 74v48l39 23 39-23V74l-39 22Z" fill="#244147" stroke="#c9a676"/><path d="M123 96v49" stroke="#c9a676"/>'
        body += route('M85 66H97V45H123V53',CYAN,0,'fast')+route('M85 146H112V135',GOLD,3,'fast')+route('M162 111H209',CYAN,5,'fast')
        for i in range(5):
            body += f'<rect x="{168+i*15}" y="{183-i*8}" width="7" height="{8+i*8}" fill="{GOLD if i%2 else CYAN}" opacity=".65"/>'
        body += '<path d="M168 105l6-3 6 3-6 3Z" fill="'+GOLD+'"><animateTransform attributeName="transform" type="translate" values="0 0;30 0;0 0" dur="4s" repeatCount="indefinite"/></path>'
    elif slug=='software':
        body += '<rect x="33" y="35" width="186" height="132" rx="4" fill="#152e34" stroke="#7da4a7" stroke-width="1.5"/><path d="M33 58h186" stroke="#618084"/>'
        for x in (45,55,65):
            body += f'<circle cx="{x}" cy="46" r="2" fill="{GOLD}"/>'
        for i,w in enumerate((54,83,68,97,61)):
            y=77+i*15
            body += f'<path d="M49 {y}h12M72 {y}h{w}" fill="none" stroke="{CYAN if i%2 else GOLD}" stroke-width="3" opacity=".7"/>'
        body += '<path d="M26 177h202l-13 14H41Z" fill="#22454a" stroke="#729b9d"/>'
        body += '<rect x="182" y="91" width="77" height="99" rx="4" fill="#101d23" stroke="#cfa86c" stroke-width="1.5"/><path d="M190 104h61v36h-61Z" fill="#28535a"/><path d="M190 153h37m-37 10h52m-52 10h42" stroke="#a8bbc1"/>'
        body += route('M188 134H253V106H188Z',CYAN,2,'fast')+route('M50 146H141',GOLD,0,'fast')
        body += '<rect x="148" y="139" width="9" height="12" fill="'+CYAN+'"><animate attributeName="opacity" values="1;1;0;0;1" dur="2s" repeatCount="indefinite"/></rect>'
    elif slug=='vision':
        # Abstract hand landmarks avoid introducing the portrait the user removed.
        body += '<path d="M94 183l-31-39q-9-13 1-19 8-4 18 11l12 11-12-72q-3-17 8-18 10-2 13 15l8 44-3-72q-1-17 10-17 11 0 12 16l4 72 6-59q2-16 12-15 10 1 8 17l-5 66 12-40q5-17 16-12 9 3 4 19l-15 60q-4 25-25 47Z" fill="#1e4247" stroke="#9bb5b5" stroke-width="1.5"/>'
        points=[(116,173),(79,137),(95,134),(92,78),(115,122),(119,48),(139,127),(151,65),(158,138),(176,96)]
        body += '<path d="M79 137L116 173 95 134 92 78M116 173L115 122 119 48M116 173L139 127 151 65M116 173L158 138 176 96" fill="none" stroke="'+CYAN+'" stroke-width="1.4"/>'
        for i,(x,y) in enumerate(points):
            body += f'<circle cx="{x}" cy="{y}" r="3" fill="{GOLD if i%2 else CYAN}"/>'
        body += '<path d="M42 68V35h33m113 0h33v33M42 154v33h33m113 0h33v-33" fill="none" stroke="#d9af6e" stroke-width="2"/>'
        body += route('M45 115H218',CYAN,3,'fast')
        body += '<rect x="43" y="36" width="177" height="2" fill="'+CYAN+'" opacity=".65"><animate attributeName="y" values="36;184;36" dur="7s" repeatCount="indefinite"/></rect>'
        body += '<g transform="translate(232 68)" stroke="#6d9396" stroke-width="1.5"><path d="M0 0h25m-25 16h17m-17 16h22m-22 16h13m-13 16h22m-22 16h17"/></g>'
    elif slug=='payments':
        body += '<path d="M97 57l54-30 54 30v79l-54 31-54-31Z" fill="#17383f" stroke="#668e92"/>'
        body += '<rect x="118" y="83" width="66" height="48" rx="4" fill="#9c7848" stroke="#e2b76f"/><path d="M132 83V67a19 19 0 0 1 38 0v16" fill="none" stroke="#e2b76f" stroke-width="4"/><circle cx="151" cy="104" r="5" fill="#132c33"/><path d="M151 107v10" stroke="#132c33" stroke-width="3"/>'
        for x,y in ((34,60),(34,140),(228,60),(228,140)):
            body += f'<rect x="{x}" y="{y}" width="38" height="28" rx="3" fill="#1d3b42" stroke="#809d9f"/><path d="M{x+7} {y+9}h24m-24 7h14" stroke="#94b4b6"/>'
        for i,path in enumerate(('M72 74H85V99H98','M72 154H85V119H98','M205 99H219V74H228','M205 119H219V154H228')):
            body += route(path,CYAN if i%2 else GOLD,i*2,'fast')
        body += '<path d="M105 186h18m8 0h18m8 0h18m8 0h18" stroke="#6f9697" stroke-width="3"/>'
        body += '<circle cx="211" cy="99" r="4" fill="'+CYAN+'"><animate attributeName="cx" values="211;221;211" dur="3s" repeatCount="indefinite"/></circle>'
    elif slug=='nlp':
        body += '<path d="M150 52Q96 29 47 48v122q50-15 103 7 53-22 103-7V48q-49-19-103 4Z" fill="#274347" stroke="#a98d62" stroke-width="1.5"/>'
        body += '<path d="M150 52v125M57 180q44-12 93 7 49-19 93-7" fill="none" stroke="#bca073"/>'
        # Real language names rather than decorative pseudo-Arabic glyphs.
        body += text(103,89,'عربية',25,GOLD,'text-anchor="middle" lang="ar"')
        body += text(201,89,'حسانية',23,GOLD,'text-anchor="middle" lang="ar"')
        for x in (65,168):
            for i,w in enumerate((65,51,59)):
                body += f'<path d="M{x} {106+i*12}h{w}" stroke="#8aabad" stroke-width="1.5"/>'
        body += route('M65 157H75V145H87V157H99V145H111V157H128',GOLD,0,'fast')
        body += route('M168 157H178V145H190V157H202V145H214V157H231',CYAN,3,'fast')
        body += '<path d="M43 32h33m149 0h33M43 193h33m149 0h33" stroke="#657f78"/>'
        body += '<rect x="64" y="142" width="18" height="20" fill="'+GOLD+'" opacity=".18"><animate attributeName="x" values="64;111;64" dur="5s" repeatCount="indefinite"/></rect>'
    elif slug=='security':
        body += '<circle cx="150" cy="110" r="78" fill="#18373c" stroke="#365b5d"/>'
        body += '<g fill="none" stroke="#547a7b" stroke-width=".8"><circle cx="150" cy="110" r="57"/><circle cx="150" cy="110" r="35"/><path d="M62 110h176M150 22v176M88 48l124 124M88 172L212 48"/></g>'
        body += '<g class="orbit" style="animation-duration:24s"><circle cx="150" cy="110" r="78" fill="none"/><path d="M150 110V32a78 78 0 0 1 67 39Z" fill="#55dce3" opacity=".12"/><path d="M150 110V32" stroke="#55dce3" stroke-width="1.5"/></g>'
        body += '<path d="M150 63l34 14v32q0 24-34 46-34-22-34-46V77Z" fill="#173139" stroke="#dfb36c" stroke-width="2"/><path d="M140 90l-10 12 10 12m20-24 10 12-10 12m-6-29-8 36" fill="none" stroke="#e2b76f" stroke-width="2"/>'
        for x,y in ((90,65),(213,134),(112,173)):
            body += f'<circle class="breathe" cx="{x}" cy="{y}" r="4" fill="{CYAN}"/>'
        body += route('M44 43V177H75',GOLD,1,'fast')
    else:
        for x,y in ((58,52),(58,112),(58,172),(150,52)):
            body += f'<circle cx="{x}" cy="{y}" r="9" fill="#1e4147" stroke="#b4c4bd" stroke-width="2"/>'
        body += '<path d="M58 61v42m0 18v42m92-102q0 51-83 51" fill="none" stroke="#698e8f" stroke-width="3"/>'
        body += route('M58 63V163',CYAN,0,'fast')+route('M150 62Q150 112 68 112',GOLD,3,'fast')
        for i in range(3):
            x=123+i*44
            body += f'<rect x="{x}" y="141" width="33" height="28" rx="2" fill="#22454b" stroke="#88aaa9"/>'
            body += f'<path d="M{x+7} 154h19" stroke="{GOLD if i==1 else CYAN}" stroke-width="3"/>'
        body += '<path d="M67 172h41v-18h14m35 0h9m35 0h9" fill="none" stroke="#698e8f"/>'
        body += '<path d="M187 41h62v65h-62Z" fill="#18353b" stroke="#caa26c"/><path d="M199 63h36m-36 11h22m-22 11h29" stroke="#7b9ea1"/>'
        body += route('M68 52H97V73H187',CYAN,4,'fast')
        body += '<circle cx="58" cy="70" r="4" fill="'+CYAN+'"><animate attributeName="cy" values="70;95;70" dur="4s" repeatCount="indefinite"/></circle>'
    return body


def domain_row(slug, mobile=False, compact=False):
    item = DOMAINS[slug]
    width, height = (400, 635) if mobile else ((700, 422) if compact else (1000, 350))
    index=list(DOMAINS).index(slug)
    reverse=index%2==1 and not (mobile or compact)
    left = 24 if mobile else (30 if compact else (40 if reverse else 365))
    body = f'<path d="M0 0H{width}V{height}H0Z" fill="{("#0d1a20" if index%2==0 else "#101e23")}"/>'
    body += f'<path d="M24 1H{width-24}M24 {height-1}H{width-24}" stroke="#2c4449"/>'
    body += text(left, 37, f'{index+1:02d}',22,GOLD,'class="mono"')
    categories=['INTELLIGENCE','DATA SYSTEMS','APPLICATIONS','PERCEPTION','TRANSACTIONS','LANGUAGE','SECURITY','DEVELOPER TOOLS']
    body += text(left+44, 37,categories[index],18,MUTED,'class="mono" letter-spacing="1.5"')
    body += text(width-46, 37, '↗', 25, GOLD)
    body += text(left, 86, item['name'], 30 if mobile else 34, WHITE, 'font-weight="700" letter-spacing="-.7"')
    art_x,art_y,scale=(50,161,1) if mobile else ((467,103,.68) if compact else ((675 if reverse else 25),64,1))
    body += f'<g transform="translate({art_x} {art_y}) scale({scale})">'+method_scene(slug)+'</g>'
    for index, phrase in enumerate(item['methods']):
        body += text(left, 126+index*33, phrase, 26 if mobile else 25, MUTED)
    icons = json.loads((ROOT/'assets/artwork/desert/tool-icons.json').read_text())
    for index, (label, key) in enumerate(item['tools']):
        x = (24 if index%2==0 else 211) if mobile else left+(index%3)*(213 if compact else 200)
        y = (430 if mobile else (282 if compact else 217))+(index//(2 if mobile else 3))*(43 if mobile else 46)
        body += tool_mark(label, key, icons, x, y-20, 22)
        body += text(x+29, y, label, 26 if mobile else 23, WHITE)
    if mobile:
        for index, label in enumerate(item['work']):
            body += text(24, 582+index*29, label, 24, GOLD)
    else:
        body += f'<path d="M{left} {365 if compact else 294}h{width-left-30 if not reverse else 570}" stroke="#355052"/>'
        body += text(left, 399 if compact else 329, ' · '.join(item['work']), 22, GOLD)
    description = item['name']+'. '+'. '.join(item['methods'])+'. Relevant toolkit: '+', '.join(label for label, _ in item['tools'])+'. Work/practice: '+'; '.join(item['work'])+'. Open the domain for native text and individual project links.'
    return document(width, height, item['name'], description, body, framed=False)
