import graphene
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
class FuelTypeInput(graphene.InputObjectType):
    id = graphene.Int()
    label = graphene.String()
class FuelSubtypeInput(graphene.InputObjectType):
    id = graphene.ID()
    label = graphene.String()
    fuel_type = graphene.Field(FuelTypeInput)


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


class UpdateFuelSubType(relay.ClientIDMutation):
  class Input:
    id = Int()
    input = FuelSubtypeInput(required=True)

  ok = True
  fuel_subtype = Field(FuelSubTypeNode)

  def mutate_and_get_payload(root, info, id, input):
    ok = False
    # fuel_subtype = FuelSubType.objects.get(pk=id)

    
    
    

    if FuelSubType.objects.filter(pk=id).update(**input):
      fuel_subtype = FuelSubType.objects.get(pk=id)
      ok = True
      # fuel_subtype.label = input.label
      # fuel_subtype.save()

      return UpdateFuelSubType(fuel_subtype=fuel_subtype)

    return UpdateFuelSubType(fuel_subtype=None)

# --- ! Fuel SubType


class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeNode)
  all_fuel_types = DjangoFilterConnectionField(FuelTypeNode)

  fuel_sub_type = relay.Node.Field(FuelSubTypeNode)
  all_fuel_sub_types = DjangoFilterConnectionField(FuelSubTypeNode)