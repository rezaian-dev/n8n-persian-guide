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
icons=json.loads((ROOT/'scripts/icons.json').read_text())
chapter_icons=['book','workflow','compare','layers','data','terminal','webhook','filter','api','fingerprint','retry','branch','server','globe','shield','queue','chart','restore','brain','search','approval','support','check','bug','route','rocket']
def icon(name, color='#167e83'):
    return f'<svg class="book-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icons[name]}</svg>'

headings=[]
subheadings={}
fa=lambda value:str(value).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
parts=re.split(r'<h2>(.*?)</h2>',content)
figures={4:('flow','مدل مفهومی یک گردش‌کار قابل‌ردیابی'),7:('webhook','قرارداد ورودی و دو مسیر جایگزین پاسخ'),10:('idempotency','طرح مفهومی جلوگیری از اثر تکراری'),13:('infrastructure','مرزهای زیرساخت در مبنای staging'),20:('rag','بازیابی زمینه با کنترل دسترسی'),21:('human','اجرای ابزار پرریسک با تأیید انسان')}
groups=[(5,'بخش یک · مبانی و مدل ذهنی'),(9,'بخش دو · از ورودی تا API'),(12,'بخش سه · اعتمادپذیری'),(18,'بخش چهار · استقرار و عملیات'),(22,'بخش پنج · هوش مصنوعی کنترل‌شده'),(26,'بخش شش · تست و انتشار')]
chapters=[]
for i in range(1,len(parts),2):
    number=(i+1)//2;title=parts[i];body=parts[i+1];key=f'chapter-{number}'
    headings.append((key,title))
    subheadings[number]=[]
    def anchor_subheading(match):
        index=len(subheadings[number])+1
        anchor=f'{key}-section-{index}'
        label=match.group(1)
        subheadings[number].append((anchor,label,index))
        prefix=f'<span class="sub-number">{fa(number)}.{fa(index)}</span> ' if number<=26 else ''
        return f'<h3 id="{anchor}">{prefix}{label}</h3>'
    body=re.sub(r'<h3>(.*?)</h3>',anchor_subheading,body)
    body=re.sub(r'(<h4>.*?</h4>)\s*(<p>.*?</p>)',lambda m:'<div class="interview-card"><div class="question-title"><span class="icon-slot">'+icon('message')+'</span>'+m.group(1)+'</div>'+m.group(2)+'</div>',body,flags=re.S)
    clean=re.sub(r'^[۰-۹0-9]+[.\s]+','',title)
    if number<=26:
        note=notes[number-1]
        group=next(label for limit,label in groups if number<=limit)
        goals=''.join('<li>'+escape(g)+'</li>' for g in note['goals'])
        density=" flow-fit" if number in [3,4,5,6,9,13,20,21,23] else ""
        opening=f'<section class="page-chapter{density}"><div class="chapter-kicker"><div class="chapter-icon-cell"><div class="chapter-icon-frame">{icon(chapter_icons[number-1])}</div></div><div class="chapter-meta"><span>{group}</span><b>فصل {fa(number)}</b></div></div><h2 class="chapter" id="{key}">{clean}</h2><div class="objectives"><div class="panel-title"><span class="icon-slot">{icon("target")}</span><strong>هدف‌های یادگیری این فصل</strong></div><ul>{goals}</ul></div>'
        if number in figures:
            name,caption=figures[number]
            figure=f'<figure class="technical-figure"><img src="docs/figures/{name}.png" alt="{caption}"><figcaption>تصویر {number} · {caption}</figcaption></figure>'
            # Keep the figure near the opening, before the next major content block.
            position=body.find('</p>')+4
            body=body[:position]+figure+body[position:]
        ending=f'<div class="exercise"><div class="exercise-label"><div class="panel-title"><span class="icon-slot">{icon("experiment")}</span><strong>تمرین و کنترل</strong></div></div><p>{escape(note["task"])}</p><p class="acceptance"><b>معیار پذیرش:</b> {escape(note["check"])}</p></div></section>'
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
for page_index in range(3):
    cards=[]
    for group_number,group_title,summary,start,end in toc_groups[page_index*2:page_index*2+2]:
        rows=[]
        for n in range(start,end+1):
            key,title=headings[n-1]
            clean=re.sub(r'^[۰-۹0-9]+[.\s]+','',title)
            rows.append(f'<a class="toc-entry" href="#{key}"><span>{fa(n)}. {clean}</span></a>')
        cards.append(f'<div class="contents-group"><h2>{group_title}</h2>'+''.join(rows)+'</div>')
    if page_index==2:
        cards.append('<div class="contents-group"><h2>پیوست و منابع</h2>'+''.join(f'<a class="toc-entry" href="#{key}"><span>{title}</span></a>' for key,title in headings[26:])+'</div>')
    toc_pages.append(f'<section class="contents" id="contents-{page_index+1}"><h1>فهرست مطالب</h1>'+''.join(cards)+'</section>')
