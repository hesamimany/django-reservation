# Generated by Django 4.2.3 on 2023-07-07 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_hotelreservation_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelreservation',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel'),
        ),
    ]