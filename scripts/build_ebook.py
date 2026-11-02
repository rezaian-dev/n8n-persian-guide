"""Build a reflowable EPUB 3 and a selectable online reader from guide.md.
Uses the existing Markdown dependency and Python's standard library only.
"""
from pathlib import Path
from html import escape
import re, json, hashlib, zipfile
import xml.etree.ElementTree as ET
import markdown

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'guide.md').read_text()
notes = json.loads((ROOT / 'scripts/book-notes.json').read_text())
parts = re.split(r'(?m)^## (.+)$', source)
fa = lambda value: str(value).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
figures = {4: 'flow', 7: 'webhook', 10: 'idempotency', 13: 'infrastructure', 20: 'rag', 21: 'human'}
chapters = []
for index in range(1, len(parts), 2):
    number = (index + 1) // 2
    title = parts[index]
    body = markdown.markdown(parts[index + 1], extensions=['tables', 'fenced_code', 'sane_lists'], output_format='xhtml')
    body = re.sub(r'<ol start="([^"]+)">', lambda match: f'<ol start="{int(match[1])}">', body)
    subnumber = [0]
    def anchor(match):
        subnumber[0] += 1
        return f'<h{match[1]} id="chapter-{number}-section-{subnumber[0]}">{match[2]}</h{match[1]}>'
    body = re.sub(r'<h([34])>(.*?)</h\1>', anchor, body)
    if number in figures:
        image = figures[number]
        figure = f'<figure><img src="../figures/{image}.png" alt="نمودار مفهومی فصل {fa(number)}" /><figcaption>تصویر مفهومی · فصل {fa(number)}</figcaption></figure>'
        position = body.find('</p>') + 4
        body = body[:position] + figure + body[position:]
    if number <= 26:
        note = notes[number - 1]
        goals = ''.join(f'<li>{escape(goal)}</li>' for goal in note['goals'])
        body = f'<aside class="learning-panel"><h3>هدف‌های یادگیری</h3><ul>{goals}</ul></aside>' + body
        body += f'<aside class="practice-panel"><h3>تمرین و کنترل</h3><p>{escape(note["task"])}</p><p><strong>معیار پذیرش:</strong> {escape(note["check"])}</p></aside>'
    chapters.append({'number': number, 'title': title, 'body': body})

# EPUB content uses an independent, intentionally conservative reflowable style.
epub_css = '''@font-face{font-family:Vazirmatn;src:url('font.woff2')}body{font-family:Vazirmatn,sans-serif;line-height:1.9;margin:5%;color:#23394b;background:#fff}h1,h2,h3,h4{line-height:1.7;color:#155c68;page-break-after:avoid}h1{font-size:1.7em}h2{font-size:1.4em}h3{font-size:1.15em}h4{font-size:1.05em}p{orphans:3;widows:3}a{color:#146e79}pre{text-align:left;white-space:pre-wrap;overflow-wrap:anywhere;background:#edf3f5;padding:1em;border-radius:.3em;font-size:.8em;line-height:1.7}code{font-family:monospace}p code,li code,td code{font-size:.88em}table{width:100%;border-collapse:collapse;font-size:.85em}td,th{border:1px solid #bdd4d9;padding:.5em;text-align:right;overflow-wrap:anywhere}img{max-width:100%;height:auto}figure{margin:1.5em 0;text-align:center}figcaption{font-size:.8em;color:#526c7a}blockquote,.learning-panel,.practice-panel{border-right:3px solid #4e9695;background:#f1f8f5;padding:.6em 1em;margin:1.5em 0}.practice-panel{background:#fdf7e9;border-color:#b59450}.learning-panel h3,.practice-panel h3{margin:.2em 0}.cover{text-align:center}.cover img{max-height:95vh}.rights{font-size:.85em;color:#536b78}'''
XHTML = 'http://www.w3.org/1999/xhtml'
EPUB = 'http://www.idpf.org/2007/ops'
OPF = 'http://www.idpf.org/2007/opf'
DC = 'http://purl.org/dc/elements/1.1/'
ET.register_namespace('', XHTML)
ET.register_namespace('epub', EPUB)
def xhtml(title, body):
    tree = ET.fromstring(f'<html xmlns="{XHTML}" xmlns:epub="{EPUB}" lang="fa" xml:lang="fa" dir="rtl"><head><meta charset="utf-8" /><title>{escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css" /></head><body>{body}</body></html>')
    for element in tree.iter():
        if element.tag in {f'{{{XHTML}}}pre', f'{{{XHTML}}}code'}:
            element.set('dir', 'ltr')
    return ET.tostring(tree, encoding='utf-8', xml_declaration=True)

