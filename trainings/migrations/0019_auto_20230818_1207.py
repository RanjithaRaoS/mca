# Generated by Django 3.1.3 on 2023-08-18 06:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainings', '0018_weightentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='trainingplan',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,null=True),
        ),
        migrations.AddField(
            model_name='weightentry',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,null=True),
        ),
        migrations.AlterField(
            model_name='weightentry',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 8, 18, 6, 37, 52, 160772, tzinfo=utc),null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]