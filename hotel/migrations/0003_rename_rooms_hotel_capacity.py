# Generated by Django 4.2.3 on 2023-07-07 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_hotel_rooms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='rooms',
            new_name='capacity',
        ),
    ]
