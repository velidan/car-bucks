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


