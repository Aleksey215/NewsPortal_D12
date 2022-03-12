# Согласно документации к Celery, мы должны добавить строки:
from .celery import app as celery_app

__all__ = ('celery_app',)