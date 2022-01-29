import graphene
from django.views.decorators import http
from graphene import relay, ObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType

from graphene_django.rest_framework.mutation import SerializerMutation
from .models import Chat, Message, NewUser
from .serializers import ChatConnection, MessageConnection, UserConnection, NewUserSerilaizer, NewUserType, MessageSerilaizer, MessageType, ChatSerilaizer, ChatType

#
# class Query(UserQuery, MeQuery, graphene.ObjectType):
#     pass
#
#
# class AuthMutation(graphene.ObjectType):
#     register = mutations.Register.Field()
#     verify_account = mutations.VerifyAccount.Field()
#     token_auth = mutations.ObtainJSONWebToken.Field()
#     update_account = mutations.UpdateAccount.Field()
#
#
# class Mutation(AuthMutation, graphene.ObjectType):
#     pass
#
#
# schema = graphene.Schema(query=Query, mutation=Mutation)


class Query(MeQuery, graphene.ObjectType):
    groups = relay.ConnectionField(ChatConnection)
    message = relay.ConnectionField(MessageConnection)
    user = relay.ConnectionField(UserConnection)

    # group = graphene.List(ChatType)
    # members = graphene.Field(NewUserType, id=graphene.Int())

    def resolve_groups(root, info, **kwargs):
        print(info.context.user)
        print(info)
        return Chat.objects.all()

    def resolve_user(root, info, **kwargs):
        return NewUser.objects.all()

    def resolve_message(root, info, **kwargs):
        return Message.objects.all()


#
# class UserMutation(SerializerMutation):
#     class Meta:
#         serializer_class = NewUserSerilaizer
#         model_operations = (
#             "create",
#             "update",
#             "delete",
#         )
#         lookup_field = 'id'
#
#
# class Mutation(graphene.ObjectType):
#     user_mutation = UserMutation.Field()

#
# class PostMessage(MeQuery, graphene.Mutation):
#     message = graphene.Field(MessageType)
#
#     class Arguments:
#         messages = graphene.String(required=True)
#         chat_id = graphene.String(required=True)
#
#     def mutate(cls, info, messages, _id=None):
#         user = info.context.user
#         print(user)
#         chat = Chat.objects.prefetch_related('members').get(members=user, id=_id)
#         print(_id, 'step1')
#         messages = Message.objects.create(
#             sender=user,
#             text=messages,
#         )
#         chat.messages.add(messages)
#         users = [usr for usr in chat.members.all() if usr != user]
#         for usr in users:
#             pass
#         return PostMessage(message=messages)
#
# class SenderInput(graphene.InputObjectType):
#     id = graphene.Int(),
#     username = graphene.String()
#
#
# class ChatInput(graphene.InputObjectType):
#     id = graphene.Int(),
#     name = graphene.String()
#
#
# class MessageInput(graphene.InputObjectType):
#     text = graphene.String(required=True)
#     sender = graphene.Field(SenderInput)
#     chat = graphene.Field(ChatInput)
#
#
# class PostMessage(graphene.Mutation):
#     message = graphene.Field(MessageType)
#
#     class Arguments:
#         message_data = MessageInput(required=True)
#
#     @staticmethod
#     def mutate(root, info, message_data):
#         message = Message.objects.create(**message_data)
#         return PostMessage(message=message)
#
#
# class Mutation(graphene.ObjectType):
#     post_message = PostMessage.Field()
#
#
# schema = graphene.Schema(mutation=Mutation)


# class PostMessage(graphene.Mutation):
#     message = graphene.Field(MessageType)
#
#     class Arguments:
#         chat_id = graphene.String(required=True)
#         message = graphene.String(required=True)
#
#     @classmethod
#     def mutate(cls, root, info, **kwargs):
#         serializer = MessageSerilaizer(data=kwargs)
#         if serializer.is_valid():
#             obj = serializer.save()
#         else:
#             obj = None
#         return cls(message=obj, status=200)

#
# class ChatMutation(MeQuery, SerializerMutation):
#     class Meta:
#         serializer_class = ChatSerilaizer
#         model_operations = (
#             "create",
#             "update",
#             "delete",
#         )
#         lookup_field = 'id'
#
#
# class Mutation(graphene.ObjectType):
#     chat_mutation = ChatMutation.Field()


schema = graphene.Schema(query=Query)
