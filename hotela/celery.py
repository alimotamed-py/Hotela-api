# import os
# from celery import Celery

# # تنظیم Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# # ساخت اپ celery
# app = Celery("booking_system")

# # گرفتن config از settings.py با prefix = CELERY_
# app.config_from_object("django.conf:settings", namespace="CELERY")

# # پیدا کردن task ها در همه اپ‌ها
# app.autodiscover_tasks()

# # (اختیاری ولی حرفه‌ای) نمایش لاگ بهتر
# app.conf.update(
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
#     timezone="UTC",
#     enable_utc=True,
# )