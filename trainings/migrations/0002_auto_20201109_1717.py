# Generated by Django 3.1.3 on 2020-11-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='time_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='time_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