entries = {}
entries['EPUB/style.css'] = epub_css.encode()
entries['EPUB/font.woff2'] = (ROOT / 'docs/assets/Vazirmatn.woff2').read_bytes()
entries['EPUB/font-license.txt'] = (ROOT / 'docs/assets/FONT-LICENSE.txt').read_bytes()
entries['EPUB/cover.png'] = (ROOT / 'docs/previews/cover.png').read_bytes()
entries['EPUB/cover.xhtml'] = xhtml('جلد مرجع فارسی n8n', '<section class="cover" epub:type="cover"><h1>مرجع جامع و پروژه‌محور n8n</h1><img src="cover.png" alt="جلد کتاب؛ نویسنده و گردآورنده محمدرضا رضائیان" /></section>')
entries['EPUB/rights.xhtml'] = xhtml('دربارهٔ این نسخه', '<section><h1>دربارهٔ این نسخه</h1><p>نویسنده و گردآورنده: محمدرضا رضائیان</p><p>این نسخهٔ EPUB متنی و بازچینش‌پذیر است؛ صفحه‌آرایی ثابت و شمارهٔ صفحهٔ PDF را بازسازی نمی‌کند. فهرست و فصل‌ها مستقیماً از منبع کتاب ساخته شده‌اند.</p><p>مبنای مثال‌ها n8n 2.45.7 و تاریخ بررسی منابع ۱ نوامبر ۲۰۲۶ است؛ نه تضمین تازه‌ترین نسخه در آینده.</p><p>منطق نمونه‌ها با تست‌های مستقل بررسی شده است؛ اجرای واقعی n8n، Docker، مدل و سرویس‌های خارجی باید در محیط مقصد آزموده شود.</p><p>تهیه‌شده با کمک ابزارهای پژوهش و نگارش هوش مصنوعی. راهنمای مستقل است و وابسته یا مورد تأیید n8n نیست.</p><p class="rights">© ۲۰۲۶ محمدرضا رضائیان. همهٔ حقوق متن، طرح و عکس محفوظ است. فونت Vazirmatn با مجوز SIL OFL استفاده شده است.</p><p><a href="https://github.com/rezaian-dev/n8n-persian-guide">مخزن، مثال‌ها و منابع</a></p></section>')
nav_rows = ['<li><a href="cover.xhtml">جلد</a></li>', '<li><a href="rights.xhtml">دربارهٔ این نسخه</a></li>']
for chapter in chapters:
    n = chapter['number']
    body = chapter['body'].replace('../figures/', 'figures/')
    entries[f'EPUB/chapter-{n}.xhtml'] = xhtml(chapter['title'], f'<section id="chapter-{n}" epub:type="chapter"><h1>{escape(chapter["title"])}</h1>{body}</section>')
    nav_rows.append(f'<li><a href="chapter-{n}.xhtml#chapter-{n}">{escape(chapter["title"])}</a></li>')
for name in figures.values():
    entries[f'EPUB/figures/{name}.png'] = (ROOT / f'docs/figures/{name}.png').read_bytes()
entries['EPUB/nav.xhtml'] = xhtml('فهرست مطالب', f'<nav epub:type="toc" id="toc"><h1>فهرست مطالب</h1><ol>{"".join(nav_rows)}</ol></nav>')

