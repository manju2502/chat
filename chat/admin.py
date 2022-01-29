from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import NewUser, Chat, Message

admin.site.register(NewUser)
admin.site.register(Chat)
admin.site.register(Message)

app = apps.get_app_config('graphql_auth')


for model_name, model in app.models.items():
    admin.site.register(model)


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {'fields': ('user_name', 'first_name', 'email', 'joining_date'
                           'is_active', 'verified')}),
    )

