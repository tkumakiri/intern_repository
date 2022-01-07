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

# DMのAPI
class DirectmessagesView(generics.UpdateAPIView):
    serializer_class = DmSerializer
    queryset = Dm.objects.all()

    def get(self, request):
        # ログインしていない
        if :
            return Response(data={
            {
              "code": 1001,
              "error": "no active user"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 自分ではないユーザー ID が central に指定
        elif :
            return Response(data={
            {
              "code": 4003,
              "error": "invalid central specified"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # central とtarget の間に一切 FF (フォロー) 関係がない
        elif :
            return Response(data={
            {
              "code": 4004,
              "error": "no ff relation between central and target"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={
                'id': self.id,
                "sender": {
                  'username': request.central.username,
                  'email': request.central.email,
                  'profile': request.central.profile,
                  },
                'id': self.id,
                "receiver": {
                  'username': request.target.username,
                  'email': request.target.email,
                  'profile': request.target.profile,
                  },
                "sent_at": request.target.sent_at
                },
                status=status.HTTP_200_OK)

    def post(self, request):
        # 送信先のユーザーが存在しない
        if User.DoesNotExist:
            return Response(data={
            {
              "code": 4001,
              "error": "invalid receiver user"
            },
            status=status.HTTP_404_NOT_FOUND)
        # ログインしていない
        elif:
            return Response(data={
            {
              "code": 1001,
              "error": "no active user"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 自分ではないユーザー ID から送信しようとした
        elif:
            return Response(data={
            {
              "code": 4000,
              "error": "invalid sender specified"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        # 送信先のユーザーをフォローしていない
        elif:
            return Response(data={
            {
              "code": 4002,
              "error": "receiver not followed by sender"
            },
            status=status.HTTP_401_UNAUTHORIZED)
        else:
            created = Dm.objects.get_or_create(text=text, sender=sender, sent_at=sent_at, receiver=receiver)
            return Response(data={
                'id': self.id,
                "sender": {
                  'username': request.sender_id.username,
                  'email': request.sender_id.email,
                  'profile': request.sender_id.profile,
                  },
                'id': self.id,
                "receiver": {
                  'username': request.receiver_id.username,
                  'email': request.receiver_id.email,
                  'profile': request.receiver_id.profile,
                  },
                "sent_at": request.receiver_id.sent_at
                },
                status=status.HTTP_201_CREATED)

