#!/usr/bin/env python3
"""Check deployable local references, accessibility basics and source sync (stdlib)."""
from pathlib import Path
from html.parser import HTMLParser
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.images=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ('href','src','data-src'):
            if a.get(k):self.refs.append(a[k])
        if tag=='img':
            assert 'alt' in a,'Image has no alt text';self.images+=1
        if 'aria-controls' in a:self.refs.append('#'+a['aria-controls'])
        if 'aria-labelledby' in a:
            self.refs.extend('#'+t for t in a['aria-labelledby'].split())
p=Page();p.feed((ROOT/'index.html').read_text())
assert len(p.ids)==len(set(p.ids)),'Duplicate element IDs'
for ref in p.refs:
    if ref.startswith('#'):assert ref[1:] in p.ids,'Broken anchor: '+ref
    elif ref.startswith('./'):assert (ROOT/ref[2:]).is_file(),'Missing local resource: '+ref
    else:assert ref.startswith('https://'),'Unexpected path or scheme: '+ref
for svg in (ROOT/'assets').rglob('*.svg'):ET.parse(svg)
for item in ('content.json','config/site.json','assets/ASSET_CREDITS.json'):json.loads((ROOT/item).read_text())
c=json.loads((ROOT/'content.json').read_text());config=json.loads((ROOT/'config/site.json').read_text())
assert isinstance(config['demo']['enabled'],bool),'demo.enabled must be boolean'
assert all(isinstance(m['placeholder'],bool) for m in c['media'].values()),'media.placeholder must be boolean'
assert isinstance(c['contribution']['enabled'],bool),'contribution.enabled must be boolean'
for ref in config['video'].values():
    if isinstance(ref,str) and ref.startswith('./'):
        path=(ROOT/ref[2:]).resolve()
        assert path.is_relative_to(ROOT) and path.is_file(),'Missing configured video resource: '+ref
subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--check'],check=True)
print(f'PASS: {len(p.ids)} unique IDs, {len(p.refs)} references, {p.images} images; SVG/JSON/source checks passed.')
