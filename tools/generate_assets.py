#!/usr/bin/env python3
"""Render the original desert console and its responsive/static variants."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from desert_console import static_svg
from activity_dashboard import render_workbench
from activity_data import activity_summary
from expertise import DOMAINS, hero, domain_row, toolbox

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'


def write_variants(name, renderer):
    for mobile in (False, True):
        source = renderer(mobile)
        suffix = '-mobile' if mobile else ''
        for static in (False, True):
            content = static_svg(source) if static else source
            ET.fromstring(content)
            path = OUT / (name+suffix+('-static' if static else '')+'.svg')
            path.write_text(content+'\n')
            print(path.name, len(content.encode()), 'bytes')


def main():
    OUT.mkdir(exist_ok=True)
    (OUT/'domains').mkdir(exist_ok=True)
    write_variants('desert', hero)
    for slug in DOMAINS:
        write_variants('domains/'+slug, lambda mobile, slug=slug: domain_row(slug, mobile))
        for static in (False, True):
            source = domain_row(slug, compact=True)
            content = static_svg(source) if static else source
            ET.fromstring(content)
            (OUT/'domains'/(slug+'-compact'+('-static' if static else '')+'.svg')).write_text(content+'\n')
    snapshot = json.loads((ROOT/'data/activity.json').read_text())
    write_variants('workbench', lambda mobile: render_workbench(snapshot, mobile))
    write_variants('toolbox', toolbox)
    (ROOT/'work').mkdir(exist_ok=True)
    (ROOT/'work/activity.md').write_text(activity_summary(snapshot))
    for name, source in [('workbench', render_workbench(snapshot, compact=True)),('toolbox',toolbox(compact=True))]:
        for static in (False, True):
            content = static_svg(source) if static else source
            ET.fromstring(content)
            (OUT/(name+'-compact'+('-static' if static else '')+'.svg')).write_text(content+'\n')


if __name__ == '__main__':
    main()
