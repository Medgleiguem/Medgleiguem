"""Compact project identities and bespoke vector drawings for the visual gallery."""
from html import escape

PROJECTS = {
    'health-ministry': ('Health Ministry AI', 'Scoped evidence. Human decisions.', 'system'),
    'central-bank': ('Central Bank / RKF', 'Sources, versions, citations.', 'system'),
    'are-intelligence': ('ARE Intelligence', 'Regulatory evidence → obligations.', 'system'),
    'national-knowledge': ('National Knowledge Base', 'Imports, provenance, review.', 'system'),
    'anrpts': ('ANRPTS / BI Houwiyeti', 'Heterogeneous sources → analytics.', 'system'),
    'kyc-identity': ('KYC Identity', 'Capture / liveness / matching.', 'system'),
    'taazour-aoun': ('Taazour Aoun', 'Eligibility → identity → wallet.', 'system'),
    'taazour-pay': ('Taazour Pay', 'Household boundaries. Payment state.', 'system'),
    'hassaniya-laghn': ('Hassaniya Laghn', 'Corpus / metre / rhyme.', 'research'),
    'mauritanian-sign-language': ('Mauritanian Sign Language', 'Quality checks. Subject-aware splits.', 'research'),
}

STYLE = '''
.packet{stroke-dasharray:12 90;animation:packet 7s linear infinite}
.float{animation:float 9s ease-in-out infinite alternate}
.scanner{animation:scanner 8s ease-in-out infinite}
@keyframes packet{to{stroke-dashoffset:-408}}
@keyframes float{to{transform:translateY(-10px)}}
@keyframes scanner{0%,100%{transform:translateY(0);opacity:.3}50%{transform:translateY(120px);opacity:.9}}
'''


