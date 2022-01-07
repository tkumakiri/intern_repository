from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from .views import AuthRegister, AuthInfoGetView, AuthInfoUpdateView, UserRetrieve

urlpatterns = [
    path('users/', AuthRegister.as_view()),
    path('auth/me/', AuthInfoGetView.as_view()),
    path('auth/auth_update/', AuthInfoUpdateView.as_view()),
    path('users/<int:pk>/', UserRetrieve.as_view()),

]
