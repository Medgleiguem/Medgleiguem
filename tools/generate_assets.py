#!/usr/bin/env python3
"""Render the original desert console and its responsive/static variants."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from desert_console import hero, tools_panel, footer, render_workbench, static_svg

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
    write_variants('desert', hero)
    write_variants('tools-rail', tools_panel)
    write_variants('desert-footer', footer)
    snapshot = json.loads((ROOT/'data/activity.json').read_text())
    write_variants('workbench', lambda mobile: render_workbench(snapshot, mobile))
    for name, source in [('workbench', render_workbench(snapshot, compact=True)), ('tools-rail', tools_panel(compact=True))]:
        for static in (False, True):
            content = static_svg(source) if static else source
            ET.fromstring(content)
            (OUT/(name+'-compact'+('-static' if static else '')+'.svg')).write_text(content+'\n')


if __name__ == '__main__':
    main()
