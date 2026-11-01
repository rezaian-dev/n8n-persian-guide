"""Typeset the Persian guide as a searchable, bookmarked A4 PDF.
Install requirements-pdf.txt before running this script.
"""
from pathlib import Path
import re, json, hashlib
import markdown
from weasyprint import HTML
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'guide.md').read_text()
content=markdown.markdown(source,extensions=['tables','fenced_code','sane_lists'])
content=content[content.index('<h2>'):]
headings=[]
def section(match):
 title=match.group(1);index=len(headings)+1;key=f'chapter-{index}'
 headings.append((key,title))
 group=' part-start' if index in [1,6,10,13,19,23,27] else ''
 return f'<h2 class="chapter{group}" id="{key}">{title}</h2>'
content=re.sub(r'<h2>(.*?)</h2>',section,content)
toc=''.join(f'<li><a href="#{key}">{title}</a></li>' for key,title in headings)
css=(ROOT/'scripts/book.css').read_text()
html='''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>راهنمای جامع و کاربردی n8n — محمدرضا رضائیان</title>
<meta name="author" content="Mohammadreza Rezaian — محمدرضا رضائیان">
<meta name="description" content="راهنمای فارسی n8n؛ اتوماسیون قابل‌اعتماد، API، استقرار امن و هوش مصنوعی کنترل‌شده.">
<style>'''+css+'''</style></head><body>
<section class="cover">
 <div class="cover-top"><span>ENGINEERING NOTES / 01</span><b>راهنمای فارسی</b></div>
 <div class="cover-rule"></div>
 <p class="cover-kicker">راهنمای جامع و کاربردی</p>
 <h1 dir="ltr">n8n<span>.</span></h1>
 <h2>از اتصال ابزارها<br>تا ساختن سیستم‌های<br><em>قابل‌اعتماد.</em></h2>
 <p class="cover-desc">اتوماسیون، API، استقرار امن و هوش مصنوعی کنترل‌شده<br>همراه با مثال عملی، کد و منابع رسمی</p>
 <div class="cover-tags"><span>WORKFLOWS</span><span>SECURITY</span><span>AI + RAG</span></div>
 <div class="cover-author"><img src="docs/assets/author.webp" alt="محمدرضا رضائیان"><div><small>نویسنده و گردآورنده</small><strong>محمدرضا رضائیان</strong><p dir="ltr">Front-End Engineer</p></div></div>
 <div class="cover-bottom"><span>۲۶ بخش کاربردی · ویرایش اول</span><span>نوامبر ۲۰۲۶</span></div>
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
<section class="contents"><p class="overline">READING MAP</p><h1>فهرست مطالب</h1><p class="muted">از مسیر کوتاه شروع کنید؛ هر بخش یک مسئلهٔ واقعی را باز می‌کند.</p><ol>'''+toc+'''</ol></section>
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
for index, name in [(0, 'cover'), (9, 'sample-01'), (15, 'sample-02')]:
    pdf[index].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(previews/f'{name}.png')
meta={'pages':len(pdf),'bytes':output.stat().st_size,'edition':'2026-11-01','sample_pages':[1,10,16],'source_sha256':hashlib.sha256((ROOT/'guide.md').read_bytes()).hexdigest()}
(ROOT/'docs/assets/book-meta.json').write_text(json.dumps(meta,indent=2)+'\n')
print(f'PDF: {len(pdf)} pages, {len(pdf.get_toc())} bookmarks, previews generated.')
