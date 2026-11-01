"""Render original technical illustrations. Optional build dependency: Playwright Chromium.
Generated PNGs are distributed so readers and CI don't need a browser.
"""
from pathlib import Path
import base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/figures';OUT.mkdir(exist_ok=True)
font='data:font/woff2;base64,'+base64.b64encode((ROOT/'docs/assets/Vazirmatn.woff2').read_bytes()).decode()
CSS=f'''@font-face{{font-family:V;src:url('{font}')}}*{{box-sizing:border-box}}body{{margin:0;font-family:V,sans-serif;direction:rtl;width:1440px;height:660px;background:#f5f7fb;color:#16213a;padding:48px 55px}}.label{{direction:ltr;text-align:right;font:13px monospace;letter-spacing:3px;color:#a36e0b}}h1{{font-size:33px;margin:12px 0 7px}}.subtitle{{font-size:17px;color:#738099;margin:0 0 36px}}.flow{{display:flex;align-items:center;direction:ltr;gap:15px;padding:20px 0}}.node{{flex:1;background:white;border:1px solid #dbe3ee;border-radius:18px;padding:25px 20px;direction:rtl;min-height:155px;box-shadow:0 9px 25px #1d355409}}.node b{{display:block;font-size:23px;margin:13px 0 6px}}.node small{{display:block;font-size:14px;color:#6c7890}}.node .icon{{font:700 25px monospace;color:#b27a11;background:#fff3d4;border-radius:10px;padding:10px;display:inline-block}}.node.accent{{background:#17243f;border-color:#17243f;color:white}}.node.accent small{{color:#b6c5df}}.node.accent .icon{{background:#30415f;color:#ffd68c}}.arrow{{color:#ba8a2b;font-size:27px}}.note{{padding:19px 23px;background:#fff6df;border-right:5px solid #c58b18;border-radius:8px;font-size:18px;margin-top:23px;color:#6c4a10}}.footer{{position:absolute;bottom:26px;left:55px;right:55px;border-top:1px solid #dce2eb;padding-top:14px;display:flex;justify-content:space-between;font-size:12px;color:#8794a9}}.footer span:last-child{{direction:ltr;font-family:monospace;letter-spacing:1px}}.mini{{display:flex;gap:16px;direction:ltr;margin-top:16px}}.mini div{{flex:1;border:1px solid #dbe2ed;border-radius:10px;padding:16px;text-align:center;background:white;font-size:18px}}.mini em{{font:13px monospace;color:#b07812;font-style:normal}}'''
def node(icon,title,sub,accent=False):return f'<div class="node {"accent" if accent else ""}"><span class="icon">{icon}</span><b>{title}</b><small>{sub}</small></div>'
def flow(items):return '<div class="flow">'+'<span class="arrow">→</span>'.join(items)+'</div>'
figures=[
 ('flow','01 / WORKFLOW ARCHITECTURE','هر رویداد، یک مسیر قابل‌ردیابی','سه لایه را جدا کنید: دریافت، تصمیم و اثر جانبی.',flow([node('01','دریافت رویداد','Webhook / Schedule'),node('02','بررسی و تصمیم','Validate / Route',True),node('03','اقدام کنترل‌شده','API / Database'),node('04','ثبت نتیجه','Observe / Recover')]),'تبدیل داده با ارسال پیام یکی نیست؛ برای اثر جانبی، سیاست تکرار تعریف کنید.'),
 ('webhook','02 / INPUT CONTRACT','از دادهٔ نامطمئن تا پاسخ روشن','همین مسیر در گردش‌کار آموزشی همراه مقاله پیاده‌سازی شده است.',flow([node('POST','ورودی ساختگی','name · email · eventId'),node('{ }','اعتبارسنجی','نوع، طول و فرمت',True),node('200','مسیر معتبر','valid: true / persisted: false'),node('422','مسیر نامعتبر','valid: false / errors')]),'دو کارت خروجی، دو نتیجهٔ جایگزین‌اند؛ در هر اجرا فقط یکی برگردانده می‌شود.'),
 ('idempotency','03 / RELIABILITY','تکرار درخواست، نه تکرار اثر','طرح مفهومی برای توسعهٔ نمونه به یک دریافت‌کنندهٔ پایدار.',flow([node('ID','رویداد پایدار','source + eventId'),node('UNIQ','ثبت اتمیک','Unique constraint',True),node('NEW','رویداد جدید','صف پردازش / outbox'),node('DUP','رویداد تکراری','پاسخ بدون اثر اضافه')]),'ثبت یکتا به‌تنهایی exactly-once نیست؛ مقصد خارجی به idempotency یا reconciliation نیاز دارد.'),
 ('infrastructure','04 / DEPLOYMENT','مرزهای روشن، دسترسی محدود','طرح مفهومی مبنای staging: برنامه، پایگاه داده و runner جداگانه.',flow([node('TLS','کاربر و سرویس','HTTPS'),node('EDGE','Reverse proxy','Forwarded headers'),node('n8n','هماهنگ‌کننده','127.0.0.1:5678',True)])+'<div class="mini"><div>PostgreSQL <em>↔ n8n</em></div><div>External runner <em>↔ n8n broker</em></div></div>','پایگاه داده و runner از شبکهٔ داخلی به n8n متصل‌اند؛ پورت عمومی ندارند.'),
 ('rag','05 / RETRIEVAL-AUGMENTED GENERATION','پاسخ، با پشتوانهٔ سند','بازیابی زمینه باید با مجوز کاربر و نسخهٔ معتبر سند هماهنگ باشد.',flow([node('ACL','کنترل دسترسی','منابع مجاز همان کاربر'),node('FIND','بازیابی مرتبط','Chunk / Embedding'),node('LLM','پیش‌نویس پاسخ','Context + Question',True),node('REF','بررسی شواهد','ارجاع قابل تطبیق')]),'RAG توهم را تضمینی حذف نمی‌کند؛ نبود شواهد باید به توقف یا مسیر انسانی منجر شود.'),
 ('human','06 / HUMAN-IN-THE-LOOP','پیشنهاد از مدل؛ اجازه از انسان','پارامترهای تأییدشده باید دقیقاً همان پارامترهای اجراشده باشند.',flow([node('AI','پیشنهاد ابزار','کمترین دسترسی'),node('VIEW','نمایش پارامترها','گیرنده، متن، مبلغ'),node('HUMAN','تأیید یا رد','هویت + زمان انقضا',True),node('RUN','اجرای مجاز','فقط پس از پذیرش')]),'رد تأیید نباید با retry دور زده شود؛ تغییر پارامترها نیازمند تأیید تازه است.')
]
# A branch represents mutually exclusive results, not a serial 200 -> 422 path.
CSS += '.branch-flow{display:flex;align-items:center;direction:ltr;gap:14px;padding:18px 0}.branch-flow>.node{min-height:190px}.branch-results{flex:1.2;display:flex;flex-direction:column;gap:13px}.branch-results .node{min-height:83px;padding:12px 17px}.branch-results .node b{display:inline;font-size:20px;margin:0 10px}.branch-results .node small{font-size:13px;margin-top:5px}.branch-results .icon{font-size:17px;padding:6px}.split-arrows{font:30px/2.3 monospace;color:#b58a31;min-width:30px}'
def branched(first,decision,yes,no):
    return '<div class="branch-flow">'+first+'<span class="arrow">→</span>'+decision+'<div class="split-arrows">↗<br>↘</div><div class="branch-results">'+yes+no+'</div></div>'
