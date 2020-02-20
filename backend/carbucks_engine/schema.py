import graphene
import graphql_jwt

import core.schema
import carbucks_engine.users.schema

from core.graphql_types import ( FuelTypeQL, FuelSubTypeQL )

class Query(
  core.schema.Query, 
  carbucks_engine.users.schema.Query, 
  graphene.ObjectType):
  # This class will inherit from multiple Queries
  # as we begin to add more apps to our project
  pass

class MyMutations(graphene.ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()
  delete_token = carbucks_engine.users.schema.DeleteJWTCookie.Field()

  create_user = carbucks_engine.users.schema.CreateUser.Field()

  create_fuel_type = FuelTypeQL.CreateFuelType.Field()

  # create_fuel_subtype = core.schema.CreateFuelSubType.Field()
  # update_fuel_subtype = core.schema.UpdateFuelSubType.Field()
  # delete_fuel_subtype = core.schema.DeleteFuelSubType.Field()

  fuel_subtype = FuelSubTypeQL.FuelSubTypeMutationRoot.Field()
  

schema = graphene.Schema(query=Query, mutation=MyMutations)
