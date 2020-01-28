import graphene
from graphene import relay, ObjectType, Mutation, String, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.models import ( Car, FuelType, FuelSubType, PaymentType,
        Currency, Station, Payment, )

class FuelTypeNode(DjangoObjectType):
  class Meta:
    model = FuelType
    filter_fields = {
      'code': ['exact', 'icontains', 'istartswith'],
    }
    interfaces = (relay.Node, )

class CreateFuelType(Mutation):
  class Arguments:
    # The input arguments for this mutation
    code = String(required=True)
    label = String(required=True)

  ok = graphene.Boolean()

  # The class attributes define the response of the mutation
  fuel_type = Field(FuelTypeNode)

  def mutate(self, info, code, label):
    fuel_type = FuelType(code=code, label=label)
    ok = True
    return CreateFuelType(fuel_type=fuel_type, ok=ok)



class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeNode)
  all_fuel_types = DjangoFilterConnectionField(FuelTypeNode)