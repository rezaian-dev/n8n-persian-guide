<div align="center">

<img src="docs/assets/social.png" alt="n8n Persian Guide — راهنمای جامع و کاربردی n8n" width="100%" />

# راهنمای جامع و کاربردی n8n
### از اتصال ابزارها تا ساختن سیستم‌های قابل‌اعتماد

**نویسنده و گردآورنده: محمدرضا رضائیان**

[**🌐 معرفی مقاله و دریافت PDF**](https://rezaian-dev.github.io/n8n-persian-guide/) · [**⬇️ دانلود مستقیم PDF**](docs/N8N-Persian-Guide.pdf) · [**📖 متن مقاله**](guide.md) · [**⚙️ گردش‌کار نمونه**](workflows/lead-intake.json)

**PDF فارسی ۲۴ صفحه‌ای** · ۲۶ بخش کاربردی · نمونهٔ JSON · ۱۰ تست مستقل

</div>

---

<div dir="rtl">

## چرا این راهنما؟

این مقاله برای کسی نوشته شده که می‌خواهد از «چند نود متصل» عبور کند و یک فرایند قابل‌فهم، قابل‌بازیابی و امن بسازد. از JSON و Webhook شروع می‌کنیم، به API، اعتبارسنجی، Idempotency و عملیات می‌رسیم، و در پایان AI، RAG و تأیید انسانی را با مرزهای روشن بررسی می‌کنیم.

**بررسی منابع:** ۱ نوامبر ۲۰۲۶ · **مبنای مثال‌ها:** n8n 2.45.7. مستندات زنده و نسخه‌ها تغییر می‌کنند؛ این تاریخ تضمین به‌روزبودن همیشگی نیست.

## مسیرهای مطالعه

| مسیر | موضوع |
|---|---|
| ساختن | مفاهیم، داده، Expression، نصب محلی، Webhook و اعتبارسنجی |
| قابل‌اعتمادکردن | API، تکرار، خطا، Retry، دریافت پایدار و اثر جانبی |
| عملیات | PostgreSQL، runner خارجی، TLS، امنیت، صف، پایش و بازیابی |
| هوشمندسازی | مدل و Agent، RAG، MCP، تأیید انسانی و ارزیابی |

## شروع سریع

</div>

```bash
git clone https://github.com/rezaian-dev/n8n-persian-guide.git
cd n8n-persian-guide
docker compose -f deploy/compose.local.yaml up -d
```

<div dir="rtl">

رابط را در `http://localhost:5678` باز کنید. فایل [lead-intake.json](workflows/lead-intake.json) را وارد کنید و بخش ۷ مقاله را دنبال کنید. نمونه فقط ورودی را اعتبارسنجی می‌کند؛ **ثبت پایدار یا اتصال CRM ندارد** و Webhook بدون احراز هویت آن فقط برای آزمایش محلی است.

## ساختار مخزن

</div>

```text
.
├── guide.md                    # متن اصلی مقاله
├── docs/                       # لندینگ معرفی، PDF و نسخهٔ HTML
│   ├── N8N-Persian-Guide.pdf    # خروجی اصلی؛ PDF فارسی صفحه‌آرایی‌شده
│   └── previews/               # تصاویر واقعی صفحات PDF
├── workflows/lead-intake.json   # گردش‌کار آموزشی کم‌وابستگی
├── examples/normalize-lead.js   # منطق اعتبارسنجی بدون وابستگی
├── tests/lead.test.mjs          # تست منطق و ساختار گردش‌کار
├── deploy/                     # Compose محلی و مبنای staging
├── scripts/                    # ساخت و بررسی سایت
└── .github/workflows/ci.yml     # بررسی خودکار، نه استقرار n8n
```

<div dir="rtl">

## ساخت سایت و اجرای تست

نیازمندی: Python 3.10+، Node.js 20+؛ Docker فقط برای اجرای خود n8n.

</div>

```bash
python -m pip install -r requirements.txt
npm test
python scripts/build.py
python scripts/check.py
python -m http.server 8080 --directory docs
```

<div dir="rtl">

**خروجی اصلی، [PDF صفحه‌آرایی‌شدهٔ ۲۴ صفحه‌ای](docs/N8N-Persian-Guide.pdf) است**؛ با جلد اختصاصی، عکس نویسنده، فهرست لینک‌دار، بوکمارک، شمارهٔ صفحه و متن قابل انتخاب و جست‌وجو.

سایت GitHub Pages صفحهٔ معرفی مقاله است: جلد سه‌بعدی، سرفصل‌های دسته‌بندی‌شده، پیش‌نمایش واقعی صفحات و دکمهٔ دانلود PDF. [نسخهٔ HTML کامل](https://rezaian-dev.github.io/n8n-persian-guide/reader.html) جداگانه حفظ شده است. فونت و تصاویر محلی‌اند و وابستگی به CDN وجود ندارد.

### بازتولید PDF

```bash
python -m pip install -r requirements-pdf.txt
python scripts/build_pdf.py
python scripts/build.py
```

ساخت PDF به کتابخانه‌های سیستمی Pango/HarfBuzz/Fontconfig نیاز دارد؛ راهنمای نصب WeasyPrint را برای سیستم‌عامل خود ببینید. اسکریپت، PDF، تصویر جلد و پیش‌نمایش‌های واقعی را تولید می‌کند. برای جزئیات آزمون صفحه‌آرایی، `PDF-QUALITY.md` را ببینید.

## وضعیت آزمون و محدودیت‌ها

- منطق اعتبارسنجی و اتصال‌های JSON به‌طور مستقل با Node.js تست می‌شوند.
- سایت از منبع Markdown ساخته می‌شود و مسیرهای محلی و anchorها بررسی می‌شوند.
- Import و اجرای واقعی workflow در n8n، Docker، TLS، API خارجی و backup/restore باید در محیط مقصد تست شوند.
- بخش AI طرح معماری و راهنمای پیاده‌سازی است؛ نمونهٔ متصل به مدل با کلید واقعی نیست.
- فایل server Compose، نقطهٔ شروع staging است؛ پیکربندی کامل و تضمین‌شدهٔ Production نیست.

## انتشار GitHub Pages

در Settings → Pages، روش Deploy from a branch، شاخهٔ `main` و پوشهٔ `/docs` را انتخاب کنید. سایت ایستا است و GitHub Pages خود n8n را اجرا نمی‌کند. فایل تولیدشدهٔ سایت در مخزن نگه داشته شده تا انتشار بدون build اختصاصی امکان‌پذیر باشد.

## نویسنده

<img src="docs/assets/author.webp" width="150" alt="محمدرضا رضائیان" />

**محمدرضا رضائیان — Front-End Engineer**<br />
[GitHub](https://github.com/rezaian-dev) · [پورتفولیو](https://rezaian-dev.vercel.app/fa) · [ایمیل](mailto:mrezaian.dev@gmail.com)

این راهنما با کمک ابزارهای پژوهش و نگارش هوش مصنوعی تهیه شده است. حدود آزمون و تاریخ منابع شفاف‌اند. برای اصلاح فنی، [راهنمای مشارکت](CONTRIBUTING.md) را ببینید؛ اطلاعات حساس را در Issue قرار ندهید.

## حقوق

همهٔ حقوق متن، طراحی، مثال‌ها و عکس نویسنده محفوظ است؛ [جزئیات](LICENSE.md). فونت Vazirmatn مجوز مستقل SIL OFL دارد. n8n مجوز مستقل Sustainable Use License / Enterprise دارد؛ این مقاله پروژهٔ رسمی n8n نیست.

</div>
