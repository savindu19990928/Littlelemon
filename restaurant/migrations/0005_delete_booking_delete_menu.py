# Generated by Django 5.0 on 2023-12-04 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20231204_2205'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
    ]