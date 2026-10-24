#!/usr/bin/env python3
"""Generate the profile's custom animated SVGs; Python standard library only."""
from html import escape
from pathlib import Path
import json
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
COLORS = ['#a78bfa', '#22d3ee', '#34d399', '#fb7185', '#fbbf24', '#60a5fa']


def text(x, y, value, size=20, color='#aebbd3', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def lines(x, y, value, width=42, size=20, color='#aebbd3', pitch=None):
    return ''.join(text(x, y+i*(pitch or size*1.45), line, size, color) for i, line in enumerate(textwrap.wrap(value, width)))


def document(w, h, title, body, description=None):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description or title)}. Decorative animation respects reduced motion.</desc>
<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#111a2e"/><stop offset="1" stop-color="#090e1b"/></linearGradient>
 <linearGradient id="border"><stop stop-color="#a78bfa" stop-opacity=".7"/><stop offset=".5" stop-color="#22d3ee" stop-opacity=".3"/><stop offset="1" stop-color="#34d399" stop-opacity=".5"/></linearGradient>
 <radialGradient id="violet"><stop stop-color="#8b5cf6" stop-opacity=".23"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>
 <radialGradient id="cyan"><stop stop-color="#22d3ee" stop-opacity=".16"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
 <linearGradient id="shine"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
 <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#a0b5dd" stroke-opacity=".045"/></pattern>
 <clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath>
</defs>
<style>
 text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif}}
 .mono{{font-family:Consolas,'Liberation Mono',monospace}}
 .flow{{stroke-dasharray:4 16;animation:flow 12s linear infinite}}
 .orbit{{transform-box:fill-box;transform-origin:center;animation:orbit 36s linear infinite}}
 .float{{animation:float 9s ease-in-out infinite alternate}}
 .pulse{{animation:pulse 5s ease-in-out infinite}}
 .cursor{{animation:cursor 1.4s steps(2,end) infinite}}
 .aurora{{animation:aurora 18s ease-in-out infinite alternate}}
 .trace{{stroke-dasharray:80 600;animation:trace 12s linear infinite}}
 .icon-line{{stroke-dasharray:100;animation:draw 9s ease-in-out infinite}}
 .icon-bob{{animation:float 5s ease-in-out infinite alternate}}
 .beam{{animation:beam 14s linear infinite}}
 .role{{opacity:0;animation:role 20s linear infinite}}
 .role.first{{opacity:1}}
 .r1{{animation-delay:5s}}.r2{{animation-delay:10s}}.r3{{animation-delay:15s}}
 @keyframes flow{{to{{stroke-dashoffset:-240}}}}
 @keyframes trace{{to{{stroke-dashoffset:-1360}}}}
 @keyframes orbit{{to{{transform:rotate(360deg)}}}}
 @keyframes float{{to{{transform:translateY(-7px)}}}}
 @keyframes pulse{{50%{{opacity:.4}}}}
 @keyframes cursor{{50%{{opacity:0}}}}
 @keyframes aurora{{to{{transform:translate(28px,-16px) scale(1.05)}}}}
 @keyframes role{{0%,22%{{opacity:1}}25%,100%{{opacity:0}}}}
 @keyframes draw{{0%,35%,100%{{stroke-dashoffset:0}}65%{{stroke-dashoffset:90}}}}
 @keyframes beam{{from{{transform:translateX(-400px)}}to{{transform:translateX(1200px)}}}}
 @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.role{{opacity:0!important}}.role.first{{opacity:1!important}}}}
