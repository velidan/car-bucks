# Generated by Django 3.0.2 on 2020-01-23 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_currency_payment_paymenttype_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.CharField(help_text='A date of the payment. Should be ISO string', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='fuel_amount',
            field=models.IntegerField(help_text='An amount of the fuel (Litre).', null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='fuel_price',
            field=models.IntegerField(help_text='A fuel price. Total price can be calculated automatically if it is a Fuel payment ', null=True),
        ),
    ]