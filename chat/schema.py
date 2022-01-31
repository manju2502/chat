import graphene
from graphene import relay, ObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphene_django import DjangoObjectType

from graphene_django.rest_framework.mutation import SerializerMutation
from .models import Chat, Message, NewUser
from .serializers import NewUserSerilaizer, MessageSerilaizer, ChatSerilaizer


# class Query(UserQuery, MeQuery, graphene.ObjectType):
#     pass

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


class NewUserType(DjangoObjectType):
    class Meta:
        model = NewUser
        fields = "__all__"
        interfaces = (relay.Node, )


class ChatType(DjangoObjectType):
    class Meta:
        model = Chat
        fields = "id", "name", "members", "created_at"
        interfaces = (relay.Node, )


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = "__all__"
        interfaces = (relay.Node, )


class ChatConnection(relay.Connection):
    class Meta:
        node = ChatType


class UserConnection(relay.Connection):
    class Meta:
        node = NewUserType


class MessageConnection(relay.Connection):
    class Meta:
        node = MessageType


class Query(MeQuery, graphene.ObjectType):
    groups = relay.ConnectionField(ChatConnection)
    message = relay.ConnectionField(MessageConnection)
    user = relay.ConnectionField(UserConnection)

    # group = graphene.List(ChatType)
    # members = graphene.Field(NewUserType, id=graphene.Int())

    def resolve_groups(root, info, **kwargs):
        return Chat.objects.all()

    def resolve_user(root, info, **kwargs):
        return NewUser.objects.all()

    def resolve_message(root, info, **kwargs):
        return Message.objects.all()

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


class MessageMutation(SerializerMutation):
    class Meta:
        serializer_class = MessageSerilaizer
        model_operations = (
            "create",
            "update",
            "delete",
        )
        lookup_field = 'id'


class ChatMutation(SerializerMutation):
    class Meta:
        serializer_class = ChatSerilaizer
        model_operations = (
            "create",
            "update",
            "delete",
        )
        lookup_field = 'id'


class UserMutation(SerializerMutation):
    class Meta:
        serializer_class = NewUserSerilaizer
        model_operations = (
            "create",
            "update",
            "delete",
        )
        lookup_field = 'id'


class Mutation(graphene.ObjectType):
    chat_mutation = ChatMutation.Field()
    user_mutation = UserMutation.Field()
    post_message = MessageMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
