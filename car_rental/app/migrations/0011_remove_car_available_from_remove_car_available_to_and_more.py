# Generated by Django 5.1.3 on 2024-12-12 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_car_available_from_alter_car_available_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='available_from',
        ),
        migrations.RemoveField(
            model_name='car',
            name='available_to',
        ),
        migrations.AddField(
            model_name='car',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
