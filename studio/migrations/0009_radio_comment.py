# Generated by Django 5.1 on 2024-08-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0008_alter_bookingstatus_options_booking_service_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Radio_Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commenter_name', models.CharField(max_length=100)),
                ('commenter_email', models.EmailField(blank=True, max_length=254)),
                ('comment', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
