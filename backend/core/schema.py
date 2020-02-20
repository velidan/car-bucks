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

from core.graphql_types import (
  FuelTypeQL, FuelSubTypeQL
)


# --- Fuel SubType ---




# ---- working create query

"""
mutation MyMutations {
 createFuelSubtype( input: { data: { label: "Another new Subtype", fuelType: 2 } } ) {
		__typename,
		fuelSubtype {
      label,
      fuelType {
        label,
        id,
        pk,
        code
      }
    }
  }
}
"""

# ---- !working create query

# TEST






# class CreateFuelSubType(relay.ClientIDMutation):
#   fuel_subtype = Field(FuelSubTypeNode)
#   ok = graphene.Boolean()

#   class Input:
#     data = FuelSubtypeInput(required=True)


#   def mutate_and_get_payload(root, info, data):
#     label = data.label
#     try:
#       fuel_type = FuelType.objects.get(pk=data.fuel_type)
#     except:
#       raise Exception('You need to pass the FuelType ID')

#     fuel_subtype = FuelSubType(label=label, fuel_type=fuel_type, errors=errors)
#     ok = True
#     fuel_subtype.save()
#     return CreateFuelSubType(fuel_subtype=fuel_subtype, ok=ok)


# # --- Working update QUERY

# """
# mutation MyMutations {
#     updateFuelSubtype( input: { pk: 2, data : { label: "A test new FuelSubtype",
#       fuelType: 3  } } ) {
#     		__typename,
#         fuelSubtype {
#             label,
#           	fuelType {
#               label,
#               id,
#               code
#             }
#         }
#     }
# }
# """

# class UpdateFuelSubType(relay.ClientIDMutation):
#   fuel_subtype = Field(FuelSubTypeNode)

#   class Input:
#     pk = Int()
#     data = FuelSubtypeInput(required=True)


#   def mutate_and_get_payload(root, info, **input):
#     pk = input.get('pk')
#     data = input.get('data')

#     fuel_type_pk = data.fuel_type

#     # a quickfix how to remote the unnecessary attr. In general we have
#     # data['fuel_type'], and data.fuel_type from the Relay...so we need to remove attr
#     # otherwise they will overlap at the django ORM level
#     del data['fuel_type']

#     # print(f"data => {data.fuel_type}, attr =? {data['fuel_type']}")
    
#     if fuel_type_pk != None:
#       # if we are using get - it throws error on unexisting ID. need to try/except it
#       fuel_type = get_object(FuelType, fuel_type_pk)
#       if not fuel_type:
#         # CustomError
#         raise Exception('Invalid Fuel Type ID!')
#       # replacing the input id type to the real Model
#       data.fuel_type = fuel_type
#     else:
#       # need to remove unused fuel_type id
#       del data.fuel_type


#     try:
#       fuel_subtype_inst = get_object(FuelSubType, pk) # get fuelsubtype by id
      
#       if fuel_subtype_inst:
#           # modify and update book model instance
#           updated_fuel_subtype = update_create_instance(fuel_subtype_inst, data)
#           #  return cls(updated_book=updated_book)
#           return UpdateFuelSubType(fuel_subtype=updated_fuel_subtype)
#     except ValidationError as e:
#       # return an error if something wrong happens
#       return UpdateFuelSubType(fuel_subtype=None, errors=get_errors(e))

# # --- ! Fuel SubType


# """
# mutation MyMutations {
#   deleteFuelSubtype(input: { pk: 3 }) {
#     ok
#   }
# }
# """
# class DeleteFuelSubType(relay.ClientIDMutation):
#   ok = graphene.Boolean()
  
#   class Input:
#     id = graphene.String()
#     pk = graphene.Int()

#   def mutate_and_get_payload(root, info, **input):
#     pk = input.get('id', input.get('pk'))

#     try:
#       deleted_count = FuelSubType.objects.filter(id=pk).delete()[0]
#       return DeleteFuelSubType(ok=True if deleted_count else False )
#     except Exception as e:
#       # return an error if something wrong happens
#       return DeleteFuelSubType(ok=False, errors=get_errors(e))





class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeQL.FuelTypeNode)
  
  all_fuel_types = ProtectedDjangoFilterConnectionField(FuelTypeQL.FuelTypeNode)

  fuel_sub_type = relay.Node.Field(FuelSubTypeQL.FuelSubTypeNode)
  all_fuel_sub_types = DjangoFilterConnectionField(FuelSubTypeQL.FuelSubTypeNode)

  