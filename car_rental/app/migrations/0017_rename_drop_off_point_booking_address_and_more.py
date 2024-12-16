# Generated by Django 5.1.3 on 2024-12-13 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_booking_created_at_booking_razorpay_payment_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='drop_off_point',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='time_slot',
            new_name='start_time',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='pickup_point',
        ),
    ]
