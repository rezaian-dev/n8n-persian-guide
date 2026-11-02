<div align="center" dir="rtl">

<img src="docs/assets/social.png" alt="مرجع جامع و پروژه‌محور n8n — محمدرضا رضائیان" width="100%" />

# 📚 مرجع جامع و پروژه‌محور n8n

### فقط ابزارها را وصل نکنید؛ سیستم بسازید.

**از مدل ذهنی تا طراحی، آزمون و بازیابی اتوماسیون قابل‌اعتماد**<br />
نویسنده و گردآورنده: **محمدرضا رضائیان**

[**🌐 شروع مطالعهٔ آنلاین**](https://rezaian-dev.github.io/n8n-persian-guide/book/) • [**📕 دریافت PDF**](https://rezaian-dev.github.io/n8n-persian-guide/N8N-Persian-Guide.pdf) • [**📱 دریافت EPUB**](https://rezaian-dev.github.io/n8n-persian-guide/N8N-Persian-Guide.epub)

**۷۱ صفحهٔ PDF · ۲۶ فصل · ۷۶ پرسش پاسخ‌داده‌شده · ۳ پروژه و آزمایشگاه · ۳۴ تست مستقل**

[معرفی کتاب](https://rezaian-dev.github.io/n8n-persian-guide/) · [فهرست فصل‌ها](#-نقشهٔ-مطالعه) · [شروع عملی](#-از-خواندن-به-ساختن) · [متن منبع](guide.md)

</div>

<div dir="rtl">

## ✨ این کتاب دربارهٔ چیست؟

یک گردش‌کار که یک بار اجرا شده، هنوز یک سیستم قابل‌اعتماد نیست. این راهنما از **داده، Expression و Webhook** شروع می‌کند و به **ثبت پایدار، Idempotency، مدیریت خطا، استقرار امن، بازیابی و AI کنترل‌شده** می‌رسد؛ با مثال حل‌شده، حالت شکست، تمرین و معیار پذیرش.

هدف، حفظ‌کردن نام نودها نیست؛ باید بتوانید توضیح دهید **چه چیزی ممکن است شکست بخورد، مرز تضمین کجاست و با چه آزمونی به طراحی خود اعتماد می‌کنید.**

> 🗓️ آخرین بررسی منابع: **۱ نوامبر ۲۰۲۶** · مبنای مثال‌ها: **n8n 2.45.7**<br />
> این تاریخ و نسخه، مبنای تدوین‌اند؛ نه تضمین تازه‌ترین نسخه در آینده. پیش از استقرار، مستندات و وضعیت امنیتی نسخهٔ مقصد را بررسی کنید.

## 📖 سه روش برای خواندن

| قالب | مناسب برای | امکانات | دسترسی |
| --- | --- | --- | --- |
| 🌐 **آنلاین** | مطالعه روی موبایل و دسکتاپ | متن قابل انتخاب، جست‌وجوی درون کتاب، تم روشن و تیره، تغییر اندازهٔ قلم، کپی کد و ادامه از آخرین فصل | [شروع مطالعه](https://rezaian-dev.github.io/n8n-persian-guide/book/) |
| 📕 **PDF؛ نسخهٔ اصلی** | مطالعهٔ صفحه‌آرایی‌شده و چاپ | ۷۱ صفحهٔ A4، فهرست نقطه‌چین، بوک‌مارک، تصویر، تمرین و متن قابل جست‌وجو | [دانلود مستقیم](https://rezaian-dev.github.io/n8n-persian-guide/N8N-Persian-Guide.pdf) · [فایل مخزن](docs/N8N-Persian-Guide.pdf) |
| 📱 **EPUB 3** | کتاب‌خوان و مطالعهٔ همراه | متن واقعی و بازچینش‌پذیر، ترتیب خواندن راست‌به‌چپ، فهرست فصل‌ها، فونت فارسی و تصویرهای درون فایل | [دانلود مستقیم](https://rezaian-dev.github.io/n8n-persian-guide/N8N-Persian-Guide.epub) · [فایل مخزن](docs/N8N-Persian-Guide.epub) |

نسخهٔ آنلاین، تصویر صفحات PDF نیست؛ متن کامل کتاب است. EPUB نیز PDF تغییرنام‌یافته نیست و صفحه‌بندی ثابتی ندارد. کیفیت نمایش فارسی و امکانات تغییر قلم در EPUB به برنامهٔ کتاب‌خوان بستگی دارد. تنظیمات و آخرین فصلِ نسخهٔ آنلاین فقط در مرورگر شما ذخیره می‌شوند؛ حساب کاربری لازم نیست.

## 🎯 برای چه کسی نوشته شده؟

- **توسعه‌دهندهٔ وب:** اتصال فرم، API، پایگاه داده و سرویس‌ها با قرارداد روشن.
- **مسئول عملیات و تیم محصول:** امنیت، مشاهده‌پذیری، هزینه، پشتیبان‌گیری و بازیابی.
- **سازندهٔ اتوماسیون هوشمند:** RAG، خروجی ساختاریافته، محدودکردن ابزار و تأیید انسانی.
- **آماده‌شونده برای مصاحبه:** پاسخ تحلیلی، فرض‌ها، سناریوی شکست و مرز ادعا.

**پیش‌نیاز:** آشنایی مقدماتی با JSON، HTTP و خط فرمان؛ برای استقرار، Docker Compose و مفاهیم دامنه و TLS. پروژهٔ اول به حساب پولی یا کلید مدل نیاز ندارد.

## 🧭 نقشهٔ مطالعه

هر عنوان، مستقیماً فصل مربوط را در نسخهٔ آنلاین باز می‌کند. پیوست مصاحبه و منابع نیز در هر سه قالب وجود دارند.

<details open>
<summary><strong>🧩 بخش اول · مبانی و مدل ذهنی — فصل‌های ۱ تا ۵</strong></summary>

۱. [این راهنما برای چه کسی است؟](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-1)<br />
۲. [n8n چیست و چه مسئله‌ای را حل می‌کند؟](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-2)<br />
۳. [انتخاب ابزار: n8n، Make، Zapier یا کد؟](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-3)<br />
۴. [مدل ذهنی: رویداد، داده، اثر جانبی](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-4)<br />
۵. [داده در n8n: Item و Expression](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-5)

</details>

<details>
<summary><strong>🔌 بخش دوم · اولین گردش‌کار واقعی — فصل‌های ۶ تا ۹</strong></summary>

۶. [راه‌اندازی محلی و محدود](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-6)<br />
۷. [پروژهٔ دریافت و اعتبارسنجی درخواست مشاوره](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-7)<br />
۸. [اعتبارسنجی درست؛ فقط trim کافی نیست](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-8)<br />
۹. [اتصال API؛ قرارداد قبل از اتصال](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-9)

</details>

<details>
<summary><strong>🛡️ بخش سوم · اعتمادپذیری و اثر جانبی — فصل‌های ۱۰ تا ۱۲</strong></summary>

۱۰. [ثبت پایدار و Idempotency](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-10)<br />
۱۱. [خطا، Retry و جریان جبران](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-11)<br />
۱۲. [شاخه‌بندی، Merge، حجم داده و زمان‌بندی](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-12)

</details>

<details>
<summary><strong>⚙️ بخش چهارم · استقرار و عملیات — فصل‌های ۱۳ تا ۱۸</strong></summary>

۱۳. [PostgreSQL و runner جداگانه](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-13)<br />
۱۴. [دامنه، TLS و Reverse proxy](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-14)<br />
۱۵. [چک‌لیست امنیت](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-15)<br />
۱۶. [مقیاس‌پذیری و Queue mode](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-16)<br />
۱۷. [مشاهده‌پذیری و هزینه](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-17)<br />
۱۸. [پشتیبان‌گیری، بازیابی و ارتقا](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-18)

</details>

<details>
<summary><strong>🧠 بخش پنجم · هوش مصنوعی کنترل‌شده — فصل‌های ۱۹ تا ۲۲</strong></summary>

۱۹. [مدل، زنجیره و عامل](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-19)<br />
۲۰. [RAG؛ پاسخ مبتنی بر سند، نه وعدهٔ حذف توهم](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-20)<br />
۲۱. [ابزارهای AI، MCP و تأیید انسانی](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-21)<br />
۲۲. [دستیار پشتیبانی کم‌ریسک](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-22)

</details>

<details>
<summary><strong>🧪 بخش ششم · تست، عیب‌یابی و انتشار — فصل‌های ۲۳ تا ۲۶ و پیوست‌ها</strong></summary>

۲۳. [تست و ارزیابی؛ فراتر از «کار کرد»](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-23)<br />
۲۴. [عیب‌یابی سریع](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-24)<br />
۲۵. [نقشهٔ راه هفت‌روزه](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-25)<br />
۲۶. [چک‌لیست انتشار و جمع‌بندی](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-26)<br />
📋 [بانک سناریوهای مصاحبه و خودارزیابی](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-27)<br />
🔗 [منابع رسمی و یادداشت به‌روزبودن](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-28)<br />
👤 [دربارهٔ نویسنده](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-29)

</details>

## 🖼️ نگاهی به نسخهٔ چاپی

تصاویر زیر مستقیماً از PDF منتشرشده گرفته شده‌اند؛ نه طرح مفهومی یا ماکاپ سه‌بعدی.

| فهرست لینک‌دار | یک صفحهٔ واقعی از کتاب |
| :---: | :---: |
| ![فهرست ساده با نقطه‌چین تا شمارهٔ صفحه](docs/previews/sample-01.png) | ![صفحهٔ استقرار با تصویر زیرساخت، توضیح و تمرین](docs/previews/sample-02.png) |

## 🚀 از خواندن به ساختن

| پروژه / آزمایشگاه | چه چیزی را تمرین می‌کنید؟ | فایل |
| --- | --- | --- |
| **دریافت درخواست مشاوره** | Webhook، اعتبارسنجی، پاسخ‌های ۲۰۰ و ۴۲۲ | [گردش‌کار n8n](workflows/lead-intake.json) · [منطق Code node](examples/normalize-lead.js) |
| **دریافت پایدار و Outbox** | ثبت اتمیک، تکرار، تضاد داده، مالکیت lease و ماندگاری پس از restart | [آزمایشگاه مستقل](projects/durable_intake.py) |
| **مرز اعتماد AI** | schema سخت‌گیرانه، مجوز سند، ابزار محدود و تطبیق تأیید انسانی | [آزمایشگاه مستقل](projects/ai_boundary.mjs) |

### اجرای نمونهٔ محلی

با Docker و Compose، و **فقط دادهٔ ساختگی**:

<div dir="ltr">

```bash
docker compose -f deploy/compose.local.yaml up -d
```

</div>

نشانی `http://localhost:5678` را باز کنید، حساب مالک محلی بسازید و فایل گردش‌کار را وارد کنید. راهنمای اجرا در [فصل ۷](https://rezaian-dev.github.io/n8n-persian-guide/book/#chapter-7) است.

> ⚠️ این گردش‌کار **داده را ذخیره نمی‌کند، به CRM وصل نمی‌شود و پیام نمی‌فرستد**. Webhook بدون احراز هویت، فقط برای آزمایش محلیِ ایزوله است. انتشار عمومی به احراز هویت، محدودسازی نرخ و بررسی امنیت نیاز دارد.

<details>
<summary><strong>🔬 مرز تضمین آزمایشگاه‌ها؛ پیش از استفاده بخوانید</strong></summary>

آزمایش‌های حل‌شده در فصل‌های ۱۰ و ۱۹ آمده‌اند. دو آزمایشگاه مستقل، به n8n زنده، مدل، پایگاه برداری، سرور MCP یا ابزار خارجی متصل نیستند.

- **Outbox:** تحویل از نوع at-least-once است. خرابی پس از موفقیت مقصد و پیش از ثبت تأیید می‌تواند اثر را تکرار کند؛ idempotency مقصد یا reconciliation همچنان لازم است. SQLite ابزار آموزشی است، نه تنظیم Queue mode در n8n. مقدار `source` باید از زمینهٔ احراز هویت بیاید. serialization این مثال Python-local است و استاندارد امضای بین‌سامانه‌ای نیست. سقف خودکار تلاش، dead-letter، retention، پایش و سخت‌سازی پروداکشن پیاده‌سازی نشده‌اند. **تمرین:** سقف تلاش، وضعیت نهایی قابل بازرسی و آزمون replay مجاز اضافه کنید.
- **AI:** زمینه و تأیید باید از سامانهٔ معتبر احراز هویت و ممیزی بیایند. digest امضا یا اثبات هویت نیست. بررسی خالص تأیید، آن را اتمیک مصرف نمی‌کند و اجرای یک‌باره را تضمین نمی‌کند. **تمرین:** مخزن تأیید احرازشده بسازید و مصرف هم‌زمان، انقضا و خرابی پس از تحویل را تست کنید.
- **استقرار:** Compose سرور، نقطهٔ شروع staging است؛ نه محصول آمادهٔ پروداکشن. secrets را از روی `deploy/.env.example` جایگزین کنید، نسخهٔ n8n و runner را هماهنگ نگه دارید و TLS و بازیابی را واقعاً آزمایش کنید. روی دادهٔ مهم، هرگز `down -v` اجرا نکنید.

</details>

## 🛠️ ساخت و اعتبارسنجی

پیش‌نیاز: **Python 3.10+** و **Node.js 20+**، به‌همراه کتابخانه‌های سیستمی WeasyPrint مانند Pango، HarfBuzz، Fontconfig و DejaVu Sans Mono؛ [راهنمای نصب](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation). تست‌های Node از runner داخلی استفاده می‌کنند؛ نیازی به نصب پکیج Node نیست.

<div dir="ltr">

```bash
python -m pip install -r requirements.txt
node --test tests/*.test.mjs
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/build_pdf.py
python scripts/build.py
python scripts/check.py
python -m http.server 8080 --directory docs
```

</div>

`build_pdf.py` فایل PDF، پیش‌نمایش‌ها و متادیتا را می‌سازد. `build.py` صفحهٔ معرفی، خوانشگر آنلاین و EPUB را تولید می‌کند؛ ساخت EPUB به ابزار یا وابستگی تازه‌ای نیاز ندارد. فایل‌های تولیدشده را دستی ویرایش نکنید.

<details>
<summary><strong>🗂️ ساختار ضروری مخزن و مسیر ویرایش</strong></summary>

| مسیر | نقش |
| --- | --- |
| `guide.md` | منبع مشترک متن و منابع رسمی هر سه قالب |
| `docs/` | خروجی انتشار و دارایی‌های محلی لازم برای GitHub Pages |
| `scripts/build_pdf.py` و `scripts/book.css` | صفحه‌آرایی PDF |
| `scripts/book-notes.json` | هدف‌ها، تمرین‌ها و معیار پذیرش فصل‌ها |
| `scripts/build_ebook.py` | تبدیل مشترک متن برای EPUB و خوانشگر |
| `scripts/landing.html` و `docs/assets/landing.{css,js}` | صفحهٔ معرفی و تعامل‌های Motion |
| `docs/assets/reader.{css,js}` | ظاهر و امکانات خوانشگر |
| `scripts/check.py` | ورودی یکپارچهٔ بررسی انتشار |
| `workflows/`، `examples/` و `projects/` | نمونهٔ قابل واردکردن و آزمایشگاه‌های مستقل |
| `tests/` | ۲۲ تست Node.js و ۱۲ تست Python |
| `deploy/` | نمونهٔ محلی و مبنای staging |

خروجی‌ها در Git نگه داشته می‌شوند چون Pages از `main:/docs` سرو می‌شود. منابع ساخت نیز برای بازتولید لازم‌اند. پوشهٔ وابستگی، محیط خصوصی، اسکرین‌شات موقت و نسخهٔ تکراریِ منبع کتاب در مخزن قرار نمی‌گیرند. مجوزهای فونت و Motion باید کنار دارایی‌هایشان بمانند.

بازسازی اختیاری تصویرهای فنی به Playwright نیاز دارد؛ برای خواندن، میزبانی یا CI معمول لازم نیست:

<div dir="ltr">

```bash
python -m pip install playwright==1.64.1
python -m playwright install --with-deps chromium
python scripts/build_figures.py
python scripts/build_pdf.py
python scripts/build.py
```

</div>

`.gitattributes` آمار زبان‌های GitHub را به HTML، CSS و JavaScript سمت خواننده محدود می‌کند. ابزارهای Python و کد کمکی حذف نشده‌اند؛ فقط از آمار خارج‌اند. محاسبهٔ مجدد آمار در GitHub ممکن است با تأخیر انجام شود.

</details>

## ✅ چه چیزی بررسی شده؛ چه چیزی نه؟

- **۳۴ تست مستقل** منطق مثال‌ها و مرز سیاست‌ها را بررسی می‌کنند؛ نه اجرای کامل n8n و نه آمادگی پروداکشن را.
- بررسی یکپارچه، فایل‌ها، لینک‌ها، تطابق منبع، ساختار EPUB، فصل‌های خوانشگر، بوک‌مارک‌ها، مقصدهای PDF، متن قابل جست‌وجو و محدودهٔ صفحه را کنترل می‌کند. CI بازتولید بدون تغییرِ خوانشگر و EPUB را نیز بررسی می‌کند.
- صفحه‌آرایی PDF، هر **۱۳۰ جای‌گذاری آیکن آموزشی** را از نظر قرارگیری در محفظه، مرکز بودن و تداخل با متن می‌سنجد. چند صفحهٔ نماینده نیز بصری بررسی شده‌اند؛ این کار گواهی PDF/UA یا ویرایش انسانی کامل نیست.
- EPUB با **EPUBCheck 5.3.0** بررسی شده است؛ سازگاری با همهٔ برنامه‌های کتاب‌خوان ادعا نمی‌شود.
- اجرای Docker، ورود و اجرای workflow در n8n، TLS، سرویس خارجی، مدل، ظرفیت و بازیابی نسخهٔ پشتیبان به آزمون در محیط مقصد نیاز دارند.

## 🤝 اصلاح و گزارش امنیتی

برای پیشنهاد اصلاح، فصل، نسخهٔ نرم‌افزار، نتیجهٔ مورد انتظار و یک نمونهٔ کوچک با دادهٔ ساختگی بفرستید. تغییرات متمرکز، منبع رسمی و دامنهٔ واقعی تست را مشخص کنید. **اعتبارنامه، دادهٔ مشتری، payload خصوصیِ pin‌شده یا خروجی پاک‌سازی‌نشدهٔ workflow منتشر نکنید.**

آسیب‌پذیری مثال‌ها یا وب‌سایت را خصوصی به **mrezaian.dev@gmail.com** گزارش کنید؛ مشکلات خود محصول n8n باید از مسیر امنیتی رسمی همان محصول گزارش شوند. این مخزن سرویس عمومی n8n اجرا نمی‌کند.

## 👤 نویسنده و حقوق اثر

**محمدرضا رضائیان — Front-End Engineer**<br />
[پورتفولیو](https://rezaian-dev.vercel.app/fa) · [GitHub](https://github.com/rezaian-dev)

تهیه‌شده با کمک ابزارهای پژوهش و نگارش هوش مصنوعی. حقوق متن، طراحی، مثال‌ها و عکس محفوظ است؛ [مجوز و حقوق اثر](LICENSE.md) را ببینید. Motion با مجوز MIT و Vazirmatn با SIL OFL استفاده شده‌اند و مجوزهای اصلی همراه فایل‌ها هستند. n8n مجوز مستقل Sustainable Use / Enterprise دارد. این راهنما مستقل است و وابسته یا مورد تأیید n8n نیست.

---

**یک فرایند کوچک انتخاب کنید؛ آن را بسازید، خراب کنید و با شواهد بهترش کنید.** 🌱

</div>
