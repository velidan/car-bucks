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
  pk = graphene.Int()
  label = graphene.String()

class FuelSubtypeInput(graphene.InputObjectType):
  pk = graphene.Int()
  label = graphene.String()
  # it's a fuel_type id
  fuel_type = graphene.Int()




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

class MutationRootOptions(graphene.types.objecttype.ObjectTypeOptions):
    model = None
    # has_permission = lambda obj, user: True

class MutationRoot(graphene.ObjectType):

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        interfaces=(),
        _meta=None,
        has_permission=None,
        **options
    ):
        if not _meta:
            _meta = MutationRootOptions(cls)
        _meta.model = model
        # _meta.has_permission = has_permission or (lambda obj, user: True)
        super(MutationRoot, cls).__init_subclass_with_meta__(
            _meta=_meta, interfaces=interfaces, **options
        )

    @classmethod
    def resolve(cls, root, info, pk=None):
      if cls._meta.model is None:
          return {}

      if pk is None:
          return getattr(root, cls._meta.model.__name__, {})
      try:
          obj = cls._meta.model.objects.get(id=pk)
          return obj
          # return obj if cls._meta.has_permission(obj, info.context.user) else None
      except cls._meta.model.DoesNotExist:
          return None

    @classmethod
    def Field(cls):
      return graphene.Field(cls, pk=graphene.ID(required=False), resolver=cls.resolve)

class MutationPayload(graphene.ObjectType):
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)
    query = graphene.Field('carbucks_engine.schema.Query', required=True)

    def resolve_ok(self, info):
        return len(self.errors or []) == 0

    def resolve_errors(self, info):
        return self.errors or []

    def resolve_query(self, info):
        return {}

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
def logger(fn):
    print('LOGGER')

    def fn_wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return fn_wrapper

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


    # # errors.append('some_error')
    # label = data.label
    # try:
    #   fuel_type = FuelType.objects.get(pk=data.fuel_type)
    # except:
    #   raise Exception('You need to pass the FuelType ID')

    # fuel_subtype = FuelSubType(label=label, fuel_type=fuel_type, errors=errors)
    # ok = True
    # fuel_subtype.save()
    # return CreateFuelSubType(fuel_subtype=fuel_subtype, ok=ok)



#!TeST


class CreateFuelSubType(relay.ClientIDMutation):
  fuel_subtype = Field(FuelSubTypeNode)
  ok = graphene.Boolean()

  class Input:
    data = FuelSubtypeInput(required=True)


  def mutate_and_get_payload(root, info, data):
    label = data.label
    try:
      fuel_type = FuelType.objects.get(pk=data.fuel_type)
    except:
      raise Exception('You need to pass the FuelType ID')

    fuel_subtype = FuelSubType(label=label, fuel_type=fuel_type, errors=errors)
    ok = True
    fuel_subtype.save()
    return CreateFuelSubType(fuel_subtype=fuel_subtype, ok=ok)


# --- Working update QUERY

"""
mutation MyMutations {
    updateFuelSubtype( input: { pk: 2, data : { label: "A test new FuelSubtype",
      fuelType: 3  } } ) {
    		__typename,
        fuelSubtype {
            label,
          	fuelType {
              label,
              id,
              code
            }
        }
    }
}
"""

class UpdateFuelSubType(relay.ClientIDMutation):
  fuel_subtype = Field(FuelSubTypeNode)

  class Input:
    pk = Int()
    data = FuelSubtypeInput(required=True)


  def mutate_and_get_payload(root, info, **input):
    pk = input.get('pk')
    data = input.get('data')

    fuel_type_pk = data.fuel_type

    # a quickfix how to remote the unnecessary attr. In general we have
    # data['fuel_type'], and data.fuel_type from the Relay...so we need to remove attr
    # otherwise they will overlap at the django ORM level
    del data['fuel_type']

    # print(f"data => {data.fuel_type}, attr =? {data['fuel_type']}")
    
    if fuel_type_pk != None:
      # if we are using get - it throws error on unexisting ID. need to try/except it
      fuel_type = get_object(FuelType, fuel_type_pk)
      if not fuel_type:
        # CustomError
        raise Exception('Invalid Fuel Type ID!')
      # replacing the input id type to the real Model
      data.fuel_type = fuel_type
    else:
      # need to remove unused fuel_type id
      del data.fuel_type


    try:
      fuel_subtype_inst = get_object(FuelSubType, pk) # get fuelsubtype by id
      
      if fuel_subtype_inst:
          # modify and update book model instance
          updated_fuel_subtype = update_create_instance(fuel_subtype_inst, data)
          #  return cls(updated_book=updated_book)
          return UpdateFuelSubType(fuel_subtype=updated_fuel_subtype)
    except ValidationError as e:
      # return an error if something wrong happens
      return UpdateFuelSubType(fuel_subtype=None, errors=get_errors(e))

# --- ! Fuel SubType


"""
mutation MyMutations {
  deleteFuelSubtype(input: { pk: 3 }) {
    ok
  }
}
"""
class DeleteFuelSubType(relay.ClientIDMutation):
  ok = graphene.Boolean()
  
  class Input:
    id = graphene.String()
    pk = graphene.Int()

  def mutate_and_get_payload(root, info, **input):
    pk = input.get('id', input.get('pk'))

    try:
      deleted_count = FuelSubType.objects.filter(id=pk).delete()[0]
      return DeleteFuelSubType(ok=True if deleted_count else False )
    except Exception as e:
      # return an error if something wrong happens
      return DeleteFuelSubType(ok=False, errors=get_errors(e))





class Query(ObjectType):
  fuel_type = relay.Node.Field(FuelTypeNode)
  
  all_fuel_types = ProtectedDjangoFilterConnectionField(FuelTypeNode)
  # all_fuel_types = DjangoFilterConnectionField(FuelTypeNode)
  # all_fuel_types = relay.ConnectionField(FuelTypeNode)
  
  # @login_required
  # def resolve_all_fuel_types(self, info):

  #   # context will reference to the Django request
  #   if not info.context.user.is_authenticated:
  #       return FuelType.objects.none()
  #   else:
  #       return FuelType.objects.all()

  fuel_sub_type = relay.Node.Field(FuelSubTypeNode)
  all_fuel_sub_types = DjangoFilterConnectionField(FuelSubTypeNode)

  