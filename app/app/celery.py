import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'fetch-coin-data-every-five-minutes': {
        'task': 'coin.tasks.fetch_coin_data_every_five_minutes',
        'schedule': crontab(minute='*/5'),  # Harmonogram co 5 minut
    },
}

# Uruchomienie Celery
if __name__ == '__main__':
    app.start()