def label(x, y, value, size=18, color='#a7bacc', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'


def route(path, delay=0):
    return f'<path d="{path}" fill="none" stroke="#345269" stroke-width="2"/><path class="packet" style="animation-delay:-{delay}s" d="{path}" fill="none" stroke="#a4d3ee" stroke-width="3"/>'


def sheet(x, y, width=86, height=103):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="5" fill="#102435" stroke="#7da5bf"/><path d="M{x+16} {y+25}h{width-32}m-{width-32} 20h{width-32}m-{width-32} 20h{width-45}" stroke="#8eafc7" stroke-width="2"/>'


def draw_project(slug):
    """Return a distinct diagram in the shared 720×370 card coordinate system."""
    if slug == 'health-ministry':
        return (sheet(75,155)+sheet(90,167)+route('M180 216H303')+
            '<g fill="none" stroke="#a4d3ee"><circle cx="360" cy="216" r="43"/><circle class="glow" cx="360" cy="216" r="55" stroke-dasharray="3 12"/><path d="M345 216h30m-15-15v30"/></g>'+route('M415 216H536',3)+
            '<rect x="536" y="180" width="130" height="75" rx="8" fill="#122536" stroke="#dbb277"/><circle cx="600" cy="203" r="9" fill="none" stroke="#e5c797"/><path d="M582 234q0-25 18-25t18 25" fill="none" stroke="#e5c797"/>'+label(94,298,'SOURCES')+label(330,298,'SCOPE')+label(568,298,'REVIEW'))
    if slug == 'central-bank':
        s=route('M90 220H255',2)+route('M430 220H630',4)
        for i in range(3):
            s+=f'<g class="float" style="animation-delay:-{i*2}s">'+sheet(270+i*27,160-i*9,112,128)+label(285+i*27,269-i*9,'v'+str(i+1),17,'#dbb277')+'</g>'
        for i in range(3):
            s+=f'<circle class="glow" style="animation-delay:-{i*2}s" cx="{530+i*43}" cy="220" r="7" fill="#dbb277"/>'
        return s+label(90,301,'IDENTITY')+label(290,316,'VERSIONS')+label(525,301,'CITATIONS')
    if slug == 'are-intelligence':
        s=''
        for row in range(3):
            for col in range(4):
                s+=f'<rect class="glow" style="animation-delay:-{row+col}s" x="{85+col*39}" y="{155+row*40}" width="24" height="24" rx="3" fill="#24455c" stroke="#90bfd8"/>'
        s+=route('M248 207H370',3)
        for i in range(3):
            s+=f'<rect x="400" y="{155+i*45}" width="230" height="28" rx="5" fill="#102434" stroke="#405f74"/><path class="packet" style="animation-delay:-{i*2}s" d="M414 {169+i*45}H615" stroke="#dbb277" stroke-width="2"/>'
        return s+label(85,303,'EVIDENCE')+label(400,303,'OBLIGATIONS')
    if slug == 'national-knowledge':
        s=''
        for i in range(3):
            s+=f'<g class="float" style="animation-delay:-{i*2}s"><rect x="{88+i*18}" y="{154+i*27}" width="172" height="58" rx="5" fill="#102535" stroke="#7ea5bd"/><path d="M{106+i*18} {174+i*27}h80m-80 16h115" stroke="#779fb9"/></g>'
        s+=route('M300 218H464',2)
        s+='<path d="M470 180h58l17 15h110v82H470Z" fill="#122a3c" stroke="#a7c9de"/><path d="M489 218h141m-141 20h95" stroke="#dbb277" stroke-width="2"/>'
        return s+label(100,310,'PROVENANCE')+label(485,310,'STAFF REVIEW')
    if slug == 'anrpts':
        s=''
        for i,name in enumerate(['MongoDB','PostgreSQL','MySQL']):
            y=157+i*58
            s+=f'<ellipse cx="140" cy="{y}" rx="60" ry="10" fill="#122a3b" stroke="#a0c8df"/><path d="M80 {y}v23q60 20 120 0v-23" fill="none" stroke="#86b5cf"/>'+label(140,y+23,name,16,extra='text-anchor="middle"')
            s+=route(f'M208 {y+16}Q265 {y+16} 320 223',i*2)
        s+='<rect x="320" y="187" width="87" height="70" rx="6" fill="#173347" stroke="#dbb277"/>'+label(335,229,'ELT',23,'#e5c797')+route('M408 223H510',2)
        for row in range(2):
            for col in range(3):
                s+=f'<rect class="glow" style="animation-delay:-{row+col*2}s" x="{520+col*45}" y="{180+row*48}" width="30" height="30" rx="3" fill="#24465d" stroke="#9ec6dc"/>'
        return s+label(520,304,'ANALYTICAL VIEWS',16)
    if slug == 'kyc-identity':
        s='<g transform="translate(225 114)" fill="none" stroke="#8cc6e8" stroke-width="2"><path d="M65 15L119 35L155 92L131 146L77 173L30 140L8 83L30 34Z M30 34L119 35L30 140L131 146L8 83L155 92L65 15L77 173" opacity=".65"/><circle class="glow" cx="52" cy="81" r="4"/><circle class="glow" style="animation-delay:-3s" cx="110" cy="81" r="4"/></g><path d="M234 168v-30h30m140 0h30v30M234 265v30h30m140 0h30v-30" fill="none" stroke="#dbb277" stroke-width="2"/><path class="scanner" d="M247 153H422" stroke="#c1e8fc" stroke-width="2"/>'
        for i,value in enumerate(['CAPTURE','LIVENESS','MATCH']):
            x=79+i*238
            s+=f'<circle class="glow" style="animation-delay:-{i*2}s" cx="{x}" cy="313" r="4" fill="#dbb277"/>'+label(x+12,319,value,17)
        return s
    if slug == 'taazour-aoun':
        s=route('M174 210H292',1)+route('M424 210H542',4)
        s+='<g fill="none" stroke="#a2c9e1" stroke-width="2"><rect x="68" y="167" width="106" height="86" rx="8"/><circle cx="122" cy="193" r="12"/><path d="M99 232q0-28 23-28t23 28"/><rect x="292" y="177" width="132" height="66" rx="8"/><rect x="542" y="172" width="112" height="79" rx="8"/><path d="M542 190h112m-28 23h28"/></g>'
        for i in range(5):
            s+=f'<circle class="glow" style="animation-delay:-{i}s" cx="{310+i*24}" cy="210" r="5" fill="#dbb277"/>'
        return s+label(70,299,'ELIGIBILITY')+label(309,299,'OTP/eKYC')+label(564,299,'WALLET')
    if slug == 'taazour-pay':
        s='<g class="flow" fill="none" stroke="#dbb277" opacity=".6"><ellipse cx="360" cy="220" rx="187" ry="68" stroke-dasharray="3 22"/></g>'+route('M150 220H297',2)+route('M421 220H565',5)
        s+='<path d="M294 196l66-48 66 48v82H294Z" fill="#132c3f" stroke="#a4cde3"/><path d="M346 221v-12a14 14 0 0 1 28 0v12m-33 0h38v34h-38Z" fill="none" stroke="#e4bd82" stroke-width="2"/>'
        for x in [132,586]:
            s+=f'<circle cx="{x}" cy="220" r="25" fill="#122b3d" stroke="#86b8d4"/><circle class="glow" cx="{x}" cy="220" r="7" fill="#b7dcee"/>'
        return s+label(79,306,'PROVIDERS')+label(275,315,'HOUSEHOLD LOCK')+label(548,306,'STATE')
    if slug == 'hassaniya-laghn':
        s=''
        for row in range(2):
            y=175+row*75
            s+=f'<path d="M65 {y}H650" stroke="#2d495e"/>'
            for n in range(7):
                x=78+n*80
                d=f'M{x} {y-15}v30m15-30v30' if (n+row)%2==0 else f'M{x} {y}h37'
                s+=f'<path class="meter" style="animation-delay:-{n+row}s" d="{d}" stroke="#dcbb86" stroke-width="3"/>'
        return s+'<path class="flow" d="M650 175q45 38 0 75" fill="none" stroke="#a4d3ee" stroke-width="2"/>'+label(65,310,'ILLUSTRATIVE SCANSION / EXPLICIT RULES',17)
    if slug == 'mauritanian-sign-language':
        hand='M125 180L85 153L65 122L48 91L35 71M125 180L95 118L93 80L91 48L91 23M125 180L125 108L125 64L125 31L125 6M125 180L154 118L160 77L163 48L165 26M125 180L178 136L192 109L202 88L210 69M95 118L125 108L154 118L178 136'
        s=f'<g transform="translate(125 126)" fill="none" stroke="#96c9e6" stroke-width="2"><path d="{hand}" opacity=".4"/><path class="trace" d="{hand}"/></g>'+route('M360 222H435',2)
        for i,value in enumerate(['TRAIN','VALIDATE','TEST']):
            y=157+i*63
            s+=f'<rect x="477" y="{y}" width="145" height="35" rx="5" fill="#132b3d" stroke="#6e9fbf"/>'+label(494,y+24,value,18)+route(f'M435 222L477 {y+18}',i*2)
        return s+label(117,322,'SYNTHETIC LANDMARKS',16)
    raise ValueError('Unknown project drawing: '+slug)
