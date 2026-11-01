"""Audit the distributed PDF. Requires PyMuPDF; does not claim semantic proofreading."""
from pathlib import Path
import json, hashlib, re
import fitz
ROOT=Path(__file__).resolve().parents[1]
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
