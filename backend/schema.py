import graphene
import graphql_jwt

from graphql_auth import mutations

import lend_app.schema
import accounts.schema


class AuthMutation(graphene.ObjectType):
#     register = mutations.Register.Field()
#     verify_account = mutations.VerifyAccount.Field()
#   resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
#     password_change = mutations.PasswordChange.Field()
#     update_account = mutations.UpdateAccount.Field()
#     archive_account = mutations.ArchiveAccount.Field()
#     delete_account = mutations.DeleteAccount.Field()
#     send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
#     verify_secondary_email = mutations.VerifySecondaryEmail.Field()
#     swap_emails = mutations.SwapEmails.Field()
#     remove_secondary_email = mutations.RemoveSecondaryEmail.Field()
#
#     # django-graphql-jwt inheritances
#     token_auth = mutations.ObtainJSONWebToken.Field()
#     verify_token = mutations.VerifyToken.Field()
#     refresh_token = mutations.RefreshToken.Field()
#     revoke_token = mutations.RevokeToken.Field()


class Query(lend_app.schema.Query, accounts.schema.Query, graphene.ObjectType):
    pass


class Mutation(lend_app.schema.Mutation, AuthMutation, accounts.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)