"""Typeset the Persian guide as a searchable, bookmarked A4 PDF.
Install requirements.txt before running this script.
"""
from pathlib import Path
import re, json, hashlib
import markdown
from weasyprint import HTML
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'guide.md').read_text()
content=markdown.markdown(source,extensions=['tables','fenced_code','sane_lists'])
content=content[content.index('<h2>'):]
from html import escape, unescape
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
notes=json.loads((ROOT/'scripts/book-notes.json').read_text())
headings=[]
parts=re.split(r'<h2>(.*?)</h2>',content)
figures={4:('flow','مدل مفهومی یک گردش‌کار قابل‌ردیابی'),7:('webhook','قرارداد ورودی و دو مسیر جایگزین پاسخ'),10:('idempotency','طرح مفهومی جلوگیری از اثر تکراری'),13:('infrastructure','مرزهای زیرساخت در مبنای staging'),20:('rag','بازیابی زمینه با کنترل دسترسی'),21:('human','اجرای ابزار پرریسک با تأیید انسان')}
groups=[(5,'بخش یک · مبانی و مدل ذهنی'),(9,'بخش دو · از ورودی تا API'),(12,'بخش سه · اعتمادپذیری'),(18,'بخش چهار · استقرار و عملیات'),(22,'بخش پنج · هوش مصنوعی کنترل‌شده'),(26,'بخش شش · تست و انتشار')]
chapters=[]
for i in range(1,len(parts),2):
    number=(i+1)//2;title=parts[i];body=parts[i+1];key=f'chapter-{number}'
    headings.append((key,title))
    clean=re.sub(r'^[۰-۹0-9]+[.\s]+','',title)
    if number<=26:
        note=notes[number-1]
        group=next(label for limit,label in groups if number<=limit)
        goals=''.join('<li>'+escape(g)+'</li>' for g in note['goals'])
        density=" dense" if number in [4,13,19,20,21] else ""
        opening=f'<section class="page-chapter{density}"><div class="chapter-kicker"><b>{number:02d}</b><span>{group}</span></div><h2 class="chapter" id="{key}">{clean}</h2><div class="objectives"><strong>هدف‌های یادگیری این فصل</strong><ul>{goals}</ul></div>'
        if number in figures:
            name,caption=figures[number]
            figure=f'<figure class="technical-figure"><img src="docs/figures/{name}.png" alt="{caption}"><figcaption>تصویر {number} · {caption}</figcaption></figure>'
            # Keep the figure near the opening, before the next major content block.
            position=body.find('</p>')+4
            body=body[:position]+figure+body[position:]
        ending=f'<div class="exercise"><div class="exercise-label">تمرین و کنترل</div><p>{escape(note["task"])}</p><p class="acceptance"><b>معیار پذیرش:</b> {escape(note["check"])}</p></div></section>'
    else:
        opening=f'<section class="reference-page"><h2 class="chapter" id="{key}">{clean}</h2>'
        ending='</section>'
    chapters.append(opening+body+ending)
content=''.join(chapters)
formatter=HtmlFormatter(nowrap=True,style='one-dark')
def code_frame(match):
    language=match.group(1) or 'text'
    try:lexer=get_lexer_by_name(language)
    except Exception:lexer=TextLexer()
    colored=highlight(unescape(match.group(2)),lexer,formatter)
    label=escape(language.upper())
    return f'<div class="code-window"><div class="code-toolbar"><span class="traffic"><i></i><i></i><i></i></span><b>{label} / EXAMPLE</b><small>نمونهٔ آموزشی</small></div><pre>{colored}</pre></div>'
