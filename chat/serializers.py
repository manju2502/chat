from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import NewUser, Chat, Message


class NewUserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = "__all__"


class ChatSerilaizer(serializers.ModelSerializer):
    members = serializers.ListField(label=_('Members'), write_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'name', 'members', 'created_at', 'created_by')

    def validate_members(self, members):
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
        fields = ("text", "sender", "chat")

    def create(self, validated_data):
        validated_data['chat'] = Chat.objects.get('id')
        validated_data['sender'] = self.context.get('user')
        return super().create(validated_data)
