# Generated by Django 4.0.10 on 2023-04-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_vote_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='coin_id',
            field=models.CharField(max_length=255),
        ),
    ]
