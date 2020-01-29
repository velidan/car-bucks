from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser


# to have a possibility to change the User model in future if necessary
class User(AbstractUser):
    pass

class Car(models.Model):
  user = models.ForeignKey('User', 
    on_delete=models.CASCADE, 
    help_text='A car user.', 
    related_name='cars')
    

  model = models.CharField(max_length=256, help_text='A car model')
  engine_displacement = models.DecimalField(
    max_digits=4,
    blank=True, 
    null=True, 
    decimal_places=2, 
    help_text='An engine volume. Eg 2.2, 5.6 etc.')

  initial_odometer = models.IntegerField(blank=True, null=True, help_text='The car initial odometer')
  current_odometer = models.IntegerField(blank=True, null=True, help_text=('The car current odometer. ' + 
                                                    'Updates automatically at each payment when you fill the odometer field '))

  year = models.IntegerField(help_text='The car year')
  fuel_type = models.ForeignKey('FuelType', on_delete=models.CASCADE, help_text='A fuel type that your car use')

  def __str__(self):
    return self.model

  class Meta:
    ordering = ['id']    

class FuelType(models.Model):

  # django 3.0 + 
  # class TYPES(models.TextChoices):
  #       DIESEL = '0', 'Diesel'
  #       BENZIN = '1', 'Benzin'
  #       GAS = '2', 'Gas'

  # DIESEL_CODE = 0
  # BENZIN_CODE = 1
  # GAS_CODE = 2


  # FUEL_TYPES = (
  #   (DIESEL_CODE, 'Diesel'),
  #   (BENZIN_CODE, 'Benzin'),
  #   (GAS_CODE, 'Gas'),
  # )

  code = models.CharField(max_length=64, help_text='Fuel Type. Diesel | Benzing | Gas | Spiritus, etc. Short code for it')
  # code = models.CharField(max_length=64, choices=TYPES.choices, default=TYPES.DIESEL, help_text='Fuel Type. Diesel | Benzing | Gas | Spiritus, etc. Short code for it')

  label = models.CharField(max_length=256, help_text='A human readable label of the fuel type.')
  # fuel_type = models.CharField(choices=FUEL_TYPES, default=0)

  def __str__(self):
    return self.label

  class Meta:
    ordering = ['id']



class FuelSubType(models.Model):
  fuel_type = models.ForeignKey('FuelType', on_delete=models.CASCADE, help_text='A fuel subtype. Eg, benzin Extra | 95 | 92, etc.')

  label = models.CharField(max_length=256, help_text='A human readable label of the fuel subtype type.')

  def __str__(self):
    return self.label


class PaymentType(models.Model):
  label = models.CharField(max_length=256, help_text='Type of the payment. Eg, Fuel, Service, Card wash, others')

  def __str__(self):
    return self.label


class Currency(models.Model):

  code = models.CharField(max_length=3, help_text='A short currency code')
  label = models.CharField(max_length=86, help_text='A human-readable currency label')

  class Meta:
    verbose_name = 'Currency'
    verbose_name_plural = 'Currencies'

  def __str__(self):
    return self.label

# In general it's a fuel station, but could be a car wash/service station, etc.
class Station(models.Model):
  name = models.CharField(max_length=256, help_text='A station name')
  place = models.CharField(max_length=256, help_text='A place where the station located')

  def __str__(self):
    return f'Name:  {self.name}, Place: {self.place}' 

# The most important class.
class Payment(models.Model):
  car = models.ForeignKey('Car', on_delete=models.CASCADE, help_text='A car for what the payment had been done')
  payment_type = models.ForeignKey('PaymentType', on_delete=models.CASCADE, help_text='A payment type')
  currency = models.ForeignKey('Currency', on_delete=models.CASCADE, help_text='A currency type of the payment')
  fuel_type = models.ForeignKey('FuelType', 
    on_delete=models.CASCADE, 
    null=True, 
    help_text='Fuel type, Diesel, etc.', 
    blank=True)

  fuel_subtype = models.ForeignKey('FuelSubType', 
    on_delete=models.CASCADE, 
    null=True, 
    help_text='Fuel subtype, 95, 92, Extra, etc.', 
    blank=True)

  station = models.ForeignKey('Station',
    on_delete=models.SET_NULL,
    blank=True, 
    null=True, 
    help_text='A station where payment had been made')

  amount = models.DecimalField(max_digits=9, decimal_places=2, help_text='Money amount of the payment')
  date = models.DateField(help_text='A date of the payment. Should be ISO string', blank=True, null=True)
  comment = models.TextField(help_text='A payment commenct', blank=True, null=True)
  odometer = models.IntegerField(help_text='The car current odometer value when payment was made', 
    blank=True, 
    null=True)
  fuel_price = models.DecimalField(
    max_digits=5, 
    decimal_places=2, 
    help_text='A fuel price. Total price can be calculated automatically if it is a Fuel payment ',
    blank=True,
    null=True)
  #  If fuel_price and this field presented - amount will be calculated automatically
  fuel_amount = models.DecimalField(
    max_digits=9, 
    decimal_places=2, 
    help_text='An amount of the fuel (Litre).', 
    blank=True, 
    null=True)

  def __str__(self):
    return f'Car: {self.car}, Type: {self.payment_type}, Amount: {self.amount}'