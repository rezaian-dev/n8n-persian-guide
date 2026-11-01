"""Check generated HTML local links, heading anchors, and required files."""
from pathlib import Path
from html.parser import HTMLParser
import json
ROOT=Path(__file__).resolve().parents[1]
class Check(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.refs=[];self.images=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids, f"Duplicate id: {a['id']}"
   self.ids.add(a['id'])
  for key in ['src','href']:
   if key in a:self.refs.append(a[key])
  if tag=='img':assert a.get('alt'), 'Image missing alt';self.images+=1
page=Check();page.feed((ROOT/'docs/index.html').read_text())
for ref in page.refs:
 if ref.startswith('#'):
  if ref!='#':assert ref[1:] in page.ids,f'Missing anchor: {ref}'
 elif not ref.startswith(('https:','http:','mailto:','data:')):
  assert (ROOT/'docs'/ref).is_file(),f'Missing local asset: {ref}'
assert page.images>=2
for f in ['guide.md','README.md','SECURITY.md','LICENSE.md','deploy/.env.example','workflows/lead-intake.json']:
 assert (ROOT/f).is_file(),f'Missing required file: {f}'
json.loads((ROOT/'workflows/lead-intake.json').read_text())
print(f'HTML checks passed: {len(page.ids)} unique ids, {len(page.refs)} references, {page.images} author images.')
