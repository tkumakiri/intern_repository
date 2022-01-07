from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from .views import AuthRegister, AuthInfoGetView, AuthInfoUpdateView, UserRetrieve
from .views_dm import DirectmessagesView
from .views_follow import FollowsView

urlpatterns = [
    path('users/', AuthRegister.as_view()),
    path('auth/me/', AuthInfoGetView.as_view()),
    path('auth/auth_update/', AuthInfoUpdateView.as_view()),
    path('users/<int:pk>/', UserRetrieve.as_view()),
    url(r'^auth/auth_update/$', AuthInfoUpdateView.as_view()),
    url(r'^directmessages/$', DirectmessagesView.as_view()),
    url(r'^follows/$', FollowsView.as_view()),
]
