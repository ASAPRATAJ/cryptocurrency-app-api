# Generated by Django 4.0.10 on 2023-04-19 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_tag_coin_symbol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coin',
            name='actual_price',
        ),
        migrations.RemoveField(
            model_name='coin',
            name='price_for_the_last_30_days',
        ),
        migrations.AlterField(
            model_name='coin',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coin',
            name='symbol',
            field=models.CharField(max_length=10),
        ),
    ]
