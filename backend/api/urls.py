from django.conf.urls import include, url
from rest_framework import routers
from .views import AuthRegister, AuthInfoGetView, AuthInfoUpdateView

urlpatterns = [
    url(r'^auth/users/$', AuthRegister.as_view()),
    url(r'^auth/me/$', AuthInfoGetView.as_view()),
    url(r'^auth/auth_update/$', AuthInfoUpdateView.as_view()),
]
