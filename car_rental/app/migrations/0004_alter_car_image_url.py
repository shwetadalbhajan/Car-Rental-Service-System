# Generated by Django 5.1.3 on 2024-12-10 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_car_buying_price_alter_car_fuel_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='image_url',
            field=models.URLField(max_length=1000),
        ),
    ]
