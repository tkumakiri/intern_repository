from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from api import views_directmessages
from . import views_auth, views_lives, views_posts, views_follow, views_goods

urlpatterns = [
    path('users/', views_auth.AuthRegister.as_view()),
    path('auth/me/', views_auth.AuthInfoGetView.as_view()),
    path('auth/auth_update/', views_auth.AuthInfoUpdateView.as_view()),
    path('users/<int:pk>/', views_auth.UserRetrieve.as_view()),
    path('lives', views_lives.LivesView.as_view()),
    path('lives/<int:pk>', views_lives.LiveView.as_view()),
    path('live_registrations', views_lives.LiveRegistrationView.as_view()),
    path('follows', views_follow.FollowsView.as_view()),
    path('follows/<int:pk>', views_follow.FollowView.as_view()),
    path('posts', views_posts.PostsView.as_view()),
    path('posts/<int:pk>', views_posts.PostView.as_view()),
    path('goods', views_goods.GoodsView.as_view()),
    path('goods/<int:pk>', views_goods.GoodView.as_view()),
    path('directmessages', views_directmessages.DirectMessagesView.as_view()),
    path('directmessages/<int:pk>', views_directmessages.DirectMessageView.as_view()),
]
