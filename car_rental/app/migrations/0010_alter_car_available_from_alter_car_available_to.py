# Generated by Django 5.1.3 on 2024-12-12 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_car_available_from_alter_car_available_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='available_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 12, 16, 35, 1, 406716)),
        ),
        migrations.AlterField(
            model_name='car',
            name='available_to',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 12, 16, 35, 1, 406716)),
        ),
    ]
