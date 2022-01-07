from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializer import AccountSerializer
from .models import User, Dm, Follow, Good

# FFのAPI
class FollowsView(generics.UpdateAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def followers(self, request):
        follower = request.user
        following = self.get_object()
        # userまたはtargetに指定されたユーザーが見つからない
        if follower.DoesNotExist or following.DoesNotExist:
            return Response(data={
            {
              "code": 6002,
              "error": "user not found"
            },
            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={
                'id': self.id,
                "user": {
                  'username': request.user.username,
                  'email': request.user.email,
                  'profile': request.user.profile,
                  }
                "target": {
                  'username': request.target.username,
                  'email': request.target.email,
                  'profile': request.target.profile,
                  }
                },
                status=status.HTTP_200_OK)

    def follow(self, request):
        follower = request.user
        following = self.get_object()
        # ログインしていない
        if :
            return Response(data={
            {
              "code": 1001,
              "error": "no active user"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 自分ではないユーザーからフォローしようとした
        elif:
            return Response(data={
            {
              "code": 6001,
              "error": "invalid user specified"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 対称となるユーザーが見つからない
        elif Follow.DoesNotExist:
            return Response(data={
            {
              "code": 6002,
              "error": "user not found"
            },
            status=status.HTTP_404_NOT_FOUND)
        # すでにフォローしている人をフォローしようとした
        elif:
            return Response(data={
            {
              "code": 6000,
              "error": "already followed"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # フォローする処理をして201を返す
        else:
            created = Follow.objects.get_or_create(user=follower, follow=following)
            return Response(data={
                'id': self.id,
                "sender": {
                  'username': request.user_id.username,
                  'email': request.user_id.email,
                  'profile': request.user_id.profile,
                  },
                'id': self.id,
                "receiver": {
                  'username': request.target_id.username,
                  'email': request.target_id.email,
                  'profile': request.target_id.profile,
                  },
                "sent_at": request.target_id.sent_at
                },
                status=status.HTTP_201_CREATED)

    def unfollow(self, request):
        follower = request.user
        following = self.get_object()
        # ログインしていない
        if :
            return Response(data={
            {
              "code": 1001,
              "error": "no active user"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 他人がしたフォローを削除しようとした
        elif:
            return Response(data={
            {
              "code": 6002,
              "error": "specified follow is not created by user"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 解除するフォローが見つからない
        elif Follow.DoesNotExist:
            return Response(data={
            {
              "code": 6004,
              "error": "follow not found"
            },
        status=status.HTTP_404_NOT_FOUND)
        # フォロー解除して200を返す
        else:
            Follow.objects.get(user=follower, follow=following).delete()
            return Response(data={
                'id': self.id,
                "sender": {
                },
                status=status.HTTP_200_OK)
