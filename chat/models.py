import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Abstract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Base(Abstract):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('chat.NewUser', verbose_name=_('Created by'), on_delete=models.SET_NULL, editable=False,
                                   null=True, related_name="created_%(class)s_set")
    modified_by = models.ForeignKey('chat.NewUser', verbose_name=_('Modified by'), on_delete=models.SET_NULL, editable=False,
                                    null=True, related_name="modified_%(class)s_set")

    class Meta:
        abstract = True


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, username):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def __str__(self):
        return self.email

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def __str__(self):
        return self.email


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    joining_date = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.username


class Chat(Base):
    name = models.CharField(_('Name'), max_length=50, blank=True)
    members = models.ManyToManyField(NewUser, verbose_name='Members', related_name='chats', related_query_name='chat')

    class Meta:
        db_table = 'chat'
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ('-modified_at',)

    def __str__(self):
        return self.name


class Message(Base):
    chat = models.ForeignKey(Chat, verbose_name=_('Chat'), related_name='messages', related_query_name='message', on_delete=models.CASCADE)
    sender = models.ForeignKey(NewUser, verbose_name=_('Sender'), related_name='messages', related_query_name='message', on_delete=models.CASCADE)
    text = models.TextField(_('Text'), blank=True)

    class Meta:
        db_table = 'message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-created_at',)

    def __str__(self):
        return self.chat.name