package = ET.Element(f'{{{OPF}}}package', {'version': '3.0', 'unique-identifier': 'book-id', 'xml:lang': 'fa'})
metadata = ET.SubElement(package, f'{{{OPF}}}metadata')
for tag, text, attrs in [('identifier', 'urn:uuid:50549cd1-6c90-4f62-a1fa-175b69e0c156', {'id': 'book-id'}), ('title', 'مرجع جامع و پروژه‌محور n8n', {}), ('language', 'fa', {}), ('creator', 'محمدرضا رضائیان', {'id': 'author'}), ('rights', '© 2026 Mohammadreza Rezaian. All rights reserved.', {})]:
    ET.SubElement(metadata, f'{{{DC}}}{tag}', attrs).text = text
ET.SubElement(metadata, f'{{{DC}}}source').text = 'urn:sha256:' + hashlib.sha256(source.encode()).hexdigest()
ET.SubElement(metadata, f'{{{OPF}}}meta', {'property': 'dcterms:modified'}).text = '2026-11-02T00:00:00Z'
ET.SubElement(metadata, f'{{{OPF}}}meta', {'property': 'rendition:layout'}).text = 'reflowable'
manifest = ET.SubElement(package, f'{{{OPF}}}manifest')
ids = {}
for i, path in enumerate(entries, 1):
    href = path.removeprefix('EPUB/')
    item_id = f'item-{i}'
    ids[href] = item_id
    media = {'.css': 'text/css', '.woff2': 'font/woff2', '.txt': 'text/plain', '.png': 'image/png', '.xhtml': 'application/xhtml+xml'}[Path(path).suffix]
    attrs = {'id': item_id, 'href': href, 'media-type': media}
    if href == 'nav.xhtml': attrs['properties'] = 'nav'
    if href == 'cover.png': attrs['properties'] = 'cover-image'
    ET.SubElement(manifest, f'{{{OPF}}}item', attrs)
spine = ET.SubElement(package, f'{{{OPF}}}spine', {'page-progression-direction': 'rtl'})
for href in ['cover.xhtml', 'rights.xhtml', 'nav.xhtml'] + [f'chapter-{c["number"]}.xhtml' for c in chapters]:
    ET.SubElement(spine, f'{{{OPF}}}itemref', {'idref': ids[href]})
