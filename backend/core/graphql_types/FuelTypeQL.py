import graphene
from graphql import GraphQLError
import django_filters
from django.db import models
from graphene import relay, ObjectType, Mutation, Int, String, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError

from core.models import FuelType

# is it in use?
class FuelTypeInput(graphene.InputObjectType):
  pk = graphene.Int()
  label = graphene.String()

# --- Fuel Type ---
"""
Custom filter


query {
  allFuelTypes (codeMatch: "g") {
    edges {
      node {
        id,
        pk,
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

  # need a custom id field alias because realy injects it's own `id | pk` property
  pk = Int()
  def resolve_model_pk(self, info):
    # self is the selected model object
    return self.id
    
"""
mutation MyMutations {
  createFuelType(input: { code: "z", label: "Zeta" }) {
    __typename,
    ok,
    fuelType {
      id,
      pk,
      label,
      code
    }
    
  }
}

"""

class CreateFuelType(relay.ClientIDMutation):
  
  class Input:
    # The input arguments for this mutation
    code = String(required=True)
    label = String(required=True)

  ok = graphene.Boolean()

  # The class attributes define the response of the mutation
  fuel_type = Field(FuelTypeNode)

  def mutate_and_get_payload(root, info, **input):
    code = input.get('code')
    label = input.get('label')

    fuel_type = FuelType(code=code, label=label)
    ok = True
    return CreateFuelType(fuel_type=fuel_type, ok=ok)


# --- ! Fuel Type ---