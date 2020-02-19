from django.contrib.auth import get_user_model
from graphene import relay, ObjectType, String, Field, Boolean, List
from graphene_django import DjangoObjectType

from django.contrib.auth import logout


class UserTypeNode(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(relay.ClientIDMutation):
    user = Field(UserTypeNode)
    ok = Boolean()

    class Input:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)

    def mutate_and_get_payload(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        ok = True
        return CreateUser(user=user, ok = True)



class DeleteJWTCookie(relay.ClientIDMutation):
    """
    a direct implementation of the graphene-jwt package delete cookie method
    because it's removed from the package somehow.

    this we are setting the delete_jwt_cookie boolean to True
    and jwt_cookie in the urls.py will detect it and remove the cookie
    """
    deleted = Boolean(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        context = info.context

        context.delete_jwt_cookie = (
            'JWT' in context.COOKIES and
            getattr(context, 'jwt_cookie', False)
        )

        return cls(deleted=context.delete_jwt_cookie)

class Query(ObjectType):
    me = Field(UserTypeNode)
    users = List(UserTypeNode)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user