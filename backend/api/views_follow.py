from django.contrib.auth import authenticate
import logging

from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from django.db.utils import IntegrityError
from django.http.response import Http404
from rest_framework.fields import CharField, IntegerField
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework import authentication, permissions, generics


from api import errors
from api.models import Live_register, Live_stream, User, Dm, Follow, Good
from .serializer import AccountSerializer

LOGGER = logging.getLogger("django")

class FollowSerializer(ModelSerializer):
    user = AccountSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    follow = AccountSerializer(read_only=True)
    follow_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Follow
        fields = ["id", "user", "follow"]
#
# BASIC_QUERYSET_FOLLOW = Follow.objects.annotate(
#     follows=Count("Follow")
# )

class FollowsRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = FollowSerializer

    def post(self, request, format=None):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 自分のフォローを一覧
class FollowsView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # queryset = User.objects.all()
    serializer_class = FollowSerializer

    def get(self, request, format=None):

        live_alldata = Live_register.objects.filter(user=request.user).all()
        old_live_list = []
        new_live_list = []


        return Response(data={
            'username': request.user.username,
            },
            status=status.HTTP_200_OK)







# # 特定のユーザーのフォロー情報を取得する
# class FollowView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = LiveSerializer
#     queryset = BASIC_QUERYSET_FOLLOW.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         try:
#             return super().retrieve(request, *args, **kwargs)
#         except Http404:
#             return errors.not_found_response(f"follow of id {kwargs['pk']}")

