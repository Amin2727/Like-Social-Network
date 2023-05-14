from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    # برای اینکه فایل سیگنال رو بخونه باید در اینجا ایمپورتش کنم با تابع زیر
    def ready(self):
        from . import signals