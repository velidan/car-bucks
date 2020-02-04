import graphene
from graphql import GraphQLError
import django_filters
from django.db import models
from graphene import relay, ObjectType, Mutation, Int, String, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from core.models import ( Car, FuelType, FuelSubType, PaymentType,
        Currency, Station, Payment, )

# --- Fuel Type ---
"""
Custom filter


query {
  allFuelTypes (codeMatch: "g") {
    edges {
      node {
        id,
        modelId,
        code,
        label
      }
    }
  }
}

allows to define some nice aliases for filter. Eg.code__Icontaints to codeMatch, or match
"""

class FuleTypeFilter(django_filters.FilterSet):
    """Filter for FuelType if contains filter queryset"""
    code_match = django_filters.CharFilter(field_name='code', method='filter_code_match')

    def filter_code_match(self, queryset, name, value):
      # construct the full lookup expression.
      lookup = '__'.join([name, 'icontains'])
      return queryset.filter(**{lookup: value})

      # alternatively, it may not be necessary to construct the lookup.
      # return queryset.filter(published_on__isnull=False) 

    class Meta:
        model = FuelType
        fields = ['code_match']

    # ---- Don't remove. For education purpose ----
    # # To redefine custom queryset to have a possibility to use custom manager
    # # etc. we need to override this method
    # def filter_queryset(self, queryset):
    #   a = FuelType.match_manager.match('g')
    #   # should return a list
    #   return list(a)

class FuelTypeNode(DjangoObjectType):
  class Meta:
    model = FuelType
    
    # use it when you want to use default django_filters
    # filter_fields = {
    #   'code': ['exact', 'icontains', 'istartswith'],
    # }

    # a custom Filter
    filterset_class = FuleTypeFilter
    interfaces = (relay.Node, )

  # need a custom id field alias because realy injects it's own `id` property
  model_id = Int()
  def resolve_model_id(self, info):
    # self is the selected model object
    return self.id
    

class CreateFuelType(relay.ClientIDMutation):
  
  class Input:
    # The input arguments for this mutation
    code = String(required=True)
    label = String(required=True)

  ok = graphene.Boolean()

  # The class attributes define the response of the mutation
  fuel_type = Field(FuelTypeNode)

  def mutate_and_get_payload(root, info, input):
    code = input['code']
    label = input['label']

    fuel_type = FuelType(code=code, label=label)
    ok = True
    return CreateFuelType(fuel_type=fuel_type, ok=ok)


# --- ! Fuel Type ---


# --- Fuel SubType ---
class FuelSubTypeNode(DjangoObjectType):
  class Meta:
    model = FuelSubType
    filter_fields = {
      'fuel_type__code': ['exact', 'icontains', 'istartswith'],
      'fuel_type__label': ['exact', 'icontains', 'istartswith'],
      'label': ['exact', 'icontains', 'istartswith'],
    }

    interfaces = (relay.Node, )

# Create Input Object Types
# class FuelTypeInput(graphene.InputObjectType):
#   id = graphene.Int()

#   # label = graphene.String()

class FuelSubtypeInput(graphene.InputObjectType):
  id = graphene.Int()
  label = graphene.String()
  # it's a fuel_type id
  fuel_type = graphene.Int()


# ---- working create query

# mutation MyMutations {
#     createFuelSubtype( input: { input : { label: "Mutation Subtype", fuelType: {
#       id: 3
#     }} } ) {
#         fuelSubtype {
#             label
#         }
#         ok
#     }
# }

# ---- !working create query


class CreateFuelSubType(relay.ClientIDMutation):
  class Input:
    input = FuelSubtypeInput(required=True)
    # label = String(required=True)
    # fuel_type_id = Int(required=True)

  fuel_subtype = Field(FuelSubTypeNode)
  ok = graphene.Boolean()

  def mutate_and_get_payload(root, info, input):
    label = input.label
    fuel_type = FuelType.objects.get(pk=input.fuel_type.id)
    print(f'fuel_type => {label} {fuel_type}')

    fuel_subtype = FuelSubType(label=label, fuel_type=fuel_type)
    ok = True
    fuel_subtype.save()
    return CreateFuelSubType(fuel_subtype=fuel_subtype, ok=ok)


# --- Working update QUERY

"""
mutation MyMutations {
    updateFuelSubtype(input: { id: 2, input: { label: "Updated 11 Mutation Label", 
      fuelType: 3 } }) {
    		__typename,
        fuelSubtype {
            label,
          	fuelType {
              label,
              id,
              modelId,
              code
            }
        }
    }
}
"""
class UpdateFuelSubType(relay.ClientIDMutation):
  fuel_subtype = Field(FuelSubTypeNode)

  class Input:
    id = Int()
    input = FuelSubtypeInput(required=True)


  def mutate_and_get_payload(root, info, id, input):
    fuel_subtype = None
  
    if input.fuel_type != None:
      # if we are using get - it throws error on unexisting ID. need to try/except it
      fuel_type = FuelType.objects.filter(pk=input.fuel_type).first()
      if not fuel_type:
        # CustomError
        raise Exception('Invalid Fuel Type ID!')
      # replacing the input id type to the real Model
      input.fuel_type = fuel_type
    else:
      del input.fuel_type
      # need to remove unused fuel_type id
    

    if FuelSubType.objects.filter(pk=id).update(**input):
      fuel_subtype = FuelSubType.objects.get(pk=id)
      # fuel_subtype.label = input.label
      # fuel_subtype.save()

    return UpdateFuelSubType(fuel_subtype=fuel_subtype)

# --- ! Fuel SubType



class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeNode)
  all_fuel_types = DjangoFilterConnectionField(FuelTypeNode)

  fuel_sub_type = relay.Node.Field(FuelSubTypeNode)
  all_fuel_sub_types = DjangoFilterConnectionField(FuelSubTypeNode)