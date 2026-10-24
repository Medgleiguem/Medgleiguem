#!/usr/bin/env python3
"""Validate local profile assets and keep private repository links out of the README."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class AssetReferences(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('img', 'source'):
            value = attrs.get('src') or attrs.get('srcset')
            assert value and value.startswith('./'), f'Expected local image: {value}'
            assert (ROOT / value).is_file(), f'Missing image: {value}'
            if tag == 'img':
                assert attrs.get('alt'), f'Missing alternative text: {value}'


def main():
    readme = (ROOT / 'README.md').read_text()
    AssetReferences().feed(readme)
    for value in re.findall(r'https://[^\s"<>\)]+', readme):
        url = urlparse(value)
        if url.netloc == 'github.com' and url.path.lower().startswith('/medgleiguem/'):
            assert url.path.lower().split('/')[2] in ('sonora-music-hub', 'medgleiguem'), 'Private repository link in README'
    count = 0
    for path in (ROOT / 'assets').rglob('*.svg'):
        root = ET.parse(path).getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg', f'Not SVG: {path}'
        ids = [node.get('id') for node in root.iter() if node.get('id')]
        assert len(ids) == len(set(ids)), f'Duplicate SVG identifier: {path}'
        for node in root.iter():
            assert node.tag.rsplit('}', 1)[-1] not in ('script', 'foreignObject', 'image'), f'External or executable SVG content: {path}'
        for reference in re.findall(r'url\(#([^\)]+)\)', path.read_text()):
            assert reference in ids, f'Unresolved SVG reference in {path}'
        count += 1
    print(f'Validated {count} SVGs, README image paths, alt text and repository links.')


if __name__ == '__main__':
    main()
