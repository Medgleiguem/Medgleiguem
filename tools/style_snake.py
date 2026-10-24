#!/usr/bin/env python3
"""Match the contribution animation to the profile and create a static fallback."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])

def main():
    path=ROOT/'output/github-snake-dark.svg'
    root=ET.fromstring(path.read_text())
    x,y,w,h=root.get('viewBox').split()
    # Background includes the SVG's padding and works in either GitHub theme.
    old=root.find(f'{NS}rect[@id="profile-background"]')
    if old is not None:root.remove(old)
    root.insert(0,ET.Element(NS+'rect',{'id':'profile-background','x':x,'y':y,'width':w,'height':h,'rx':'14','fill':'#060b0e'}))
    style=root.find(NS+'style')
    style.text=re.sub(r'/\* profile-motion \*/.*?$', '', style.text,flags=re.S)
    style.text+='\n/* profile-motion */\n@media(prefers-reduced-motion:reduce){*{animation:none!important}}\n'
    path.write_text(ET.tostring(root,encoding='unicode')+'\n')
    for child in list(root):
        if child.tag==NS+'rect' and set(child.get('class','').split()) & {'s','u'}:root.remove(child)
    style.text=re.sub(r'@keyframes\s+[^\s{]+\s*\{(?:[^{}]|\{[^{}]*\})*\}', '', style.text)
    style.text+='\n*{animation:none!important}\n'
    (ROOT/'assets/contributions-static.svg').write_text(ET.tostring(root,encoding='unicode')+'\n')

if __name__=='__main__':main()