toc=''.join(toc_pages)
css=(ROOT/'scripts/book.css').read_text()+'\n'+formatter.get_style_defs('.code-window')
html='''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>مرجع جامع و پروژه‌محور n8n — محمدرضا رضائیان</title>
<meta name="author" content="Mohammadreza Rezaian — محمدرضا رضائیان">
<meta name="description" content="راهنمای فارسی n8n؛ اتوماسیون قابل‌اعتماد، API، استقرار امن و هوش مصنوعی کنترل‌شده.">
<style>'''+css+'''</style></head><body><div class="running-header"><span>مرجع فارسی اتوماسیون</span><b dir="ltr">n8n</b></div>
<section class="cover">
 <p class="cover-overline">THE PROJECT-BASED PERSIAN REFERENCE</p>
 <div class="cover-logo" dir="ltr">n8n.</div>
 <p class="cover-kicker">مرجع جامع و پروژه‌محور</p>
 <h1>از ایده، تا یک سیستم<br><em>قابل‌اعتماد.</em></h1>
 <p class="cover-subtitle">مدل ذهنی · طراحی · آزمون · بازیابی</p>
 <img class="cover-art" src="docs/assets/cover-art.webp" alt="تصویر مفهومی مسطح از جریان داده و شاخه‌های اتوماسیون">
 <div class="cover-tags"><span>۲۶ فصل عمیق</span><span>۷۶ پرسش تحلیلی</span><span>۳ پروژه و آزمایشگاه</span></div>
 <div class="cover-author"><img src="docs/assets/author.webp" alt="محمدرضا رضائیان"><div><strong>محمدرضا رضائیان</strong><small>نویسنده و گردآورنده · برای جامعهٔ توسعه‌دهندگان فارسی‌زبان</small></div></div>
 <div class="cover-bottom"><span>n8n 2.45.7 · PostgreSQL · API · AI</span><span>ویرایش دوم / نوامبر ۲۰۲۶</span></div>
</section>
<section class="imprint">
 <h1>پیش از شروع</h1>
 <p class="large">یک گردش‌کار خوب فقط در روزهای خوب کار نمی‌کند؛ در روزهای سخت هم قابل‌فهم و قابل‌بازیابی است.</p>
 <p>این راهنما برای توسعه‌دهندگان و سازندگان محصول نوشته شده است. مسیر مطالعه از داده و Webhook آغاز می‌شود و به طراحی قابل‌اعتماد، استقرار، امنیت و استفادهٔ کنترل‌شده از هوش مصنوعی می‌رسد.</p>
 <div class="edition"><p><b>نویسنده و گردآورنده:</b> محمدرضا رضائیان</p><p><b>ویرایش:</b> دوم — ۱ نوامبر ۲۰۲۶</p><p><b>مبنای مثال‌ها:</b> n8n 2.45.7، نه تضمین تازه‌ترین نسخه در آینده.</p><p><b>مخزن و فایل‌های همراه:</b><br><a class="ltr" href="https://github.com/rezaian-dev/n8n-persian-guide">github.com/rezaian-dev/n8n-persian-guide</a></p></div>
 <h2>چگونه با این مرجع کار کنید؟</h2><p>هر فصل را با پیش‌بینی رفتار و ساختن حالت شکست بخوانید. ۵۲ پرسش در فصل‌ها و ۲۴ سناریو در پیوست، تحلیل تصمیم‌ها را تمرین می‌دهند. پروژهٔ n8n و دو آزمایشگاه مستقلِ دریافت پایدار و مرز AI را از مخزن اجرا کنید. خواندن به‌تنهایی تضمین تسلط نیست.</p>
 <h2>حدود آزمون و مسئولیت</h2><p>منطق اعتبارسنجی و ساختار نمونه با تست‌های مستقل بررسی شده‌اند. اجرای کامل در n8n، Docker، سرویس خارجی و فرایند بازیابی باید در محیط مقصد آزمایش شوند. مثال‌ها مبنای آموزش و staging هستند و تضمین آماده‌بودن برای Production ندارند.</p>
 <p>این اثر با کمک ابزارهای پژوهش و نگارش هوش مصنوعی تهیه شده است. تاریخ بررسی منابع و حدود آزمون شفاف‌اند. این راهنما محصول رسمی یا مورد تأیید n8n نیست. نام‌ها و علائم تجاری متعلق به صاحبانشان‌اند.</p>
 <p class="small">© ۲۰۲۶ محمدرضا رضائیان. همهٔ حقوق محفوظ است. عکس نویسنده با اجازهٔ صاحب حساب استفاده شده است. فونت Vazirmatn با مجوز SIL OFL به‌کار رفته است. مجوز n8n مستقل از این مقاله است.</p>
</section>
'''+toc+'''
<main>'''+content+'''</main>
<section class="back-cover"><p class="overline">BUILD SMALL. BUILD RELIABLE.</p><h1>یک فرایند کوچک.<br>یک اثر واقعی.</h1><p>فایل گردش‌کار، مثال‌های کد و راهنمای استقرار را از مخزن دریافت کنید. برای گزارش خطا، شمارهٔ بخش و نسخهٔ نرم‌افزار را همراه با نمونهٔ پاک‌سازی‌شده ارسال کنید.</p><a class="ltr" href="https://github.com/rezaian-dev/n8n-persian-guide">github.com/rezaian-dev/n8n-persian-guide</a><div class="back-author"><img src="docs/assets/author.webp" alt="محمدرضا رضائیان"><h2>محمدرضا رضائیان</h2><p>React · Next.js · TypeScript</p><a href="https://rezaian-dev.vercel.app/fa">rezaian-dev.vercel.app</a></div></section>
</body></html>'''
output=ROOT/'docs/N8N-Persian-Guide.pdf'
document=HTML(string=html,base_url=str(ROOT)).render(presentational_hints=True)
# Geometric preflight: SVGs must occupy their own slots, not a text line.
icon_count=0
icon_collisions=[]
icon_center_errors=[]
icon_slots_checked=0
for page_number,page in enumerate(document.pages,1):
    all_boxes=[]
    parents={}
    def walk(box):
        all_boxes.append(box)
        for child in getattr(box,'children',[]):
            parents[id(child)]=box
            walk(child)
    walk(page._page_box)
    svg_boxes=[box for box in all_boxes if getattr(box,'replacement',None) is not None and getattr(box,'element',None) is not None and 'book-icon' in box.element.get('class','').split()]
    text_boxes=[box for box in all_boxes if type(box).__name__=='TextBox' and getattr(box,'text','').strip()]
    for svg in svg_boxes:
        icon_count+=1
        x,y=svg.content_box_x(),svg.content_box_y()
        parent=parents.get(id(svg))
        while parent is not None:
            element=getattr(parent,'element',None)
            classes=element.get('class','').split() if element is not None else []
            if 'icon-slot' in classes or 'chapter-icon-frame' in classes:
                icon_slots_checked+=1
                assert x>=parent.content_box_x()-.75 and y>=parent.content_box_y()-.75 and x+svg.width<=parent.content_box_x()+parent.width+.75 and y+svg.height<=parent.content_box_y()+parent.height+.75, f'Icon outside slot on page {page_number}'
                cx=parent.content_box_x()+parent.width/2
                cy=parent.content_box_y()+parent.height/2
                dx=abs(x+svg.width/2-cx)
                dy=abs(y+svg.height/2-cy)
                if max(dx,dy)>1:
                    icon_center_errors.append((page_number,round(dx,2),round(dy,2)))
                break
            parent=parents.get(id(parent))
        for text in text_boxes:
            tx,ty=text.content_box_x(),text.content_box_y()
            overlap_x=min(x+svg.width,tx+text.width)-max(x,tx)
            overlap_y=min(y+svg.height,ty+text.height)-max(y,ty)
            if overlap_x>.75 and overlap_y>.75:
                icon_collisions.append((page_number,text.text))
