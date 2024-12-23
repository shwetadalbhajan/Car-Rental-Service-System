# Generated by Django 5.1.3 on 2024-12-13 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_rename_drop_off_point_booking_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('hours', models.IntegerField()),
                ('address', models.TextField()),
                ('driver_needed', models.BooleanField(default=False)),
                ('total_price', models.FloatField()),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
