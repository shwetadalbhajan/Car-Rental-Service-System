# Generated by Django 5.1.3 on 2024-12-12 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_car_available_from_remove_car_available_to_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='available',
        ),
    ]