from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

FUEL_TYPES = [
  (0, 'Diesel'),
  (1, 'Benzin'),
  (2, 'Gas'),
]

# to have a possibility to change the User model in future if necessary
class User(AbstractUser):
    pass

class Car(models.Model):
  user = models.ForeignKey('User', 
    on_delete=models.CASCADE, 
    help_text='A car user.', 
    related_name='cars')

  model = models.CharField(max_length=256, help_text='A car model')
  initial_odometer = models.IntegerField(help_text='The car initial odometer')
  current_odometer = models.IntegerField(help_text=('The car current odometer. ' + 
                                                    'Updates automatically at each payment when you fill the odometer field '))

  year = models.IntegerField(help_text='The car year')
  fuel_type = models.ForeignKey('FuelType', on_delete=models.CASCADE, help_text='A fuel type that your car use')


class FuelType(models.Model):
  code = models.IntegerField(choices=FUEL_TYPES, default=0, help_text='Fuel Type. Diesel | Benzing | Gas | Spiritus, etc. Short code for it')
  label = models.CharField(max_length=256, help_text='A human readable label of the fuel type.')
  # fuel_type = models.CharField(choices=FUEL_TYPES, default=0)


class FuelSubType(models.Model):
  fuel_type = models.ForeignKey('FuelType', on_delete=models.CASCADE, help_text='A fuel subtype. Eg, benzin Extra | 95 | 92, etc.')

  code = models.IntegerField(help_text='The fuel subtype code. Must be unique ')
  label = models.CharField(max_length=256, help_text='A human readable label of the fuel subtype type.')


class PaymentType(models.Model):
  label = models.CharField(max_length=256, help_text='Type of the payment. Eg, Fuel, Service, Card wash, others')


class Currency(models.Model):
  code = models.CharField(max_length=3, help_text='A short currency code')
  label = models.CharField(max_length=86, help_text='A human-readable currency label')

# In general it's a fuel station, but could be a car wash/service station, etc.
class Station(models.Model):
  name = models.CharField(max_length=256, help_text='A station name')
  place = models.CharField(max_length=256, help_text='A place where the station located')

# The most important class.
class Payment(models.Model):
  car = models.ForeignKey('Car', on_delete=models.CASCADE, help_text='A car for what the payment had been done')
  payment_type = models.ForeignKey('PaymentType', on_delete=models.CASCADE, help_text='A payment type')
  currency = models.ForeignKey('Currency', on_delete=models.CASCADE, help_text='A currency type of the payment')
  fuel_subtype = models.ForeignKey('FuelSubType', on_delete=models.CASCADE, null=True, help_text='Fuel subtype, 95, 92, Extra, etc.')
  station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, help_text='A station where payment had been made')

  amount = models.IntegerField(help_text='Money amount of the payment')
  date = models.CharField(max_length=64, help_text='A date of the payment. Should be ISO string', null=True)
  comment = models.TextField(help_text='A payment commenct', null=True)
  odometer = models.IntegerField(help_text='The car current odometer value when payment was made', null=True)
  fuel_price = models.IntegerField(help_text='A fuel price. Total price can be calculated automatically if it is a Fuel payment ', null=True)
  #  If fuel_price and this field presented - amount will be calculated automatically
  fuel_amount = models.IntegerField(help_text='An amount of the fuel (Litre).', null=True)