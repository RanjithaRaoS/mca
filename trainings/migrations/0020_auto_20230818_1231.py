# Generated by Django 3.1.3 on 2023-08-18 07:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0019_auto_20230818_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='user',
        ),
        migrations.RemoveField(
            model_name='trainingplan',
            name='user',
        ),
        migrations.RemoveField(
            model_name='weightentry',
            name='user',
        ),
        migrations.AlterField(
            model_name='weightentry',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 8, 18, 7, 1, 26, 980640, tzinfo=utc)),
        ),
    ]