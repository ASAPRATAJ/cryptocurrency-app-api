# Generated by Django 4.0.10 on 2023-04-29 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_vote_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote_number',
            field=models.IntegerField(null=True),
        ),
    ]
