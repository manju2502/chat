from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import *
from graphene_django import DjangoObjectType
from graphene import relay, ObjectType
from datetime import datetime


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


class NewUserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = "__all__"


class ChatSerilaizer(serializers.ModelSerializer):
    members = serializers.ListField(label=_('Members'), write_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'name', 'members', 'created_at')

    def validate_members(self, members):
        print(self)
        # print(self.context.get('user'))
        data = []
        for member in members:
            try:
                data.append(NewUser.objects.get(id=member))
            except NewUser.DoesNotExist:
                return serializers.ValidationError(_(f'User does not exist!'))

        return set(data)

    # def update(self, instance, validated_data):
    #     jd = dict()
    #     for member in instance.members.all():
    #         jd.update({'joining_date':[member.joining_date]})
    #     print(jd)
    #     print(jd['joining_date'])
    #     jd['joining_date'] = datetime.now()
    #     print(jd['joining_date'])
    #     NewUser.objects.update(joining_date=jd['joining_date'])

        # for i in jd:
        #     print(i)
        #     i.datetime.now()
        #     print(i)
        #obj = NewUser.objects.update(joining)
        # pass


class MessageSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


