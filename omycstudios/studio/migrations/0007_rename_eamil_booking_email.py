# Generated by Django 5.1 on 2024-08-10 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0006_booking_contact_booking_eamil'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='eamil',
            new_name='email',
        ),
    ]
