# Generated by Django 2.2.6 on 2019-11-17 18:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warsztat', '0011_auto_20191117_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='additional_info',
        ),
        migrations.RemoveField(
            model_name='service',
            name='parts_prize',
        ),
        migrations.RemoveField(
            model_name='service',
            name='total_prize',
        ),
        migrations.RemoveField(
            model_name='service',
            name='work_prize',
        ),
        migrations.AlterField(
            model_name='service',
            name='cli_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 17, 19, 49, 45, 594365)),
        ),
    ]
