# Generated by Django 4.0.10 on 2023-04-15 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
                ('actual_price', models.FloatField()),
                ('price_for_the_last_30_days', models.FloatField()),
            ],
        ),
    ]
