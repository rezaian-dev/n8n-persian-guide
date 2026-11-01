# استقرار

دو پیکربندی عمداً جدا هستند. مراحل کامل: بخش‌های ۶ و ۱۳ تا ۱۸ مقاله.

## محلی

```bash
docker compose -f deploy/compose.local.yaml up -d
```

فقط `localhost:5678`، بدون TLS، بدون اسرار واقعی. Secure cookie صرفاً برای این تست HTTP خاموش است. runner داخلی پیش‌فرض برای این محیط محدود و ساختگی است، نه دادهٔ حساس.

## Staging

```bash
cp deploy/.env.example deploy/.env
# دامنه و همهٔ رمزهای نمونه را عوض کنید؛ هر رمز مستقل باشد.
chmod 600 deploy/.env
docker compose --env-file deploy/.env -f deploy/compose.server.yaml config --quiet
docker compose --env-file deploy/.env -f deploy/compose.server.yaml up -d
```

PostgreSQL + external runner، نیازمند proxy میزبان و TLS. Caddyfile فقط نمونهٔ proxy میزبان است. رمزهای محیط از تنظیمات کانتینر برای مدیر میزبان قابل مشاهده‌اند؛ برای محیط حساس secrets manager بررسی شود.

تصویر PostgreSQL نسخهٔ نمونهٔ ثابت است، نه ادعای تازه‌ترین patch امن؛ قبل از استقرار واقعی tag پشتیبانی‌شده و patchشده را بررسی و در staging آزمایش کنید. نسخهٔ n8n و runner باید یکسان باشد. فایل Compose عمداً Queue mode، HA و backup خودکار ندارد.

این پیکربندی‌ها در این محیط با Docker اجرا نشده‌اند. قابلیت‌ها، سخت‌سازی، منابع، backup/restore، محدودیت شبکه و نسخه‌های سازگار را در محیط مقصد آزمایش کنید. از `down -v` در محیط دارای داده استفاده نکنید.
