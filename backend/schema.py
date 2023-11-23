import graphene

import lend_app.schema


class Query(lend_app.schema.Query, graphene.ObjectType):
    pass


class Mutation(lend_app.schema.Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)