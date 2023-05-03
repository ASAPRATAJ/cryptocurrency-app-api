# Generated by Django 4.0.10 on 2023-05-03 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_vote_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='price_change_percentage',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
            preserve_default=False,
        ),
    ]
