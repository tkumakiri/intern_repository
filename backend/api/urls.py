from django.conf.urls import include, url
from rest_framework import routers
from .views import AuthRegister, AuthInfoGetView, AuthInfoUpdateView

urlpatterns = [
    url(r'^users/$', AuthRegister.as_view()),
    url(r'^me/$', AuthInfoGetView.as_view()),
    url(r'^auth_update/$', AuthInfoUpdateView.as_view()),
]
