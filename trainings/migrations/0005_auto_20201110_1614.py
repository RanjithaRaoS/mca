# Generated by Django 3.1.3 on 2020-11-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0004_auto_20201110_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.TextField(default='Exercise'),
        ),
    ]