</style>
<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#bg)"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>{body}</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="none" stroke="url(#border)" stroke-opacity=".7"/>
</svg>'''


ICONS = {
 'ai':'M9 3a3 3 0 0 0-3 3 4 4 0 0 0-2 7 4 4 0 0 0 5 6V3z M15 3a3 3 0 0 1 3 3 4 4 0 0 1 2 7 4 4 0 0 1-5 6V3z M12 2v20',
 'data':'M4 5c0-4 16-4 16 0s-16 4-16 0v14c0 4 16 4 16 0V5 M4 12c0 4 16 4 16 0',
 'shield':'M12 2 3 6v6c0 5 9 10 9 10s9-5 9-10V6z M8 12l3 3 5-6',
 'code':'m8 5-7 7 7 7 m8-14 7 7-7 7 M14 3l-4 18',
 'mobile':'M7 2h10a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z M9 5h6 M10 19h4',
 'research':'M8 2h8 M10 2v7l-6 10q-1 3 2 3h12q3 0 2-3L14 9V2 M7 16h10',
 'trophy':'M7 3h10v6a5 5 0 0 1-10 0z M7 5H3v3c0 3 4 4 5 3 M17 5h4v3c0 3-4 4-5 3 M12 14v5 M7 22h10 M9 19h6v3',
 'poetry':'M4 3h16v18H4z M8 7h8 M8 11h8 M8 15h5',
 'music':'M9 18V5l11-2v13 M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0 M20 16a3 3 0 1 1-6 0 3 3 0 0 1 6 0',
 'work':'M3 7h18v14H3z M8 7V3h8v4 M3 13h18 M10 12v3h4v-3',
}


def icon(name, x, y, size=32, color='#22d3ee'):
    return f'<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path class="icon-line" d="{ICONS.get(name,ICONS["code"])}"/></g>'


def panel(x,y,w,h,color,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#111a2e" stroke="{color}" stroke-opacity=".28" {extra}/>'


def hero(mobile=False):
    w,h=(600,710) if mobile else (1000,500)
    s=f'<ellipse class="aurora" cx="180" cy="60" rx="470" ry="400" fill="url(#violet)"/><ellipse class="aurora" cx="{w}" cy="{h}" rx="500" ry="450" fill="url(#cyan)"/>'
    s+=f'<polygon class="beam" points="0,0 120,0 350,{h} 230,{h}" fill="url(#shine)"/>'
    s+=text(36,42,'MG / ENGINEERING',14 if not mobile else 18,'#c4b5fd',700,'class="mono" letter-spacing="2"')
    if not mobile:s+=text(964,42,'NOUAKCHOTT · UTC+0',12,'#92a6c8',500,'text-anchor="end" class="mono"')
    s+='<path d="M36 62H'+str(w-36)+'" stroke="#8b9bbe" stroke-opacity=".17"/>'
    s+=text(36,114,'TECHNICAL LEAD · AI & SOFTWARE',15 if not mobile else 18,'#67e8f9',700,'class="mono" letter-spacing="1.2"')
    s+=text(32,191,'MOHAMED',69 if not mobile else 76,'#f1f5ff',800,'letter-spacing="-2"')
    s+=text(32,269,'GLEIGUEM',69 if not mobile else 76,'#c4b5fd',800,'letter-spacing="-2"')
    s+=text(36,317,'AI systems. Data platforms.',23 if not mobile else 27,'#d8e1f3',500)
    s+=text(36,351,'Security-minded software.',23 if not mobile else 27,'#d8e1f3',500)
    if mobile:
        s+=panel(36,394,528,222,'#22d3ee')
        s+=text(60,431,'~/profile.yml',17,'#67e8f9',500,'class="mono"')
        entries=[('focus:','AI / DATA / SECURITY'),('work:','Richat Partners'),('languages:','AR / FR / EN')]
        for i,(k,v) in enumerate(entries):
            s+=text(60,477+i*42,k,20,'#c4b5fd',500,'class="mono"')+text(205,477+i*42,v,20,'#c5d9e9',500,'class="mono"')
        s+=text(36,661,'BUILD → TEST → REVIEW → SHIP',21,'#6ee7b7',600,'class="mono"')
        s+=text(36,690,'MAURITANIA · ARABIC / FRENCH / ENGLISH',15,'#a5b4ce',500,'class="mono"')
    else:
        # A moving data path around a real profile configuration, not a fake shell session.
        s+='<g class="float">'+panel(620,100,340,290,'#a78bfa')
        for i,col in enumerate(['#fb7185','#fbbf24','#34d399']):s+=f'<circle cx="{642+i*18}" cy="123" r="4" fill="{col}"/>'
        s+=text(936,128,'profile.yml',12,'#92a6c8',500,'text-anchor="end" class="mono"')
        for i,(k,v) in enumerate([('engineer:','Mohamed Gleiguem'),('focus:','AI · Data · Security'),('work:','Richat Partners'),('languages:','[AR, FR, EN]')]):
            s+=text(642,173+i*46,k,14,'#c4b5fd',500,'class="mono"')+text(642,192+i*46,v,14,'#c8daed',500,'class="mono"')
        s+='</g><path class="flow" d="M590 145H602V412H920V400" fill="none" stroke="#22d3ee" stroke-opacity=".7"/>'
        s+='<circle class="pulse" cx="602" cy="412" r="4" fill="#22d3ee"/>'
        s+=text(36,410,'BUILD → TEST → REVIEW → SHIP → LEARN',14,'#6ee7b7',600,'class="mono" letter-spacing=".5"')
        s+='<path d="M36 438H964" stroke="#8b9bbe" stroke-opacity=".17"/>'
        s+=text(36,474,'AI / DATA / SECURITY / WEB / MOBILE / RESEARCH',13,'#b5c4de',500,'class="mono" letter-spacing=".5"')
        s+=text(964,474,'CONTEXT → SYSTEMS → IMPACT',12,'#67e8f9',500,'text-anchor="end" class="mono"')
    return document(w,h,'Mohamed Gleiguem — technical lead, AI, data, security and software engineering',s)


def roles(mobile=False):
    w,h=(600,96) if mobile else (1000,86)
    x=26
    s=text(x,33 if mobile else 30,'ENGINEERING ACROSS',13,'#90a3c4',600,'class="mono" letter-spacing="2"')
    values=['RAG systems & LLM agents','Data platforms & fintech','Cybersecurity & CTFs','Arabic NLP & accessible software']
    for i,value in enumerate(values):
        s+=f'<g class="role {"first" if i==0 else "r"+str(i)}">'+text(x,72 if mobile else 64,value,26 if mobile else 27,COLORS[i],700)+'</g>'
    s+=f'<rect class="cursor" x="{w-40}" y="48" width="10" height="22" rx="1" fill="#22d3ee"/>'
    return document(w,h,'RAG systems, data platforms, cybersecurity, Arabic NLP and accessible software',s)


def header(slug,title,index,color,mobile=False):
    w,h=(600,88) if mobile else (1000,72)
    s=f'<rect x="0" y="0" width="5" height="{h}" fill="{color}"/>'
    s+=text(28,32 if mobile else 26,f'{index:02d} / ENGINEERING NOTEBOOK',12 if not mobile else 15,'#94a7c9',600,'class="mono" letter-spacing="1.5"')
    s+=text(27,66 if mobile else 56,title,27 if not mobile else 30,'#eef2ff',700)
    s+=f'<path class="trace" d="M{w-240} {h-15}H{w-25}" stroke="{color}" stroke-width="2"/>'
    return document(w,h,title,s)


def metrics(mobile=False):
    w,h=(600,340) if mobile else (1000,180)
    data=[('2M+','citizens reached','through donation programs'),('5.5B MRO','distributed','through national programs'),('100K+','documents','in the national knowledge base'),('19.75/20','final-year score','for the ANRPTS platform')]
    s=''
    for i,(value,a,b) in enumerate(data):
        x,y=(20+(i%2)*290,18+(i//2)*160) if mobile else (18+i*246,18)
        cw=270 if mobile else 228
        s+=panel(x,y,cw,144,COLORS[i])
        s+=text(x+20,y+54,value,39 if mobile else 34,COLORS[i],800)
        s+=text(x+20,y+90,a,21 if mobile else 17,'#eef2ff',600)
        s+=lines(x+20,y+116,b,24 if mobile else 25,17 if mobile else 14,pitch=21)
    return document(w,h,'Program impact: 2 million citizens reached; 5.5 billion MRO distributed; 100,000 documents; 19.75 out of 20 final-year score',s)


def focus(mobile=False):
    w,h=(600,350) if mobile else (1000,262)
    x=28
    s=''
    for i,col in enumerate(['#fb7185','#fbbf24','#34d399']):s+=f'<circle cx="{x+i*19}" cy="30" r="5" fill="{col}"/>'
    s+=text(w-28,35,'CURRENT FOCUS / ONGOING',14 if not mobile else 16,'#94a7c9',500,'text-anchor="end" class="mono"')
    s+='<path d="M28 52H'+str(w-28)+'" stroke="#94a7c9" stroke-opacity=".14"/>'
    rows=[('BUILD','RAG & decision platforms','for Mauritanian institutions'),('RESEARCH','Hassaniya NLP & Laghn','corpus, metre and prosody'),('SHIP','Sonora music app','offline audio & Android Media3')]
    for i,(tag,title,sub) in enumerate(rows):
        yy=89+i*(86 if mobile else 57)
        s+=text(x,yy,tag,16,COLORS[i],700,'class="mono"')
        if mobile:
            s+=text(160,yy,title,24,'#eef2ff',600)+text(160,yy+31,sub,20,'#aebbd3')
        else:
            s+=text(165,yy,title,23,'#eef2ff',600)+text(165,yy+27,sub,17,'#aebbd3')
        s+=f'<circle class="pulse" cx="{w-33}" cy="{yy-6}" r="4" fill="{COLORS[i]}" style="animation-delay:{i}s"/>'
    return document(w,h,'Current focus: institutional RAG, Hassaniya NLP research and Sonora',s)


DOMAINS=[
 ('ai','AI & AGENTS','Reason over real knowledge','Source-cited RAG, LLM agents and metadata-filtered retrieval across multilingual documents.','RAG / VECTOR SEARCH / LEGAL NLP'),
 ('data','DATA & FINTECH','Make complex data useful','Multi-source ELT, medallion pipelines, star schemas and fraud analysis for financial workflows.','AIRFLOW / DBT / POSTGRESQL'),
 ('shield','CYBERSECURITY','Think like an adversary','CTF competition, penetration testing and vulnerability assessment, with national-team mentoring.','CTF / BURP SUITE / SECURITY'),
 ('code','FULL-STACK SYSTEMS','Own the whole delivery','APIs, interfaces and banking integrations, from identity verification to government programs.','NEXT.JS / SPRING BOOT / PYTHON'),
 ('mobile','MOBILE & OPERATIONS','Build beyond the browser','Android audio, Flutter projects, containerized services and repeatable delivery workflows.','CAPACITOR / FLUTTER / DOCKER'),
 ('research','LANGUAGE & ACCESSIBILITY','Build for local reality','Arabic poetry, low-resource Hassaniya NLP and Mauritanian sign-language research.','ARABIC NLP / MEDIAPIPE / VISION'),
]
WORK=[
 ('ai','INSTITUTIONAL / PRIVATE','Richat AI platforms','RAG and decision support for the Ministry of Health, Central Bank and ARE telecom regulator.','SOURCE-CITED / MULTILINGUAL'),
 ('data','FINTECH / PRIVATE','Taazour & identity','Donation program platforms, GIMTEL bank integration, liveness and facial verification.','PAYMENTS / KYC / COMPUTER VISION'),
 ('data','DATA ENGINEERING / PRIVATE','ANRPTS analytics','Five heterogeneous sources, dimensional models and a 22-module national reporting dashboard.','AIRFLOW / DBT / NEXT.JS'),
 ('shield','DATATHON / PRIVATE','BAMIS Sentinel','Fraud detection with explainable scoring, graph investigation and reproducible deliverables.','FRAUD ANALYTICS / GRAPH / ML'),
 ('poetry','PERSONAL PROJECT / LIVE','AI Diwan','Poems, poets and verses with Al-Hakim, an AI companion for exploring Arabic poetry.','ARABIC / CULTURE / AI'),
 ('music','OPEN SOURCE / ACTIVE','Sonora Music Hub','Local offline music, a shared React interface and native Android background playback.','REACT / CAPACITOR / MEDIA3'),
]
RESEARCH=[
 ('poetry','ONGOING RESEARCH','Hassaniya NLP · Laghn','Corpus building, metre definitions and computational prosody; dialect adaptation and evaluation are planned.','LOW-RESOURCE NLP / POETRY'),
 ('research','ONGOING RESEARCH','Mauritanian signs','Structuring local sign data and developing hand-detection and normalization pipelines for recognition.','MEDIAPIPE / VISION / CORPORA'),
 ('mobile','IN DESIGN','Samia accessibility','A community-contributed sign dictionary and Arabic/French communication tools for deaf users.','ACCESSIBILITY / LANGUAGE / COMMUNITY'),
]


def cards(title,items,mobile=False):
    w=600 if mobile else 1000
    cols=1 if mobile else 2
    cw=552 if mobile else 472
    ch=310 if mobile else 272
    gap=24
    rows=(len(items)+cols-1)//cols
    h=rows*(ch+gap)+24
    s=''
    for i,(ic,kicker,name,description,tags) in enumerate(items):
        x=24+(i%cols)*(cw+gap);y=24+(i//cols)*(ch+gap);c=COLORS[i%6]
        s+=panel(x,y,cw,ch,c)
        s+=f'<rect x="{x+1}" y="{y+28}" width="3" height="52" rx="1" fill="{c}"/>'
        s+=f'<circle class="pulse" cx="{x+cw-47}" cy="{y+47}" r="29" fill="{c}" fill-opacity=".065"/>'
        s+=icon(ic,x+cw-62,y+32,30,c)
        s+=text(x+24,y+40,kicker,16 if mobile else 12,c,700,'class="mono" letter-spacing="1"')
        s+=text(x+24,y+82,name,30 if mobile else 26,'#eef2ff',700)
        s+=lines(x+24,y+124,description,40 if mobile else 43,25 if mobile else 19,pitch=33 if mobile else 27)
        s+=text(x+24,y+ch-27,tags,15 if mobile else 12,c,600,'class="mono"')
        s+=f'<path class="flow" d="M{x+24} {y+ch-9}H{x+cw-24}" stroke="{c}" stroke-opacity=".35"/>'
    return document(w,h,title,s,'; '.join(v[2]+': '+v[3] for v in items))


def honors(mobile=False):
    data=[('2ND PLACE','International Financial','Security Olympiad','Russia · 2025'),('WINNER','Nouakchott AI Build','Hackathon','Soil & land-use forecasting · 2026'),('RUNNER-UP','DATATHON 2026','BAMIS Bank','Fraud detection · 2026'),('3RD PLACE','0xMR CTF','Pro Hacker level','Competing as MGL · 2026')]
    w=600 if mobile else 1000;cw=552 if mobile else 472;ch=210 if mobile else 196;cols=1 if mobile else 2
    h=((len(data)+cols-1)//cols)*(ch+24)+24;s=''
    for i,(rank,a,b,sub) in enumerate(data):
        x=24+(i%cols)*(cw+24);y=24+(i//cols)*(ch+24);c=COLORS[i]
        s+=panel(x,y,cw,ch,c)+icon('trophy',x+24,y+30,38,c)
        s+=text(x+86,y+50,rank,20,c,800,'class="mono"')
        s+=text(x+24,y+103,a,29 if mobile else 25,'#eef2ff',700)+text(x+24,y+139,b,27 if mobile else 24,'#eef2ff',600)
        s+=text(x+24,y+ch-25,sub,21 if mobile else 17,'#aebbd3')
    return document(w,h,'Recognition: international security olympiad, AI hackathon, datathon and national CTF',s)


def timeline(mobile=False):
    w=600 if mobile else 1000;pitch=190 if mobile else 144;h=pitch*4+38;s=''
    items=[('SEP 2026 → PRESENT','Richat Partners','Technical Lead · AI & Software Engineering'),('JAN → SEP 2026','IBTIKAR Technologies','Full-Stack Engineer · fintech, identity & data'),('MAY → NOV 2025','Macor','Full-Stack Engineer · e-commerce & services'),('2023 → PRESENT','University of Nouakchott','BSc Computer Science → Master’s in AI')]
    s+=f'<path d="M40 54V{h-70}" stroke="#4a5471"/>'
    for i,(period,company,role) in enumerate(items):
        y=24+i*pitch;c=COLORS[i]
        s+=f'<circle cx="40" cy="{y+40}" r="7" fill="{c}"/><circle class="pulse" cx="40" cy="{y+40}" r="15" fill="none" stroke="{c}" stroke-opacity=".3"/>'
        s+=panel(72,y,w-96,pitch-18,c)
        s+=text(94,y+35,period,18 if mobile else 13,c,600,'class="mono"')
        s+=text(94,y+77,company,29 if mobile else 26,'#eef2ff',700)
        s+=lines(94,y+111,role,33 if mobile else 75,23 if mobile else 18,pitch=30)
    return document(w,h,'Experience and education timeline',s)


def stack(mobile=False):
    specs=json.loads((ROOT/'tools/icons.json').read_text())
    cols=3 if mobile else 6;w=600 if mobile else 1000
    cw=172 if mobile else 142;ch=126 if mobile else 112;gap=18
    rows=(len(specs)+cols-1)//cols;h=24+rows*(ch+gap);s=''
    for i,spec in enumerate(specs):
        x=24+(i%cols)*(cw+gap);y=24+(i//cols)*(ch+gap);c=COLORS[i%6]
        s+=panel(x,y,cw,ch,c)
        root=ET.parse(OUT/'icons'/f'{spec["slug"]}.svg').getroot()
        paths=''.join(f'<path d="{escape(p.get("d"),quote=True)}"/>' for p in root.iter() if p.tag.endswith('path'))
        sz=40 if mobile else 34
        s+=f'<g transform="translate({x+(cw-sz)/2} {y+23}) scale({sz/24})" fill="{c}"><g class="icon-bob" style="animation-delay:-{i%8}s">{paths}</g></g>'
        s+=text(x+cw/2,y+ch-24,spec['name'],21 if mobile else 16,'#dbe5f7',600,'text-anchor="middle"')
        s+=f'<path class="trace" d="M{x+15} {y+ch-9}H{x+cw-15}" stroke="{c}" stroke-opacity=".6" style="animation-delay:-{i}s"/>'
    return document(w,h,'Technology stack: '+', '.join(x['name'] for x in specs),s)


def footer(mobile=False):
    w,h=(600,260) if mobile else (1000,240)
    s=f'<ellipse class="aurora" cx="{w-150}" cy="160" rx="440" ry="280" fill="url(#violet)"/>'
    s+=text(32,48,'CONNECT / COLLABORATE / BUILD',15 if mobile else 13,'#67e8f9',700,'class="mono" letter-spacing="1.5"')
    s+=text(30,109,'Let’s build',49 if mobile else 52,'#eef2ff',800,'letter-spacing="-1"')
    s+=text(30,166,'something that matters.',40 if mobile else 52,'#c4b5fd',800,'letter-spacing="-1"')
    s+=text(32,219,'AI · DATA · SECURITY · ACCESSIBLE SOFTWARE',16 if mobile else 17,'#aebbd3',500,'class="mono"')
    s+=f'<path class="flow" d="M32 {h-15}H{w-32}" stroke="#22d3ee" stroke-opacity=".55"/>'
    return document(w,h,'Let’s build something that matters',s)


def contact(label, color):
    body=f'<circle cx="25" cy="25" r="5" fill="{color}"/>'
    body+=text(43,32,label,20,'#eef2ff',600)
    body+=f'<path d="M154 28l6-6m-6 0h6v6" fill="none" stroke="{color}" stroke-width="1.5"/>'
    return document(180,50,label,body)


def main():
    OUT.mkdir(exist_ok=True)
    for slug,label,color in [('email','Email','#a78bfa'),('linkedin','LinkedIn','#22d3ee'),('diwan','AI Diwan','#34d399'),('sonora','Sonora','#fbbf24')]:
        (OUT/f'contact-{slug}.svg').write_text(contact(label,color)+'\n')
    sections=[('focus','On the workbench',1,'#22d3ee'),('impact','Systems with real reach',2,'#34d399'),('domains','Engineering across domains',3,'#a78bfa'),('work','Selected systems & projects',4,'#fb7185'),('research','Research & local languages',5,'#22d3ee'),('stack','Tools behind the work',6,'#60a5fa'),('experience','The path so far',7,'#34d399'),('honors','Competition & community',8,'#fbbf24'),('activity','A year in the commit graph',9,'#a78bfa')]
    for mobile in [False,True]:
        suf='-mobile' if mobile else ''
        generated={'banner':hero(mobile),'roles':roles(mobile),'metrics':metrics(mobile),'focus':focus(mobile),'domains':cards('Engineering domains',DOMAINS,mobile),'work':cards('Selected systems and projects',WORK,mobile),'research':cards('Research in progress',RESEARCH,mobile),'honors':honors(mobile),'timeline':timeline(mobile),'stack':stack(mobile),'footer':footer(mobile)}
        for slug,title,index,color in sections:generated['section-'+slug]=header(slug,title,index,color,mobile)
        for name,svg in generated.items():
            ET.fromstring(svg)
            (OUT/f'{name}{suf}.svg').write_text(svg+'\n',encoding='utf-8')
            print(f'{name}{suf}.svg {len(svg.encode())} bytes')


if __name__=='__main__':
    main()
