#!/usr/bin/env python3
"""Build the GitHub-native hacker/anime profile using local art and SVG animation."""
from pathlib import Path
from html import escape
import base64
import json
import textwrap
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
LIME='#b7ff5a'
CYAN='#43e6f6'
WHITE='#e8f4ee'
MUTED='#9ab8b0'


def text(x,y,value,size=22,color=MUTED,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def bitmap(path,x,y,w,h,extra='',position='xMaxYMid slice'):
    data=base64.b64encode((OUT/path).read_bytes()).decode()
    return f'<image href="data:image/jpeg;base64,{data}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{position}" {extra}/>'


def document(w,h,title,body,description=None):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description or title)}. All motion stops for reduced-motion preferences.</desc>
<defs>
 <clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8"/></clipPath>
 <linearGradient id="shade"><stop stop-color="#02090d" stop-opacity=".72"/><stop offset=".52" stop-color="#02090d" stop-opacity=".25"/><stop offset="1" stop-color="#02090d" stop-opacity="0"/></linearGradient>
 <linearGradient id="vertical-shade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#060b0e" stop-opacity="0"/><stop offset=".45" stop-color="#060b0e" stop-opacity=".9"/><stop offset=".7" stop-color="#060b0e"/></linearGradient>
 <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 0H4" stroke="#000" stroke-opacity=".18"/></pattern>
 <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#43e6f6" stop-opacity="0"/><stop offset="1" stop-color="#43e6f6" stop-opacity=".11"/></linearGradient>
