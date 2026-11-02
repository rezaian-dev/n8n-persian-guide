"""Validate the repository, website and distributed PDF in one command."""
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
for f in ['guide.md','README.md','LICENSE.md','deploy/.env.example','workflows/lead-intake.json','docs/N8N-Persian-Guide.pdf','.gitattributes']:
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

# Publication audit: kept here so one entry point validates the complete release.
import hashlib, re
import fitz
meta=json.loads((ROOT/'docs/assets/book-meta.json').read_text())
file=ROOT/'docs/N8N-Persian-Guide.pdf';pdf=fitz.open(file)
assert len(pdf)==meta['pages']
assert file.stat().st_size==meta['bytes']
assert hashlib.sha256((ROOT/'guide.md').read_bytes()).hexdigest()==meta['source_sha256'], 'PDF is stale relative to guide.md'
layout_files=['scripts/build_pdf.py','scripts/book.css','scripts/book-notes.json','scripts/build_figures.py','docs/assets/cover-art.webp','docs/assets/author.webp','scripts/icons.json']
assert hashlib.sha256(b''.join((ROOT/f).read_bytes() for f in layout_files)).hexdigest()==meta['layout_sha256'], 'PDF layout sources have changed; rebuild the PDF'
source=(ROOT/'guide.md').read_text()
assert len(re.findall(r'^#### پرسش ',source,re.M))==52
assert len(re.findall(r'^### سناریوی ',source,re.M))==24
assert meta['interview_questions']==76 and meta['chapters']==26 and meta['projects']==3
assert len(meta['chapter_pages'])==len(re.findall(r'^## ',source,re.M))
assert meta['chapter_pages'][0]==meta['toc_pages']+3
assert meta['toc_pages']==3
assert sum(page.get_text().count('.') for page in pdf[2:5])>=100, 'Missing dotted leaders'
assert sum(len(page.get_links()) for page in pdf[2:5])>=29, 'Missing chapter destinations'
assert meta['chapter_icons']==26 and meta['pdf_icons']==29
assert meta['placed_icons']==meta['icon_slots_checked']==130
assert meta['icon_text_overlaps']==0 and meta['icon_center_errors']==0
assert len(pdf.get_toc())>=190, 'Missing hierarchical bookmarks'
assert all(len(page.get_text().strip())>30 for page in pdf), 'Empty or image-only page'
internal=[link for page in pdf for link in page.get_links() if link.get('page',-1)>=0]
assert len(internal)>=29
assert all(link['page']<len(pdf) for link in internal)
for i,page in enumerate(pdf):
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   for span in line['spans']:
    x0,y0,x1,y1=span['bbox']
    assert x0>=-.5 and y0>=-.5 and x1<=page.rect.width+.5 and y1<=page.rect.height+.5, f'Text outside page {i+1}: {span["text"]}'
print(f'PDF audit passed: {len(pdf)} pages, {len(pdf.get_toc())} bookmarks; source hash, searchable text, internal links and page bounds verified.')

pdf.close()
