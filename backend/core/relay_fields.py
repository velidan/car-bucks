from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required


class ProtectedDjangoFilterConnectionField(DjangoFilterConnectionField):
    """
    An extended DjangoFilterConnectionFiled with the  login jwt_decorator
    """

    @classmethod
    @login_required
    def resolve_queryset(
    cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        return super().resolve_queryset(
            connection, iterable, info, args, filtering_args, filterset_class
        )
