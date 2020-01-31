import graphene
import django_filters
from django.db import models
from graphene import relay, ObjectType, Mutation, String, Field
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
    

class CreateFuelType(relay.ClientIDMutation):
  
  class Input:
    # The input arguments for this mutation
    code = String(required=True)
    label = String(required=True)

  ok = graphene.Boolean()

  # The class attributes define the response of the mutation
  fuel_type = Field(FuelTypeNode)

  def mutate_and_get_payload (root, info, input):
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
# --- ! Fuel SubType


class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeNode)
  all_fuel_types = DjangoFilterConnectionField(FuelTypeNode)

  fuel_sub_type = relay.Node.Field(FuelSubTypeNode)
  all_fuel_sub_types = DjangoFilterConnectionField(FuelSubTypeNode)