content=re.sub(r'<pre><code(?: class="language-([^" ]+)")?>(.*?)</code></pre>',code_frame,content,flags=re.S)
fa=lambda value:str(value).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
toc_groups=[('01','مبانی و مدل ذهنی','پیش از ساختن، مسئله و داده را بشناسید.',1,5),('02','اولین گردش‌کار','از یک ورودی ساده تا اتصال API.',6,9),('03','اعتمادپذیری','تکرار، خطا و اثر جانبی را کنترل کنید.',10,12),('04','استقرار و عملیات','از محیط محلی تا زیرساخت قابل‌بازیابی.',13,18),('05','هوش مصنوعی کنترل‌شده','مدل، بازیابی سند و اختیار انسان.',19,22),('06','آزمون و انتشار','کیفیت را با شواهد نشان دهید.',23,26)]
toc_pages=[]
for page_index in range(2):
    cards=[]
    for group_number,group_title,summary,start,end in toc_groups[page_index*3:page_index*3+3]:
        rows=[]
        for n in range(start,end+1):
            key,title=headings[n-1]
            clean=re.sub(r'^[۰-۹0-9]+[.\s]+','',title)
            rows.append(f'<a class="toc-row" href="#{key}"><span class="toc-index">{fa(f"{n:02d}")}</span><span class="toc-title">{clean}</span></a>')
        cards.append(f'<div class="toc-group"><div class="toc-group-heading"><b>{fa(group_number)}</b><div><h2>{group_title}</h2><p>{summary}</p></div></div><div class="toc-rows">'+''.join(rows)+'</div></div>')
    extras=''
    if page_index==1:
        extras='<div class="toc-extras">'+''.join(f'<a href="#{key}">{title}</a>' for key,title in headings[26:])+'</div>'
    continuation=' / ادامه' if page_index else ''
    toc_pages.append(f'<section class="contents"><div class="toc-top"><p class="overline">THE READING MAP / {page_index+1:02d}</p><span>۲۶ فصل · ۶ مسیر یادگیری</span></div><h1>فهرست مطالب{continuation}</h1><p class="toc-intro">یک مسیر روشن، از فهم مسئله تا ساختن یک سیستم قابل‌اعتماد.</p>'+''.join(cards)+extras+'</section>')
