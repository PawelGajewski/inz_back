# Generated by Django 2.2.6 on 2019-11-16 21:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warsztat', '0009_auto_20191116_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='version',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='service',
            name='cli_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 16, 22, 16, 39, 432398)),
        ),
    ]
