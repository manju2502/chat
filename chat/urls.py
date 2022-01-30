from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
# from .views import ActivateView

from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # path(r"activate/<str:token>", ActivateView.as_view()),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
]