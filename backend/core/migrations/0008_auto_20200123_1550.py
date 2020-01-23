# Generated by Django 3.0.2 on 2020-01-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200123_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fuelsubtype',
            name='code',
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_displacement',
            field=models.DecimalField(decimal_places=2, help_text='An engine volume. Eg 2.2, 5.6 etc.', max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Money amount of the payment', max_digits=9),
        ),
        migrations.AlterField(
            model_name='payment',
            name='fuel_amount',
            field=models.DecimalField(decimal_places=2, help_text='An amount of the fuel (Litre).', max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='fuel_price',
            field=models.DecimalField(decimal_places=2, help_text='A fuel price. Total price can be calculated automatically if it is a Fuel payment ', max_digits=5, null=True),
        ),
    ]
