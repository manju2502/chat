import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def _create_user(self, email, password, is_staff=False, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(email=self.normalize_email(email),
                          password=password,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    joining_date = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Abstract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Base(Abstract):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(NewUser, verbose_name=_('Created by'), on_delete=models.SET_NULL, editable=False,
                                   null=True, related_name="created_%(class)s_set")
    modified_by = models.ForeignKey(NewUser, verbose_name=_('Modified by'), on_delete=models.SET_NULL, editable=False,
                                    null=True, related_name="modified_%(class)s_set")

    class Meta:
        abstract = True


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


