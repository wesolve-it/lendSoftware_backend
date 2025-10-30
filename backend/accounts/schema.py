from django.db.models import Q

from .models import User

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.hashers import check_password


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    @staticmethod
    def mutate(root, info, email, password, first_name, last_name, username):
        user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class ChangeUsername(graphene.Mutation):
    ok = graphene.Boolean()
    username = graphene.String()

    class Arguments:
        username = graphene.String()

    @staticmethod
    def mutate(root, info, username=None):
        user_id = info.context.user.id
        ok = False
        user_instance = User.objects.get(pk=user_id)
        if user_instance:
            ok = True
            user_instance.username = username
            user_instance.save()
            return ChangeUsername(ok=ok, username=username)
        return ChangeUsername(ok=ok)


class ChangePassword(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        old_password = graphene.String()
        new_password = graphene.String()

    @staticmethod
    def mutate(root, info, old_password, new_password):
        user_id = info.context.user.id
        ok = False
        user_instance = User.objects.get(pk=user_id)
        if user_instance:
            if check_password(old_password, user_instance.password):
                ok = True
                user_instance.set_password(new_password)
                user_instance.save()
                return ChangePassword(ok=ok)
            return ChangePassword(ok=ok)
        return ChangePassword(ok=ok)


class ChangeEmail(graphene.Mutation):
    ok = graphene.Boolean()
    email = graphene.String()

    class Arguments:
        email = graphene.String()

    @staticmethod
    def mutate(root, info, email=None):
        user_id = info.context.user.id
        ok = False
        user_instance = User.objects.get(pk=user_id)
        if user_instance:
            ok = True
            user_instance.email = email
            user_instance.save()
            return ChangeEmail(ok=ok, email=email)
        return ChangeEmail(ok=ok)


class UpdateUser(graphene.Mutation):
    ok = graphene.Boolean()
    username = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    email = graphene.String()

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()

    @staticmethod
    def mutate(root, info, username=None, email=None, firstname=None, lastname=None):
        user_id = info.context.user.id
        ok = False
        user_instance = User.objects.get(pk=user_id)
        if user_instance:
            ok = True
            user_instance.firstname = firstname,
            user_instance.lastname = lastname,
            user_instance.username = username,
            user_instance.email = email
            user_instance.save()
            return UpdateUser(ok=ok, username=username, firstname=firstname, lastname=lastname, email=email)

        return UpdateUser(ok=ok)


class DeleteUser(graphene.Mutation):
    user_id = graphene.Int()
    deleted = graphene.Boolean()

    class Arguments:
        user_id = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, user_id):
        user = User.objects.get(id=user_id)
        print("DEBUG: ${user.id}")
        user.delete()

        return DeleteUser(
            deleted=True
        )


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    change_username = ChangeUsername.Field()
    change_email = ChangeEmail.Field()
    change_password = ChangePassword.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @staticmethod
    def resolve_users(root, info):
        return User.objects.all()

    @staticmethod
    def resolve_me(root, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user
