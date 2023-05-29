"""
Configuration for celery.
"""
import os

from celery import Celery
from celery.schedules import crontab

from calendar import monthrange
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def get_last_day_of_month():
    now = datetime.now()
    year = now.year
    month = now.month
    _, last_day = monthrange(year, month)
    return last_day


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


last_day = get_last_day_of_month()
app.conf.beat_schedule = {
    'fetch-coin-data-every-five-minutes': {
        'task': 'coin.tasks.fetch_coin_data_every_five_minutes',
        'schedule': crontab(minute='*/5'),
    },
    'calculate-monthly-votes': {
        'task': 'app.tasks.calculate_votes',
        'schedule': crontab(day_of_month=last_day, hour=16, minute='30'),
    },
    'reset-votes': {
        'task': 'app.tasks.reset_votes',
        'schedule': crontab(day_of_month='1', hour='1', minute='0'),
    },
}

# Uruchomienie Celery
if __name__ == '__main__':
    app.start()
