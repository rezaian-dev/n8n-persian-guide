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

for filename in ['index.html']:
 page=Check();page.feed((ROOT/'docs'/filename).read_text())
 for ref in page.refs:
  if ref.startswith('#'):
   if ref!='#':assert ref[1:] in page.ids,f'Missing anchor: {ref}'
  elif not ref.startswith(('https:','http:','mailto:','data:')):
   path,_,fragment=ref.partition('#')
   assert (ROOT/'docs'/path).is_file(),f'Missing local asset: {ref}'
   if fragment and path.endswith('.html'):
    other=Check();other.feed((ROOT/'docs'/path).read_text());assert fragment in other.ids,ref
 assert page.images>=2
 print(f'{filename}: {len(page.ids)} unique ids, {len(page.refs)} references checked.')
for f in ['guide.md','README.md','SECURITY.md','LICENSE.md','deploy/.env.example','workflows/lead-intake.json','docs/N8N-Persian-Guide.pdf','.gitattributes']:
 assert (ROOT/f).is_file(),f'Missing required file: {f}'
json.loads((ROOT/'workflows/lead-intake.json').read_text())
print('All local link and required-file checks passed.')

attributes=(ROOT/'.gitattributes').read_text()
assert '*.py linguist-detectable=false' in attributes
assert 'docs/assets/vendor/** linguist-vendored=true' in attributes
landing=(ROOT/'docs/index.html').read_text()
assert 'cover-3d' not in landing
assert all(f'id="{key}"' in landing for key in ['chapter-search','page-preview','mobile-download'])
print('Flat-cover, progressive-enhancement and Linguist configuration checks passed.')

assert all(f'id="{key}"' in landing for key in ['primary-nav','menu-toggle','footer'])
assert 'site-footer' in landing and 'site-header' in landing
assert '*.py linguist-detectable=false linguist-generated=true linguist-vendored=true' in attributes
print('Responsive shell and Python-exclusion rules verified.')
