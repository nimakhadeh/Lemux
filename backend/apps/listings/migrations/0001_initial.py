# Generated for the portfolio repository.

from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Listing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="عنوان آگهی")),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                ("address", models.TextField(verbose_name="آدرس کامل")),
                ("city", models.CharField(max_length=100, verbose_name="شهر")),
                ("district", models.CharField(max_length=100, verbose_name="محله")),
                ("neighborhood", models.CharField(blank=True, max_length=100, verbose_name="محله")),
                ("price", models.BigIntegerField(validators=[MinValueValidator(0)], verbose_name="قیمت (تومان)")),
                ("area", models.FloatField(validators=[MinValueValidator(1)], verbose_name="متراژ (متر مربع)")),
                ("rooms", models.IntegerField(default=1, validators=[MinValueValidator(0)], verbose_name="تعداد اتاق")),
                ("year_built", models.IntegerField(blank=True, null=True, verbose_name="سال ساخت")),
                ("property_type", models.CharField(choices=[("apartment", "آپارتمان"), ("villa", "ویلا"), ("office", "دفتر کار"), ("store", "مغازه"), ("land", "زمین")], default="apartment", max_length=20, verbose_name="نوع ملک")),
                ("condition", models.CharField(choices=[("new", "نوساز"), ("renovated", "بازسازی شده"), ("normal", "معمولی"), ("old", "قدیمی")], default="normal", max_length=20, verbose_name="وضعیت ملک")),
                ("contact_phone", models.CharField(blank=True, max_length=15, verbose_name="تلفن تماس")),
                ("contact_name", models.CharField(blank=True, max_length=100, verbose_name="نام تماس")),
                ("source", models.CharField(choices=[("divar", "دیوار"), ("sheypoor", "شیپور"), ("ihome", "آی‌هوم"), ("manual", "دستی")], default="manual", max_length=20, verbose_name="منبع داده")),
                ("source_url", models.URLField(blank=True, verbose_name="لینک منبع")),
                ("source_id", models.CharField(blank=True, max_length=100, verbose_name="شناسه در منبع")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")),
                ("last_seen", models.DateTimeField(auto_now=True, verbose_name="آخرین مشاهده")),
                ("is_active", models.BooleanField(default=True, verbose_name="فعال")),
                ("is_verified", models.BooleanField(default=False, verbose_name="تأیید شده")),
            ],
            options={
                "verbose_name": "ملک",
                "verbose_name_plural": "املاک",
                "ordering": ["-created_at"],
                "db_table": "backend_propanalyzer_api_listing",
                "indexes": [
                    models.Index(fields=["city", "district"], name="listing_city_district_idx"),
                    models.Index(fields=["price"], name="listing_price_idx"),
                    models.Index(fields=["created_at"], name="listing_created_idx"),
                ],
            },
        ),
    ]
