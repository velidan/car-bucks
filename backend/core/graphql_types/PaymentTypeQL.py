import graphene
from graphene import relay, Mutation
from graphql import GraphQLError
from graphene_django import DjangoObjectType


from core.models import PaymentType

from core.graphql_mutations import (MutationRootOptions, MutationRoot, MutationPayload)
from core.helpers import get_object, update_create_instance

class PymentTypeInput(graphene.InputObjectType):
  pk = graphene.Int()
  label = graphene.String()

class PaymentTypeNode(DjangoObjectType):

  class Meta:
    model = PaymentType
    filter_fields = []

    interfaces = (relay.Node, )

  pk = graphene.Int()

  def resolve_model_pk(self, info):
    # self is the selected model object
    return self.id


class CreatePaymentTypeChildMut(MutationPayload, relay.ClientIDMutation):

  class Input:
    # the input argument for this mutation
    data = PymentTypeInput(required=True)

  def mutate_and_get_payload(_, info, data):
    errors = []

    label = data.label

    # TODO: the same logic in the FuelSUbtype. Optimization required
    if len(label) < 2:
      errors.append('label_too_short')

    if PaymentType.objects.filter(label=label).exists():
      errors.append('label_already_taken')

    if not errors:
      payment_type = PaymentType(label=label)
      payment_type.save()

    return CreatePaymentTypeChildMut(errors=errors)

  
class UpdatePaymentTypeChildMut(MutationPayload, relay.ClientIDMutation):

  class Input:
    # the input argument for this mutation
    data = PymentTypeInput(required=True)


  def mutate_and_get_payload(paymentType, info, data):
    # the paymentType will be a first arg
    errors = []

    if paymentType is None:
      return None

    label = data.label

    if len(label) < 2:
      errors.append('label_too_short')

    if PaymentType.objects.filter(label=label).exists():
      errors.append('label_already_taken')

    if not errors:
        updated_fuel_subtype = update_create_instance(paymentType, data)

    return UpdatePaymentTypeChildMut(errors=errors)


class DeletePaymentTypeChildMut(MutationPayload, Mutation):

  def mutate(paymentType, info):
    errors = []

    try:
      PaymentType.delete()
    except Exception as e:
      # return an error if something wrong happens
      errors.append('cant_delete_payment_type')

    return DeletePaymentTypeChildMut(errors)

class PaymentTypeMutationRoot(MutationRoot):

    class Meta:
        model = PaymentType

    create = CreatePaymentTypeChildMut.Field()
    update = UpdatePaymentTypeChildMut.Field()
    delete = DeletePaymentTypeChildMut.Field()