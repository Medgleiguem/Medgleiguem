#!/usr/bin/env python3
"""Validate local profile assets and keep private repository links out of the README."""
from html.parser import HTMLParser
import base64
from pathlib import Path
import re
from urllib.parse import urlparse, unquote
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


def validate_local_links(source, base=ROOT, repository=ROOT):
    """Reject missing public briefs and links that resolve outside the checkout."""
    links = re.findall(r'(?<!!)\[[^\]]+\]\(([^\s\)]+)\)', source)

    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'a' and dict(attrs).get('href'):
                links.append(dict(attrs)['href'])

    Links().feed(source)
    for value in links:
        url = urlparse(value)
        if url.scheme or url.netloc or not url.path:
            continue
        target = (base/unquote(url.path)).resolve()
        assert target.is_relative_to(repository.resolve()), f'Local link outside repository: {value}'
        assert target.is_file(), f'Missing local link: {value}'


def validate_profile_navigation(source):
    """GitHub prefixes custom HTML IDs; fragment links must address those IDs."""
    ids, fragments = set(), re.findall(r'(?<!!)\[[^\]]+\]\(#([^\s\)]+)\)', source)

    class Anchors(HTMLParser):
        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            if values.get('id'):
                ids.add('user-content-'+values['id'])
            if tag == 'a' and values.get('href', '').startswith('#'):
                fragments.append(values['href'][1:])

    Anchors().feed(source)
    for fragment in fragments:
        assert fragment in ids, f'GitHub navigation target does not match a sanitized custom ID: {fragment}'


def validate_svg(source):
    root = ET.fromstring(source)
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Expected an SVG document')
    ids = [node.get('id') for node in root.iter() if node.get('id')]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate SVG identifier')
    for node in root.iter():
        tag = node.tag.rsplit('}', 1)[-1]
        if tag in ('script', 'foreignObject') or any(key.rsplit('}', 1)[-1].lower().startswith('on') for key in node.attrib):
            raise ValueError('External or executable SVG content')
        if tag == 'image':
            href = node.get('href') or node.get('{http://www.w3.org/1999/xlink}href', '')
            if not href.startswith('data:image/jpeg;base64,'):
                raise ValueError('Only self-contained JPEG bitmap images are allowed')
            try:
                bitmap = base64.b64decode(href.split(',', 1)[1], validate=True)
            except ValueError:
                raise ValueError('Invalid embedded bitmap') from None
            if not bitmap.startswith(b'\xff\xd8\xff') or len(bitmap) > 2_000_000:
                raise ValueError('Invalid or oversized embedded bitmap')
    for reference in re.findall(r'url\(#([^\)]+)\)', source):
        if reference not in ids:
            raise ValueError('Unresolved SVG reference')


def main():
    readme = (ROOT / 'README.md').read_text()
    AssetReferences().feed(readme)
    validate_local_links(readme)
    validate_profile_navigation(readme)
    for brief in (ROOT/'work').glob('*.md'):
        validate_local_links(brief.read_text(), brief.parent)
    for value in re.findall(r'https://[^\s"<>\)]+', readme):
        url = urlparse(value)
        if url.netloc == 'github.com' and url.path.lower().startswith('/medgleiguem/'):
            assert url.path.lower().split('/')[2] in ('sonora-music-hub', 'medgleiguem'), 'Private repository link in README'
    count = 0
    for path in (ROOT / 'assets').rglob('*.svg'):
        validate_svg(path.read_text())
        count += 1
    print(f'Validated {count} SVGs, image paths, alt text, local briefs and repository links.')


if __name__ == '__main__':
    main()
