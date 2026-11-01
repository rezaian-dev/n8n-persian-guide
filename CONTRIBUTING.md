# مشارکت در راهنما

برای گزارش خطا، شمارهٔ بخش، نسخهٔ n8n و نتیجهٔ قابل‌بازتولید را بنویسید. در مثال‌ها فقط دادهٔ ساختگی بفرستید. کلید، Credential، payload مشتری یا export دارای pinData واقعی ارسال نکنید.

ویرایش اصلی در `guide.md` است، نه `docs/index.html` که تولیدی است. برای تغییر ظاهر `scripts/template.html` و `docs/assets/style.css` را ویرایش کنید.

```bash
pip install -r requirements.txt
npm test
python scripts/build.py
python scripts/check.py
```

منبع رسمی و تاریخ بررسی برای ادعای نسخه‌محور لازم است. اصلاح فنی کوچک و قابل‌بررسی را به تغییر بزرگ ترجیح دهید. هیچ نمونه‌ای را بدون ثبت نوع آزمون «production-ready» معرفی نکنید.
