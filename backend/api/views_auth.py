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
from .models import User, UserManager, Live_register, Live_stream
import datetime

# ユーザ作成のView(POST)
class AuthRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ユーザ情報取得のView(GET)
class AuthInfoGetView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, format=None):

        live_alldata = Live_register.objects.filter(user=request.user).all()
        old_live_list = []
        new_live_list = []

        for live in live_alldata:
            live_streams = Live_stream.objects.filter(id=live.live.id)
            live_a = {}
            for stream in live_streams:
                live_a["title"] = stream.title
                live_a["started_at"] = stream.started_at
                print(datetime.date.today())
                print(stream.started_at)
                if stream.started_at < datetime.date.today():
                    old_live_list.append((live_a))
                else:
                    new_live_list.append(live_a)

        return Response(data={
            'username': request.user.username,
            'email': request.user.email,
            'profile': request.user.profile,
            'image_name': request.user.image_name,
            'data': request.user.data,
            'old_live_list': old_live_list,
            'new_live_list': new_live_list
            },
            status=status.HTTP_200_OK)

# ユーザ情報更新のView(PUT)
class AuthInfoUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer
    lookup_field = 'email'
    queryset = User.objects.all()

    def get(self, request, format=None):
        return Response(data={
            'username': request.user.username,
            'email': request.user.email,
            'profile': request.user.profile,
            },
            status=status.HTTP_200_OK)

    def get_object(self):
        try:
            instance = self.queryset.get(email=self.request.user)
            return instance
        except User.DoesNotExist:
            raise Http404


# ユーザー情報取得
class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        live_alldata = Live_register.objects.filter(user=user).all()
        old_live_list = []
        new_live_list = []

        for live in live_alldata:
            live_streams = Live_stream.objects.filter(id=live.live.id)
            live_a = {}
            for stream in live_streams:
                live_a["title"] = stream.title
                live_a["started_at"] = stream.started_at
                print(datetime.date.today())
                print(stream.started_at)
                if stream.started_at < datetime.date.today():
                    old_live_list.append((live_a))
                else:
                    new_live_list.append(live_a)

        return Response(data={
            'username': user.username,
            'email': user.email,
            'profile': user.profile,
            'image_name': user.image_name,
            'data': user.data,
            'old_live_list': old_live_list,
            'new_live_list': new_live_list
            },
            status=status.HTTP_200_OK)