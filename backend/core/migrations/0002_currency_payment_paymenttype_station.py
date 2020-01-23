# Generated by Django 3.0.2 on 2020-01-23 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='A short currency code', max_length=3)),
                ('label', models.CharField(help_text='A human-readable currency label', max_length=86)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Type of the payment. Eg, Fuel, Service, Card wash, others', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A station name', max_length=256)),
                ('place', models.CharField(help_text='A place where the station located', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(help_text='Money amount of the payment')),
                ('date', models.CharField(help_text='A date of the payment. Should be ISO string', max_length=64)),
                ('comment', models.TextField(help_text='A payment commenct', null=True)),
                ('odometer', models.IntegerField(help_text='The car current odometer value when payment was made', null=True)),
                ('fuel_price', models.IntegerField(help_text='A fuel price. Total price can be calculated automatically if it is a Fuel payment ')),
                ('fuel_amount', models.IntegerField(help_text='An amount of the fuel (Litre).')),
                ('car', models.ForeignKey(help_text='A car for what the payment had been done', on_delete=django.db.models.deletion.CASCADE, to='core.Car')),
                ('currency', models.ForeignKey(help_text='A currency type of the payment', on_delete=django.db.models.deletion.CASCADE, to='core.Currency')),
                ('fuel_subtype', models.ForeignKey(help_text='Fuel subtype, 95, 92, Extra, etc.', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.FuelSubType')),
                ('payment_type', models.ForeignKey(help_text='A payment type', on_delete=django.db.models.deletion.CASCADE, to='core.PaymentType')),
                ('station', models.ForeignKey(help_text='A station where payment had been made', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Station')),
            ],
        ),
    ]