updated=[]
for name,label,title,sub,body,note in figures:
    if name=='webhook':
        body=branched(node('POST','ورودی ساختگی','name · email · eventId'),node('{ }','اعتبارسنجی','نوع، طول و فرمت',True),node('200','معتبر','valid: true / persisted: false'),node('422','نامعتبر','valid: false / errors'))
    if name=='idempotency':
        body=branched(node('ID','رویداد پایدار','source + eventId'),node('UNIQ','ثبت اتمیک','Unique constraint',True),node('NEW','دریافت جدید','صف پردازش / outbox'),node('DUP','دریافت تکراری','بدون اثر جانبی تازه'))
    updated.append((name,label,title,sub,body,note))
figures=updated
with sync_playwright() as p:
 browser=p.chromium.launch(args=['--no-sandbox']);page=browser.new_page(viewport={'width':1440,'height':660},device_scale_factor=1.5)
 for name,label,title,sub,body,note in figures:
  html=f'<html lang="fa"><style>{CSS}</style><body><div class="label">{label}</div><h1>{title}</h1><p class="subtitle">{sub}</p>{body}<div class="note">{note}</div><div class="footer"><span>تصویر مفهومی · راهنمای فارسی n8n</span><span>REZAIAN / ENGINEERING NOTES</span></div></body></html>'
  page.set_content(html);page.evaluate('document.fonts.ready');page.screenshot(path=str(OUT/f'{name}.png'))
 import json
 meta=json.loads((ROOT/'docs/assets/book-meta.json').read_text())
 cover='data:image/png;base64,'+base64.b64encode((ROOT/'docs/previews/cover.png').read_bytes()).decode()
 page.set_viewport_size({'width':1200,'height':630})
 social=f"""<html dir="rtl"><style>@font-face{{font-family:V;src:url('{font}')}}*{{box-sizing:border-box}}body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#101c32;color:#f7f4ec;font-family:V}}.grid{{display:flex;height:100%;padding:55px 70px;gap:90px;background:radial-gradient(ellipse at 10% 90%,#23465355,transparent 70%)}}.text{{flex:1;padding-top:20px}}.kicker{{font:11px monospace;letter-spacing:3px;color:#e6bd72}}h1{{font:800 92px/1.2 V;margin:22px 0 10px;direction:ltr;text-align:right}}h2{{font-size:34px;line-height:1.8;margin:10px 0}}h2 span{{color:#ebc57e}}p{{font-size:15px;color:#9caec7}}.by{{border-top:1px solid #3a4d6b;margin-top:28px;padding-top:20px;font-size:18px}}.book{{width:330px;flex-shrink:0;transform:none}}.book img{{width:100%;border:1px solid #65728b;box-shadow:none}}.meta{{font-size:13px;color:#afc4df;margin-top:20px}}</style><div class="grid"><div class="text"><div class="kicker">THE ILLUSTRATED PERSIAN GUIDE</div><h1>n8n.</h1><h2>اتوماسیون،<br><span>قابل‌اعتماد و قابل‌آزمون.</span></h2><p>از مدل ذهنی تا ساختن سیستم‌های قابل‌اعتماد</p><div class="by">محمدرضا رضائیان</div><div class="meta">{meta['pages']} صفحه · ۲۶ فصل · ۷۶ پرسش تحلیلی</div></div><div class="book"><img src="{cover}"></div></div></html>"""
 page.set_content(social);page.evaluate('document.fonts.ready');page.screenshot(path=str(ROOT/'docs/assets/social.png'))
 browser.close()
print(f'Rendered {len(figures)} original technical illustrations.')
