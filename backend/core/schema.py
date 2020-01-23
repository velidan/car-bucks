from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.models import ( Car, FuelType, FuelSubType, PaymentType,
        Currency, Station, Payment, )

class FuelTypeNode(DjangoObjectType):
  class Meta:
    model = FuelType
    filter_fields = ['code']
    interfaces = (relay.Node, )


class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeNode)
  all_fuel_types = DjangoFilterConnectionField(FuelTypeNode)