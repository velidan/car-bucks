import graphene

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
        
      obj = cls._meta.model.objects.get(id=pk)
      return obj

    # in this case it will sillently return None without any error
    # is this behavior fine -  depends on our requirements
    #  print('pk =>> {pk}')
    #   try:
    #       obj = cls._meta.model.objects.get(id=pk)
    #       print(f'====>>>> obj {obj}')
    #       return obj
    #       # return obj if cls._meta.has_permission(obj, info.context.user) else None
    #   except cls._meta.model.DoesNotExist:
    #       print('None')
    #       return None

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