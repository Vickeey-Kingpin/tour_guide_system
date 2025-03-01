# Generated by Django 5.1.4 on 2025-02-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourapp', '0012_rename_hotel_latitude_hotel_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='site',
            field=models.CharField(choices=[('Game Park', 'GP'), ('Museum', 'M'), ('Airport', 'A')], max_length=15),
        ),
    ]