toc=''.join(toc_pages)
css=(ROOT/'scripts/book.css').read_text()+'\n'+formatter.get_style_defs('.code-window')
html='''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>راهنمای جامع و کاربردی n8n — محمدرضا رضائیان</title>
<meta name="author" content="Mohammadreza Rezaian — محمدرضا رضائیان">
<meta name="description" content="راهنمای فارسی n8n؛ اتوماسیون قابل‌اعتماد، API، استقرار امن و هوش مصنوعی کنترل‌شده.">
<style>'''+css+'''</style></head><body>
<section class="cover">
 <div class="cover-code" dir="ltr">const workflow = {<br>  event: 'received',<br>  validate: true,<br>  retry: 'bounded',<br>  humanReview: 'required'<br>};<br>// Build small. Build reliable.</div>
 <p class="cover-overline">P E R S I A N   E N G I N E E R I N G   G U I D E</p>
 <div class="cover-logo" dir="ltr">n8n</div>
 <p class="cover-kicker">راهنمای جامع و کاربردی</p>
 <h1>اتوماسیون،<br><em>همان‌طور که باید.</em></h1>
 <p class="cover-subtitle">از مدل ذهنی تا ساختن سیستم‌های قابل‌اعتماد</p>
 <p class="cover-desc">داده و API · مدیریت خطا و تکرار · استقرار امن<br>هوش مصنوعی کنترل‌شده، همراه با مثال و تمرین</p>
 <div class="cover-tags"><span>۲۶ فصل کاربردی</span><span>۶ تصویر مفهومی</span><span>مثال و تمرین</span><span>منابع رسمی</span></div>
 <div class="cover-author"><img src="docs/assets/author.webp" alt="محمدرضا رضائیان"><div><strong>محمدرضا رضائیان</strong><small>نویسنده و گردآورنده · برای جامعهٔ توسعه‌دهندگان فارسی‌زبان</small></div></div>
 <div class="cover-bottom"><span>n8n 2.45.7 · PostgreSQL · API · AI</span><span>ویرایش اول / نوامبر ۲۰۲۶</span></div>
</section>
<section class="imprint">
 <p class="overline">BEFORE YOU START</p><h1>پیش از شروع</h1>
 <p class="large">یک گردش‌کار خوب فقط در روزهای خوب کار نمی‌کند؛ در روزهای سخت هم قابل‌فهم و قابل‌بازیابی است.</p>
 <p>این راهنما برای توسعه‌دهندگان و سازندگان محصول نوشته شده است. مسیر مطالعه از داده و Webhook آغاز می‌شود و به طراحی قابل‌اعتماد، استقرار، امنیت و استفادهٔ کنترل‌شده از هوش مصنوعی می‌رسد.</p>
 <div class="edition"><p><b>نویسنده و گردآورنده:</b> محمدرضا رضائیان</p><p><b>ویرایش:</b> اول — ۱ نوامبر ۲۰۲۶</p><p><b>مبنای مثال‌ها:</b> n8n 2.45.7، نه تضمین تازه‌ترین نسخه در آینده.</p><p><b>مخزن و فایل‌های همراه:</b><br><a class="ltr" href="https://github.com/rezaian-dev/n8n-persian-guide">github.com/rezaian-dev/n8n-persian-guide</a></p></div>
 <h2>حدود آزمون و مسئولیت</h2><p>منطق اعتبارسنجی و ساختار نمونه با تست‌های مستقل بررسی شده‌اند. اجرای کامل در n8n، Docker، سرویس خارجی و فرایند بازیابی باید در محیط مقصد آزمایش شوند. مثال‌ها مبنای آموزش و staging هستند و تضمین آماده‌بودن برای Production ندارند.</p>
 <p>این اثر با کمک ابزارهای پژوهش و نگارش هوش مصنوعی تهیه شده است. تاریخ بررسی منابع و حدود آزمون شفاف‌اند. این راهنما محصول رسمی یا مورد تأیید n8n نیست. نام‌ها و علائم تجاری متعلق به صاحبانشان‌اند.</p>
 <p class="small">© ۲۰۲۶ محمدرضا رضائیان. همهٔ حقوق محفوظ است. عکس نویسنده با اجازهٔ صاحب حساب استفاده شده است. فونت Vazirmatn با مجوز SIL OFL به‌کار رفته است. مجوز n8n مستقل از این مقاله است.</p>
</section>
'''+toc+'''
<main>'''+content+'''</main>
<section class="back-cover"><p class="overline">BUILD SMALL. BUILD RELIABLE.</p><h1>یک فرایند کوچک.<br>یک اثر واقعی.</h1><p>فایل گردش‌کار، مثال‌های کد و راهنمای استقرار را از مخزن دریافت کنید. برای گزارش خطا، شمارهٔ بخش و نسخهٔ نرم‌افزار را همراه با نمونهٔ پاک‌سازی‌شده ارسال کنید.</p><a class="ltr" href="https://github.com/rezaian-dev/n8n-persian-guide">github.com/rezaian-dev/n8n-persian-guide</a><div class="back-author"><img src="docs/assets/author.webp" alt="محمدرضا رضائیان"><h2>محمدرضا رضائیان</h2><p>React · Next.js · TypeScript</p><a href="https://rezaian-dev.vercel.app/fa">rezaian-dev.vercel.app</a></div></section>
</body></html>'''
output=ROOT/'docs/N8N-Persian-Guide.pdf'
HTML(string=html,base_url=str(ROOT)).write_pdf(output,presentational_hints=True)
print(f'Built {output.name}: {output.stat().st_size:,} bytes')

# Render real PDF previews and save metadata for the static landing page.
import fitz
pdf=fitz.open(output)
previews=ROOT/'docs/previews'
previews.mkdir(exist_ok=True)
destinations={link.get('nameddest'):link.get('page') for page in pdf for link in page.get_links() if link.get('nameddest')}
samples=[0,2,destinations['chapter-13']]
for index,name in zip(samples,['cover','sample-01','sample-02']):
    pdf[index].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(previews/f'{name}.png')
layout_files=['scripts/build_pdf.py','scripts/book.css','scripts/book-notes.json','scripts/build_figures.py']
layout_hash=hashlib.sha256(b''.join((ROOT/f).read_bytes() for f in layout_files)).hexdigest()
meta={'pages':len(pdf),'bytes':output.stat().st_size,'edition':'2026-11-01','sample_pages':[x+1 for x in samples],'source_sha256':hashlib.sha256((ROOT/'guide.md').read_bytes()).hexdigest(),'layout_sha256':layout_hash,'chapter_pages':[destinations[f'chapter-{n}']+1 for n in range(1,29)],'illustrations':6,'motion_version':'14.9.0'}
(ROOT/'docs/assets/book-meta.json').write_text(json.dumps(meta,indent=2)+'\n')
print(f'PDF: {len(pdf)} pages, {len(pdf.get_toc())} bookmarks, previews generated.')
