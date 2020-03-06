import graphene
from graphql import GraphQLError
import django_filters
from django.db import models
from graphene import relay, ObjectType, Mutation, Int, String, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError

from core.relay_fields import ProtectedDjangoFilterConnectionField

from core.models import ( Car, FuelType, FuelSubType, PaymentType,
        Currency, Station, Payment, )

from core.helpers import get_object, update_create_instance, get_errors

from core.graphql_mutations import (MutationRootOptions, MutationRoot, MutationPayload)


class FuelSubTypeNode(DjangoObjectType):
  class Meta:
    model = FuelSubType
    filter_fields = {
      'fuel_type__code': ['exact', 'icontains', 'istartswith'],
      'fuel_type__label': ['exact', 'icontains', 'istartswith'],
      'label': ['exact', 'icontains', 'istartswith'],
    }

    interfaces = (relay.Node, )

    # need a custom id field alias because realy injects it's own `id | pk` property
  pk = Int()
  def resolve_model_pk(self, info):
    # self is the selected model object
    return self.id

# Create Input Object Types

class FuelSubtypeInput(graphene.InputObjectType):
  pk = graphene.Int()
  label = graphene.String()
  # it's a fuel_type id
  fuel_type = graphene.Int()



"""
mutation MuMutations {
  fuelSubtype {
    create(input: { data: { label: "E-95", fuelType: 1} } ) {
      ok,
      errors,
      query {
        allFuelSubTypes {
          edges {
            node {
              id,
              label
            }
          }
        }
      }
    }
  }
}

"""

class CreateFuelSubTypeChildMut(MutationPayload, relay.ClientIDMutation):
  # fuel_subtype = Field(FuelSubTypeNode)
  # ok = graphene.Boolean()

  class Input:
    data = FuelSubtypeInput(required=True)


  def mutate_and_get_payload(_, info, data):
    errors = []

    # it's a child mutation so the fuelSubtype will be a first arg
    label = data.label

    if len(label) < 2:
      errors.append('label_too_short')

    if FuelSubType.objects.filter(label=label).exists():
      errors.append('label_already_taken')

    try:
      fuel_type = FuelType.objects.get(pk=data.fuel_type)
    except:
      errors.append('invalid_fuel_type')

    if not errors:
      fuel_subtype = FuelSubType(label=label, fuel_type=fuel_type)
      fuel_subtype.save()

    return CreateFuelSubTypeChildMut(errors=errors)

"""
Working
mutation MyMutations {
  fuelSubtype(pk: 1) {
    update(input: { data: { label: "Shell V-Power", fuelType: 2 } }) {
			ok,
      errors,
      query {
        allFuelSubTypes {
        	edges {
            node {
              id,
              label,
            }
          }
        }
      }
		}
  }
}
"""
class UpdateFuelSubTypeChildMut(MutationPayload, relay.ClientIDMutation):
  class Input:
    data = FuelSubtypeInput(required=True)


  def mutate_and_get_payload(fuelSubType, info, data):
    # it's a child mutation so the fuelSubtype will be a first arg
    errors = []

    if fuelSubType is None:
      return None
    
    label = data.label

    if len(label) < 2:
      errors.append('label_too_short')

    if FuelSubType.objects.filter(label=label).exists():
      errors.append('label_already_taken')
    

    fuel_type_pk = data.fuel_type

    # a quickfix how to remote the unnecessary attr. In general we have
    # data['fuel_type'], and data.fuel_type from the Relay...so we need to remove attr
    # otherwise they will overlap at the django ORM level
    del data['fuel_type']

    if fuel_type_pk != None:
      # if we are using get - it throws error on unexisting ID. need to try/except it
      fuel_type = get_object(FuelType, fuel_type_pk)
      if not fuel_type:
        # CustomError
        # raise Exception('Invalid Fuel Type ID!')
        errors.append('fuel_type_invalid_id')
      # replacing the input id type to the real Model
      data.fuel_type = fuel_type
    else:
      # need to remove unused fuel_type id
      del data.fuel_type

    if not errors:
        updated_fuel_subtype = update_create_instance(fuelSubType, data)

    return UpdateFuelSubTypeChildMut(errors=errors)



"""
mutation MyMutations {
  fuelSubtype(pk: 4) {
    delete {
      ok,
      errors,
    }
  }
}

"""
class DeleteFuelSubTypeChildMut(MutationPayload, Mutation):

  def mutate(fuelSubType, info):
    errors = []
    try:
      fuelSubType.delete()
    except Exception as e:
      # return an error if something wrong happens
      errors.append('cant_delete_fuel_subtype')

    return DeleteFuelSubTypeChildMut(errors)


class FuelSubTypeMutationRoot(MutationRoot):

    class Meta:
        model = FuelSubType

    create = CreateFuelSubTypeChildMut.Field()
    update = UpdateFuelSubTypeChildMut.Field()
    delete = DeleteFuelSubTypeChildMut.Field()
