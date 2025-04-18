# Generated by Django 5.1.4 on 2025-03-03 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourapp', '0016_tripbooking_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tripbooking',
            name='paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_paid',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_number',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