assert icon_count==130, f'Expected 130 placed learning icons, found {icon_count}'
assert icon_slots_checked==icon_count, 'An icon has no dedicated layout slot'
assert not icon_collisions, f'Icon/text overlaps: {icon_collisions}'
assert not icon_center_errors, f'Icon centering errors: {icon_center_errors}'
document.write_pdf(output)
print(f'Icon alignment preflight: {icon_count} vectors, centered in dedicated slots; no text-box overlaps.')
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
layout_files=['scripts/build_pdf.py','scripts/book.css','scripts/book-notes.json','scripts/build_figures.py','docs/assets/cover-art.webp','docs/assets/author.webp','scripts/icons.json']
layout_hash=hashlib.sha256(b''.join((ROOT/f).read_bytes() for f in layout_files)).hexdigest()
meta={'pages':len(pdf),'bytes':output.stat().st_size,'edition':'2026-11-01','sample_pages':[x+1 for x in samples],'source_sha256':hashlib.sha256((ROOT/'guide.md').read_bytes()).hexdigest(),'layout_sha256':layout_hash,'chapter_pages':[destinations[f'chapter-{n}']+1 for n in range(1,len(headings)+1)],'illustrations':6,'chapters':26,'interview_questions':76,'source_words':len(source.split()),'projects':3,'toc_pages':destinations['chapter-1']-2,'icons':len(icons),'chapter_icons':26,'pdf_icons':29,'placed_icons':icon_count,'icon_text_overlaps':len(icon_collisions),'icon_center_errors':len(icon_center_errors),'icon_slots_checked':icon_slots_checked,'motion_version':'14.9.0'}
(ROOT/'docs/assets/book-meta.json').write_text(json.dumps(meta,indent=2)+'\n')
print(f'PDF: {len(pdf)} pages, {len(pdf.get_toc())} bookmarks, previews generated.')
