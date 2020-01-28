import graphene

import core.schema

class Query(core.schema.Query, graphene.ObjectType):
  # This class will inherit from multiple Queries
  # as we begin to add more apps to our project
  pass

class MyMutations(graphene.ObjectType):
  create_fuel_type = core.schema.CreateFuelType.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations)
