"""Responsive activity board; data marks stay fixed and decorative paths animate."""
from html import escape
from math import ceil
from activity_data import calendar_days, calendar_stats, weekly_totals, language_shares
from desert_console import WHITE, GOLD, CYAN, MUTED, LEVELS, text, document, route, static_svg

COLORS = [CYAN, GOLD, '#8aa5d6', '#98baa4', '#c18d74']


def heading(y, label, left=40, size=22):
    return text(left,y,label,size,WHITE,'class="mono" letter-spacing="1.4"')


def main_metrics(stats, width, mobile):
    body = ''
    labels = [('contributions','Contributions'),('active_days','Active days'),
              ('current_streak','Current streak'),('longest_streak','Longest streak')]
    left, slot = (24,188) if mobile else (30 if width==700 else 40,(width-80)/4)
    for i,(key,label) in enumerate(labels):
        x = left+(i%2 if mobile else i)*slot
        y = 151+(i//2)*101 if mobile else 153
        value = f'{stats[key]:,}'
        body += text(x,y,value,46 if mobile or width==700 else 54, CYAN if i==0 else WHITE,
                     f'data-metric="{key.replace("_","-")}" font-weight="600" letter-spacing="-1.5"')
        body += text(x,y+35,label,24 if mobile else 22,GOLD if i==0 else MUTED)
        if not mobile and i:
            body += f'<path d="M{x-18} 116v79" stroke="#293f46"/>'
    return body


def year_grid(days, width, mobile):
    offset = (days[0][0].weekday()+1)%7
    columns = ceil((offset+len(days))/7)
    step = 18.5 if mobile else (width-80)/max(53,columns)
    cell = 14 if mobile else step*.77
    left, top = (24,399) if mobile else (30 if width==700 else 40,305)
    blocks = ceil(columns/18) if mobile else 1
    body = ''
    for block in range(blocks):
        subset = [(i,day,count) for i,(day,count) in enumerate(days) if not mobile or (i+offset)//7//18==block]
        block_y = top+block*168
        if mobile:
            label = subset[0][1].strftime('%d %b %Y')+' → '+subset[-1][1].strftime('%d %b %Y')
            body += text(left,block_y-20,label,21,MUTED)
        else:
            last_col = -4
            for i,day,_ in subset:
                col = (i+offset)//7
                if (day.day==1 or (i==0 and day.day<16)) and col-last_col>=3 and col<max(53,columns)-2:
                    body += text(left+col*step,block_y-18,day.strftime('%b'),16 if width==700 else 18,MUTED)
                    last_col=col
        for i,day,count in subset:
            col,row=divmod(i+offset,7)
            if mobile:col%=18
            color = next(color for limit,color in LEVELS if count<=limit)
            body += f'<rect x="{left+col*step:.2f}" y="{block_y+row*step:.2f}" width="{cell:.2f}" height="{cell:.2f}" rx="1.4" fill="{color}" data-date="{day}" data-count="{count}"><title>{day}: {count} contributions</title></rect>'
    bottom = top+(blocks-1)*168+7*step
    legend_y = bottom+(26 if mobile else 24)
    for i,(_,color) in enumerate(LEVELS):
        x=left+i*(70 if mobile else 105)
        body += f'<rect x="{x}" y="{legend_y}" width="17" height="13" rx="1.3" fill="{color}"/>'
        body += text(x+(8 if mobile else 24),legend_y+(43 if mobile else 12),['0','1–4','5–19','20–49','50+'][i],
                     24 if mobile else 19,MUTED,'text-anchor="middle"' if mobile else '')
    return body,legend_y+(75 if mobile else 55)


def weekly_chart(days, stats, width, top, mobile):
    left = 24 if mobile else (30 if width==700 else 40)
    body = heading(top,'RECENT WEEKS',left,24 if mobile else 22)
    note = f'{stats["last_30_days"]:,} in the last 30 days'
    body += text(left if mobile else width-355,top+37 if mobile else top,note,24 if mobile else 22,GOLD)
    weeks = weekly_totals(days)
    peak = max((count for _,count in weeks),default=0)
    chart_top = top+(71 if mobile else 35)
    baseline = chart_top+102
    step = (width-left*2)/max(13,len(weeks))
    for i,(day,count) in enumerate(weeks):
        x = left+i*step
        h = 100*count/peak if peak else 0
        body += f'<rect x="{x:.2f}" y="{baseline-h:.2f}" width="{step*.65:.2f}" height="{h:.2f}" fill="{CYAN if i==len(weeks)-1 else "#366b75"}" data-week="{day}" data-count="{count}"><title>Week of {day}: {count} contributions</title></rect>'
        if not mobile:
            body += text(x,baseline-h-10,f'{count:,}',16,MUTED)
    body += f'<path d="M{left} {baseline}H{width-left}" stroke="#456068"/>'
    body += text(left,baseline+31,weeks[0][0].strftime('%d %b') if weeks else '',21,MUTED)
    body += text(width-left,baseline+31,days[-1][0].strftime('%d %b'),21,MUTED,'text-anchor="end"')
    if mobile:
        body += text(left,baseline+63,'Sunday-based weeks',19,MUTED)
        body += text(left,baseline+89,'First & last weeks may be partial',19,MUTED)
    else:
        body += text(left,baseline+63,'Sunday weeks · edge weeks may be partial',18,MUTED)
    return body,baseline+(126 if mobile else 110)


def type_counters(data, width, top, mobile):
    left = 24 if mobile else (30 if width==700 else 40)
    body = heading(top,'CONTRIBUTION TYPES',left,24 if mobile else 22)
    window=data.get('collection_window')
    period = window['start'][:10]+' → '+window['end'][:10] if window else 'Collection period unavailable'
    body += text(left,top+35,period,22 if mobile else 20,MUTED)
    labels=[('commits','Commits'),('pull_requests','Pull requests'),('issues','Issues opened'),('reviews','PR reviews')]
    for i,(key,label) in enumerate(labels):
        x=left+(i%2 if mobile else i)*((188 if mobile else (width-left*2)/4))
        y=top+101+(i//2)*100 if mobile else top+100
        value=data.get('contribution_types',{}).get(key)
        body += text(x,y,f'{value:,}' if value is not None else '—',40 if mobile else 38,WHITE,f'data-type="{key}" font-weight="600"')
        body += text(x,y+32,label,24 if mobile else 21,MUTED)
    bottom=top+(260 if mobile else 175)
    body += text(left,bottom-4,'Accessible API records',21 if mobile else 19,GOLD)
    return body,bottom+52


def public_languages(data,width,top,mobile):
    left=24 if mobile else (30 if width==700 else 40)
    shares=language_shares(data)
    body=heading(top,'PUBLIC CODE',left,24 if mobile else 22)
    body+=text(left if mobile else left+187,top+34 if mobile else top,'Source bytes · public repositories',20 if mobile else 19,MUTED)
    chart_y=top+(65 if mobile else 31)
    x=left
    for i,item in enumerate(shares):
        w=(width-left*2)*item['percent']/100
        body+=f'<rect x="{x:.3f}" y="{chart_y}" width="{w:.3f}" height="12" fill="{COLORS[i]}" data-language="{escape(item["name"],quote=True)}" data-bytes="{item["bytes"]}"><title>{escape(item["name"])}: {item["percent"]:.1f}% of public source bytes</title></rect>'
        x+=w
    for i,item in enumerate(shares):
        x=left+(i%2 if mobile else i)*(188 if mobile else (width-left*2)/5)
        y=chart_y+54+(i//2)*65 if mobile else chart_y+48
        name=item['name'] if len(item['name'])<=14 else item['name'][:12]+'…'
        body+=f'<path d="M{x} {y-8}h8" stroke="{COLORS[i]}" stroke-width="3"/>'
        body+=text(x+15,y,name,24 if mobile else (19 if width==700 else 21),WHITE)
        body+=text(x+15,y+29,f'{item["percent"]:.1f}%',23 if mobile else 20,MUTED)
    if not shares:
        body+=text(left,chart_y+55,'No public language bytes',23,MUTED)
    bottom=chart_y+(ceil(len(shares)/2)*65+45 if mobile and shares else 130)
    return body,bottom


def render_workbench(data,mobile=False,animated=True,compact=False):
    width=400 if mobile else (700 if compact else 1000)
    left=24 if mobile else (30 if compact else 40)
    days,stats=calendar_days(data),calendar_stats(data)
    body='<style>.activity-flow{stroke-dasharray:8 92;animation-duration:15s}</style>'
    body+=heading(53,'GitHub / activity' if mobile else 'GitHub / year in view',left,29 if mobile else 30)
    body+=text(left,85,f'{days[0][0]} → {days[-1][0]}',21 if mobile else 22,MUTED)
    # The small architectural branch and header line are the only animated layer.
    if not mobile:
        motif='<path d="M0 32V11l11-11 11 11v21M6 32V18l5-5 5 5v14M-4 36h30" fill="none" stroke="'+GOLD+'"/>'
        body+=f'<g transform="translate({width-66} 30)">{motif}</g>'
    body+=route(f'M{left} 100H{width-left}',GOLD,0,'activity-flow')
    body+=main_metrics(stats,width,mobile)
    divider=312 if mobile else 218
    body+=f'<path d="M{left} {divider}H{width-left}" stroke="#2b444b"/>'
    body+=heading(348 if mobile else 256,'CONTRIBUTION CALENDAR',left,23 if mobile else 22)
    grid,bottom=year_grid(days,width,mobile)
    body+=grid
    if not stats['contributions']:
        body+=text(left,bottom,'No contributions in this window',21,MUTED)
        bottom+=38
    chart,bottom=weekly_chart(days,stats,width,bottom+15,mobile)
    body+=chart
    types,bottom=type_counters(data,width,bottom,mobile)
    body+=types
    languages,bottom=public_languages(data,width,bottom,mobile)
    body+=languages
    body+=text(left,bottom+6,'Snapshot '+data['updated_at'][:10]+' UTC',22 if mobile else 20,MUTED)
    body+=text(left,bottom+40,'GitHub-visible contributions',22 if mobile else 20,MUTED)
    height=bottom+69
    body='<rect width="'+str(width)+'" height="'+str(height)+'" fill="#0c1a21"/>'+body
    description=f'Calendar {days[0][0]} to {days[-1][0]}: {stats["contributions"]} contributions, {stats["active_days"]} active days; current streak {stats["current_streak"]} days, longest {stats["longest_streak"]} days, last30 days {stats["last_30_days"]}. Includes a weekly trend, separately scoped API collection counters and public language byte shares. Data marks remain still; header signals are decorative.'
    result=document(width,height,'Med Gleiguem — GitHub activity',description,body,framed=False)
    return result if animated else static_svg(result)
