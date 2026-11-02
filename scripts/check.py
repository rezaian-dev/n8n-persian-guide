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

for filename in ['index.html', 'book/index.html']:
 base=(ROOT/'docs'/filename).parent
 page=Check();page.feed((ROOT/'docs'/filename).read_text())
 for ref in page.refs:
  if ref.startswith('#'):
   if ref!='#':assert ref[1:] in page.ids,f'Missing anchor: {ref}'
  elif not ref.startswith(('https:','http:','mailto:','data:')):
   path,_,fragment=ref.partition('#')
   target=(base/path).resolve()
   if target.is_dir():target=target/'index.html'
   assert target.is_relative_to(ROOT/'docs'), f'Unexpected path outside publication: {ref}'
   assert target.is_file(),f'Missing local asset: {ref}'
   if fragment and target.suffix=='.html':
    other=Check();other.feed(target.read_text());assert fragment in other.ids,ref
 assert page.images>=2
 print(f'{filename}: {len(page.ids)} unique ids, {len(page.refs)} references checked.')
for f in ['guide.md','README.md','LICENSE.md','deploy/.env.example','workflows/lead-intake.json','docs/N8N-Persian-Guide.pdf','docs/N8N-Persian-Guide.epub','docs/book/index.html','docs/assets/reader.css','docs/assets/reader.js','.gitattributes']:
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

# Basic package integrity is checked on every build; EPUBCheck remains an independent check.
import zipfile, posixpath
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, unquote
reader=(ROOT/'docs/book/index.html').read_text()
source_hash=hashlib.sha256((ROOT/'guide.md').read_bytes()).hexdigest()
assert f'name="source-sha256" content="{source_hash}"' in reader, 'Online reader is stale'
assert reader.count('class="reader-chapter"')==29
assert all(f'id="chapter-{n}"' in reader for n in range(1,30))
assert 'canvas' not in reader
assert all(f'id="{name}"' in reader for name in ['reader-toc','reader-search','reader-theme','reader-resume','font-more','font-less'])
ns={'p':'http://www.idpf.org/2007/opf','x':'http://www.w3.org/1999/xhtml','dc':'http://purl.org/dc/elements/1.1/'}
with zipfile.ZipFile(ROOT/'docs/N8N-Persian-Guide.epub') as archive:
 names=set(archive.namelist())
 assert len(names)==len(archive.namelist()), 'Duplicate archive entries'
 first=archive.infolist()[0]
 assert first.filename=='mimetype' and first.compress_type==zipfile.ZIP_STORED
 assert archive.read('mimetype')==b'application/epub+zip'
 assert archive.testzip() is None
 container=ET.fromstring(archive.read('META-INF/container.xml'))
 package_path=container.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile').get('full-path')
 package=ET.fromstring(archive.read(package_path));assert package.get('version')=='3.0'
 assert package.find('p:metadata/dc:language',ns).text=='fa'
 assert package.find('p:metadata/dc:source',ns).text=='urn:sha256:'+source_hash, 'EPUB is stale'
 assert package.find('p:spine',ns).get('page-progression-direction')=='rtl'
 manifest={item.get('id'):item for item in package.findall('p:manifest/p:item',ns)}
 paths={posixpath.normpath('EPUB/'+item.get('href')) for item in manifest.values()}
 assert all(path in names for path in paths)
 assert paths==names-{'mimetype','META-INF/container.xml',package_path}, 'Unmanifested EPUB asset'
 assert len([item for item in manifest.values() if item.get('properties')=='cover-image'])==1
 assert len([item for item in manifest.values() if item.get('properties')=='nav'])==1
 spine=package.findall('p:spine/p:itemref',ns)
 assert len(spine)==32 and all(item.get('idref') in manifest for item in spine)
 documents={path:ET.fromstring(archive.read(path)) for path in paths if path.endswith('.xhtml')}
 for path,document in documents.items():
  assert document.get('dir')=='rtl' and document.get('lang')=='fa'
  assert not document.findall('.//x:script',ns), 'EPUB must not contain scripts'
  ids=[element.get('id') for element in document.iter() if element.get('id')]
  assert len(ids)==len(set(ids)), f'Duplicate XHTML ids: {path}'
  for element in document.iter():
   for key in ['href','src']:
    ref=element.get(key)
    if not ref:continue
    url=urlsplit(ref)
    if url.scheme:continue
    target=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(url.path))) if url.path else path
    assert target in names, f'Missing EPUB resource {path}: {ref}'
    if url.fragment:
     assert any(node.get('id')==unquote(url.fragment) for node in documents[target].iter()), f'Missing EPUB anchor: {ref}'
  if path.startswith('EPUB/chapter-'):
   number=int(Path(path).stem.split('-')[1])
   assert document.find('.//x:h1',ns).text==re.findall(r'^## (.+)$',source,re.M)[number-1]
   assert len(''.join(document.itertext()).strip())>100
 toc=documents['EPUB/nav.xhtml'].find('.//x:nav',ns)
 assert toc.get('{http://www.idpf.org/2007/ops}type')=='toc'
 assert len(toc.findall('.//x:a',ns))==31
 for internal,local in [('font.woff2','assets/Vazirmatn.woff2'),('font-license.txt','assets/FONT-LICENSE.txt'),('cover.png','previews/cover.png')]+[(f'figures/{name}.png',f'figures/{name}.png') for name in ['flow','webhook','idempotency','infrastructure','rag','human']]:
  assert archive.read('EPUB/'+internal)==(ROOT/'docs'/local).read_bytes(), f'Stale EPUB asset: {internal}'
print('Reader and EPUB audit passed: 29 complete sections, source hashes, RTL spine, nav, XHTML, assets and internal links.')
