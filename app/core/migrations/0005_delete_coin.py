# Generated by Django 4.0.10 on 2023-04-19 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_coin_actual_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coin',
        ),
    ]