</defs>
<style>
text{{font-family:'SFMono-Regular',Consolas,'Liberation Mono',monospace}}
.rain{{animation:rain 1.8s linear infinite}}
.drift{{animation:drift 18s ease-in-out infinite alternate}}
.scan{{animation:scan 9s linear infinite}}
.flow{{stroke-dasharray:6 22;animation:flow 12s linear infinite}}
.glitch{{animation:glitch 9s linear infinite}}
.type-mask{{transform-box:fill-box;transform-origin:left;animation:type 6s steps(28,end) infinite}}
.cursor{{animation:cursor 1.4s steps(2,end) infinite}}
.role{{opacity:0;animation:role 24s linear infinite}}
.role.first{{opacity:1}}.r1{{animation-delay:6s}}.r2{{animation-delay:12s}}.r3{{animation-delay:18s}}
.icon{{animation:icon 8s ease-in-out infinite alternate}}
@keyframes rain{{to{{transform:translate(-26px,110px)}}}}
@keyframes drift{{to{{transform:translate(-8px,-3px) scale(1.015)}}}}
@keyframes scan{{from{{transform:translateY(-500px)}}to{{transform:translateY(700px)}}}}
@keyframes flow{{to{{stroke-dashoffset:-280}}}}
@keyframes glitch{{0%,15%,100%{{transform:translateX(0)}}25%{{transform:translateX(5px)}}35%{{transform:translateX(-4px)}}45%{{transform:translateX(0)}}}}
@keyframes type{{from{{transform:scaleX(0)}}28%,100%{{transform:scaleX(1)}}}}
@keyframes cursor{{50%{{opacity:0}}}}
@keyframes role{{0%,22%{{opacity:1}}25%,100%{{opacity:0}}}}
@keyframes icon{{to{{transform:translateY(-2px)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.role{{opacity:0!important}}.role.first{{opacity:1!important}}}}
</style>
<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="#060b0e"/>{body}</g>
<path d="M1 28V1H28 M{w-28} 1H{w-1}V28 M1 {h-28}V{h-1}H28 M{w-28} {h-1}H{w-1}V{h-28}" fill="none" stroke="#b7ff5a" stroke-opacity=".6"/>
</svg>'''


def entrance(mobile=False):
    w,h=(600,680) if mobile else (1000,470)
    art_h=430 if mobile else h
    s='<g class="drift">'+bitmap(Path('artwork/after-hours-anime.jpg'),0,0,w,art_h)+'</g>'
    if mobile:s+=f'<rect y="260" width="{w}" height="420" fill="url(#vertical-shade)"/>'
    else:s+=f'<rect width="{w}" height="{h}" fill="url(#shade)"/>'
    s+=f'<rect width="{w}" height="{h}" fill="url(#scanlines)"/>'
    # Rain and a quiet CRT sweep are illustration overlays, never activity claims.
    rain=''
    for i in range(42):
        x=10+(i*109)%w;y=-90+(i*71)%(art_h+90)
        rain+=f'<path d="M{x} {y}l-8 34" stroke="#7bd9df" stroke-opacity="{.17+(i%4)*.04:.3f}" stroke-width=".8"/>'
    s+=f'<defs><clipPath id="rain-area"><rect width="{w}" height="{art_h}"/></clipPath></defs><g clip-path="url(#rain-area)"><g class="rain">'+rain+'</g></g>'
    s+=f'<rect class="scan" x="0" y="0" width="{w}" height="100" fill="url(#scan)"/>'
    s+=text(28,35,'MEDGLEIGUEM / PERSONAL WORKSPACE',15 if mobile else 13,LIME,600,'letter-spacing="1"')
    title_y=444 if mobile else 222
    title_size=112 if mobile else 134
    s+=text(28,title_y,'MGL_',title_size,WHITE,800,'letter-spacing="-8"')
    s+=f'<defs><clipPath id="glitch-band"><rect x="26" y="{title_y-65}" width="430" height="16"/></clipPath></defs>'
    s+='<g class="glitch" clip-path="url(#glitch-band)">'+text(31,title_y,'MGL_',title_size,CYAN,800,'letter-spacing="-8"')+'</g>'
    s+=text(34,title_y+49,'BUILD. BREAK. REPEAT.',24 if mobile else 27,LIME,700)
    s+=text(34,title_y+95,'AI / DATA / SECURITY / SYSTEMS',22 if mobile else 20,'#c7dcd3',500)
    s+=text(34,h-28,'~/ideas → ~/experiments → ~/projects',19 if mobile else 15,MUTED)
    if not mobile:s+=text(w-28,h-28,'NOUAKCHOTT / UTC+0',13,'#b9d7ce',500,'text-anchor="end"')
    return document(w,h,'MGL — Medgleiguem. Build. Break. Repeat.',s,'Original anime-inspired hacker workspace over a neon coastal city, with rain, CRT scan and restrained glitch animation')


def terminal(mobile=False):
    w,h=(600,240) if mobile else (1000,208)
    s=f'<rect x="1" y="1" width="{w-2}" height="38" fill="#0b171b"/>'
    for i,c in enumerate([LIME,CYAN,'#46645b']):s+=f'<circle cx="{22+i*18}" cy="20" r="4" fill="{c}"/>'
    s+=text(w-24,25,'med@github:~/workspace',13 if not mobile else 16,MUTED,500,'text-anchor="end"')
    s+=text(26,82,'$ cat interests.txt',23 if mobile else 21,LIME,600)
    s+=f'<defs><clipPath id="typing"><rect class="type-mask" x="26" y="96" width="{w-52}" height="45"/></clipPath></defs>'
    for i,value in enumerate(['RAG / agents / knowledge systems','ELT / data models / analytics','Payments / identity / vision','CTFs / low-resource Arabic NLP']):
        s+=f'<g class="role {"first" if i==0 else "r"+str(i)}" clip-path="url(#typing)">'+text(26,129,value,26 if mobile else 29,WHITE,600)+'</g>'
    s+=text(26,184 if mobile else 177,'$ explore ./projects',23 if mobile else 21,LIME,500)
    s+=f'<rect class="cursor" x="{310 if mobile else 286}" y="{166 if mobile else 160}" width="12" height="22" fill="{LIME}"/>'
    if mobile:s+=text(26,220,'code / learn / iterate',18,MUTED)
    return document(w,h,'Terminal intro: RAG, data platforms, identity, payments, security and Arabic NLP',s)



def wrapped(x,y,value,width,size=20,color=MUTED,pitch=None):
    return ''.join(text(x,y+i*(pitch or size*1.4),line,size,color) for i,line in enumerate(textwrap.wrap(value,width)))


def section(name,mobile=False):
    w,h=(600,84) if mobile else (1000,70)
    body=text(24,31,'MGL / WORKSPACE',14 if mobile else 12,MUTED,500)
    body+=text(24,65 if mobile else 55,'./'+name,30 if mobile else 28,LIME,700)
    body+=f'<path class="flow" d="M{w-240} 47H{w-24}" stroke="{CYAN}" stroke-opacity=".6"/>'
    return document(w,h,'./'+name,body)


def systems(group,mobile=False):
    items=json.loads((ROOT/'tools/projects.json').read_text())[group]
    w,h=(600,900) if mobile else (1000,520)
    label='AI + KNOWLEDGE SYSTEMS' if group=='ai' else 'DATA + IDENTITY + PAYMENTS'
    s=text(24,34,label,22 if mobile else 20,LIME,700)
    s+=text(24,63,'PRIVATE CODE / ENGINEERING SCOPE MAPS',15 if mobile else 12,MUTED)
    s+='<defs><marker id="flow-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#43e6f6"/></marker></defs>'
    s+='<style>.module{opacity:0;animation:module 24s linear infinite}.module.first{opacity:1}.m1{animation-delay:6s}.m2{animation-delay:12s}.m3{animation-delay:18s}@keyframes module{0%,22%{opacity:1}25%,100%{opacity:0}}@media(prefers-reduced-motion:reduce){.module{opacity:0!important}.module.first{opacity:1!important}}</style>'
    for i,item in enumerate(items):
        yy=112+i*(83 if mobile else 91)
        xx=40
        s+=text(xx,yy,item['name'],25 if mobile else 20,WHITE,600)
        s+=wrapped(xx,yy+28,item['scope'],43 if mobile else 39,20 if mobile else 14,pitch=25 if mobile else 20)
        # The active row and diagram share one clock; the file list remains readable.
        s+=f'<g class="module {"first" if i==0 else "m"+str(i)}"><rect x="22" y="{yy-23}" width="3" height="58" fill="{LIME}"/></g>'
        if not mobile:s+=f'<path d="M24 {yy+56}H454" stroke="#1c302a"/>'
    gx,gy,gw=(24,460,552) if mobile else (486,88,490)
    gh=376 if mobile else 360
    s+=f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="5" fill="#0b1418" stroke="#274638"/>'
    for i,item in enumerate(items):
        content=text(gx+20,gy+35,item['name'],26 if mobile else 24,LIME,700)
        content+=text(gx+20,gy+67,'PROJECT MAP / PRIVATE SOURCE',15 if mobile else 12,MUTED)
        node_w=(gw-64)/2;node_h=54 if mobile else 48
        left=gx+20;right=gx+gw-20-node_w
        top=gy+106;bottom=gy+222
        positions=[(left,top),(right,top),(right,bottom),(left,bottom)]
        for j,(node,(nx,ny)) in enumerate(zip(item['nodes'],positions)):
            content+=f'<rect x="{nx}" y="{ny}" width="{node_w}" height="{node_h}" rx="3" fill="#08100d" stroke="#345e45"/>'
            content+=text(nx+7,ny+14,str(j+1).zfill(2),12 if mobile else 10,MUTED)
            # Two-line node labels prevent tiny text on phone layouts.
            pieces=textwrap.wrap(node,17 if mobile else 18)
            size=19 if mobile else 15
            for k,line in enumerate(pieces):
                baseline=ny+(node_h/2)+(size*.35)+(k-(len(pieces)-1)/2)*(size+3)
                content+=text(nx+node_w/2,baseline,line,size,WHITE,500,'text-anchor="middle"')
        paths=[f'M{left+node_w} {top+node_h/2}H{right}',f'M{right+node_w/2} {top+node_h}V{bottom}',f'M{right} {bottom+node_h/2}H{left+node_w}']
        for path in paths:content+=f'<path class="flow" d="{path}" stroke="{CYAN}" stroke-width="2" fill="none" marker-end="url(#flow-arrow)"/>'
        content+=wrapped(gx+20,gy+gh-36,item['stack'],40 if mobile else 43,19 if mobile else 14,CYAN,pitch=24)
        s+=f'<g class="module {"first" if i==0 else "m"+str(i)}">{content}</g>'
    if not mobile:s+='<path d="M470 88V448" stroke="#1a3027"/>'
    s+=text(24,h-27,'AUTO TOUR / 4 PROJECTS / SOURCE REMAINS PRIVATE',15 if mobile else 13,MUTED)
    return document(w,h,label,s,'; '.join(item['name']+': '+item['scope']+' Flow: '+', '.join(item['nodes']) for item in items))


def research(mobile=False):
    w=600 if mobile else 1000;pitch=210 if mobile else 160;h=pitch*2+60
    items=[('hassaniya-laghn/','Corpus, metre rules and computational prosody.','COLLECT → NORMALIZE → CHECK METRE → REVIEW'),('mauritanian-signs/','Local sign corpus and recognition research.','COLLECT → DETECT HANDS → NORMALIZE → EVALUATE')]
    s=text(24,33,'RESEARCH / IN PROGRESS',16 if mobile else 13,CYAN,600)
    for i,(name,scope,flow) in enumerate(items):
        y=82+i*pitch
        s+=text(24,y,name,29 if mobile else 28,LIME,600)
        s+=wrapped(24,y+40,scope,38 if mobile else 75,24 if mobile else 21,pitch=31)
        s+=wrapped(24,y+(116 if mobile else 88),flow,37 if mobile else 75,20 if mobile else 18,CYAN,pitch=27)
        s+=f'<path class="flow" d="M24 {y+pitch-31}H{w-24}" stroke="#345e45"/>'
    return document(w,h,'Hassaniya Laghn and Mauritanian Sign Language research',s)


def arsenal(mobile=False):
    specs=json.loads((ROOT/'tools/icons.json').read_text())
    cols=3 if mobile else 6;cw=172 if mobile else 146;ch=108 if mobile else 85;gap=18
    w=600 if mobile else 1000;h=56+((len(specs)+cols-1)//cols)*(ch+gap)
    s=text(24,31,'LOADOUT // PICK THE RIGHT TOOL',15 if mobile else 13,LIME,600)
    for i,spec in enumerate(specs):
        x=24+(i%cols)*(cw+gap);y=56+(i//cols)*(ch+gap);color=LIME if i%3 else CYAN
        root=ET.parse(OUT/'icons'/f'{spec["slug"]}.svg').getroot()
        paths=''.join(f'<path d="{escape(p.get("d"),quote=True)}"/>' for p in root.iter() if p.tag.endswith('path'))
        size=36 if mobile else 30
        s+=f'<g transform="translate({x+(cw-size)/2} {y+8}) scale({size/24})" fill="{color}"><g class="icon" style="animation-delay:-{i%8}s">{paths}</g></g>'
        s+=text(x+cw/2,y+ch-23,spec['name'],20 if mobile else 15,WHITE,500,'text-anchor="middle"')
        s+=f'<path d="M{x+15} {y+ch-4}H{x+cw-15}" stroke="#203a2e"/>'
    return document(w,h,'Technical loadout: '+', '.join(s['name'] for s in specs),s)


def contact(label,mobile=False):
    w,h=180,48
    s=f'<rect x="1" y="1" width="178" height="46" rx="4" fill="#0b1418" stroke="#234432"/>'
    s+=text(18,31,'↗',23,LIME,600)+text(48,30,label,18,WHITE,500)
    return document(w,h,label,s)


def signoff(mobile=False):
    w,h=(600,180) if mobile else (1000,150)
    s=f'<path class="flow" d="M{w-180} 20l-45 55 45 55m80-110 45 55-45 55" fill="none" stroke="#43e6f6" stroke-opacity=".12" stroke-width="3"/>'
    s+=text(26,65,'See you in the next commit.',30 if mobile else 34,LIME,700)
    s+=text(26,112,'CTFs / chess / Arabic poetry',21 if mobile else 19,WHITE)
    s+=f'<path class="flow" d="M26 {h-15}H{w-26}" stroke="{CYAN}"/>'
    return document(w,h,'See you in the next commit — CTFs, chess and Arabic poetry',s)


def main():
    OUT.mkdir(exist_ok=True)
    for mobile in [False,True]:
        suffix='-mobile' if mobile else ''
        assets={'entrance':entrance(mobile),'terminal':terminal(mobile),'systems-ai':systems('ai',mobile),'systems-platforms':systems('platforms',mobile),'research':research(mobile),'arsenal':arsenal(mobile),'signoff':signoff(mobile)}
        for label in ['projects','research','arsenal','activity']:
            assets['section-'+label]=section(label,mobile)
        for name,source in assets.items():
            ET.fromstring(source)
            (OUT/f'{name}{suffix}.svg').write_text(source+'\n')
            print(name+suffix+'.svg',len(source.encode()))
    for label in ['email','linkedin','side-quests']:
        (OUT/f'contact-{label}.svg').write_text(contact(label)+'\n')


if __name__=='__main__':main()