entries['EPUB/package.opf'] = ET.tostring(package, encoding='utf-8', xml_declaration=True)
container = b'''<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'''
output = ROOT / 'docs/N8N-Persian-Guide.epub'
with zipfile.ZipFile(output, 'w') as archive:
    def put(name, data, compressed=True):
        info = zipfile.ZipInfo(name, date_time=(2026, 11, 2, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
        archive.writestr(info, data)
    put('mimetype', b'application/epub+zip', False)
    put('META-INF/container.xml', container)
    for name, data in entries.items(): put(name, data)

# Overflow containers are static so tables remain usable even with JavaScript disabled.
for chapter in chapters:
    chapter['body'] = chapter['body'].replace('<table>', '<div class="table-scroll" role="region" aria-label="جدول؛ برای دیدن ستون‌ها پیمایش کنید" tabindex="0"><table>').replace('</table>', '</table></div>')

# One HTML reader, not a duplicate set of rasterized book pages.
nav = ''.join(f'<li><a href="#chapter-{c["number"]}">{escape(c["title"])}</a></li>' for c in chapters)
content = ''.join(f'<section class="reader-chapter" id="chapter-{c["number"]}" aria-labelledby="title-{c["number"]}"><div class="chapter-label">{("فصل "+fa(c["number"])) if c["number"]<=26 else "پیوست و منابع"}</div><h2 id="title-{c["number"]}">{escape(c["title"])}</h2>{c["body"]}</section>' for c in chapters)
html = f'''<!doctype html><html lang="fa" dir="rtl" data-theme="light"><head><meta charset="utf-8"><meta name="source-sha256" content="{hashlib.sha256(source.encode()).hexdigest()}"><meta name="viewport" content="width=device-width,initial-scale=1"><title>مطالعهٔ آنلاین مرجع n8n — محمدرضا رضائیان</title><meta name="description" content="متن کامل فارسی کتاب n8n؛ مطالعهٔ آنلاین، جست‌وجوی متن، تغییر اندازهٔ قلم و دسترسی به ۲۶ فصل و پیوست‌ها."><link rel="canonical" href="https://rezaian-dev.github.io/n8n-persian-guide/book/"><link rel="icon" href="../assets/icon.svg"><link rel="stylesheet" href="../assets/reader.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('n8n-reader-theme')||'light';const s=Number(localStorage.getItem('n8n-reader-size'));if(s>=14&&s<=24)document.documentElement.style.setProperty('--reading-size',s+'px')}}catch{{}}</script></head><body><a class="reader-skip" href="#reader-content">رفتن به متن کتاب</a><div id="reader-progress" aria-hidden="true"></div><header class="reader-header"><a class="reader-brand" href="../"><b dir="ltr">n8n /</b><span>کتابخانهٔ فارسی</span></a><nav aria-label="قالب‌های کتاب"><a href="../N8N-Persian-Guide.pdf">PDF</a><a href="../N8N-Persian-Guide.epub" download>EPUB</a><a href="../">معرفی کتاب</a></nav><button id="reader-theme" type="button" hidden>تم تیره</button></header><div class="reader-layout"><aside class="reader-sidebar"><details id="reader-toc" open><summary>فهرست فصل‌ها <span>۲۶ فصل + پیوست‌ها</span></summary><nav aria-label="فهرست کتاب"><ol>{nav}</ol></nav></details></aside><main id="reader-content"><div class="reader-intro"><p class="reader-eyebrow">مطالعهٔ آنلاین · متن کامل و قابل انتخاب</p><h1>مرجع جامع و پروژه‌محور <bdi>n8n</bdi></h1><p>نویسنده و گردآورنده: <strong>محمدرضا رضائیان</strong></p><p class="reader-note">این نسخه متن بازچینش‌پذیر کتاب است، نه تصویر صفحات PDF. برای صفحه‌آرایی چاپی، PDF و برای کتاب‌خوان، EPUB را انتخاب کنید.</p><a id="reader-resume" hidden href="#chapter-1">ادامه از آخرین فصل ←</a></div><div class="reader-tools" hidden><div class="reader-font"><span>اندازهٔ متن</span><button id="font-less" type="button" aria-label="کوچک‌تر کردن متن">−</button><output id="font-value">۱۸</output><button id="font-more" type="button" aria-label="بزرگ‌تر کردن متن">+</button></div><form id="reader-search-form" role="search"><label for="reader-search">جست‌وجو در کتاب</label><div class="reader-search-row"><input id="reader-search" type="search" placeholder="مثلاً Webhook یا امنیت" autocomplete="off" minlength="2"><button type="submit">جست‌وجو</button></div></form><div class="reader-search-status"><span id="search-status" role="status" aria-live="polite"></span><button id="match-prev" type="button" aria-label="نتیجهٔ قبلی" hidden>↑</button><button id="match-next" type="button" aria-label="نتیجهٔ بعدی" hidden>↓</button><button id="search-clear" type="button" hidden>پاک‌کردن</button></div></div>{content}<footer class="reader-footer"><p>© ۲۰۲۶ محمدرضا رضائیان · همهٔ حقوق محفوظ است.</p><a href="../">بازگشت به معرفی کتاب</a><a href="https://github.com/rezaian-dev/n8n-persian-guide">مخزن و فایل‌های همراه ↗</a></footer></main></div><script src="../assets/reader.js" defer></script></body></html>'''
reader = ROOT / 'docs/book/index.html'
reader.parent.mkdir(exist_ok=True)
reader.write_text(html)
print(f'Built EPUB 3: {output.stat().st_size:,} bytes; reader: {len(chapters)} sections, selectable text.')
