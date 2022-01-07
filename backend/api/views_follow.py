import logging

from django.contrib.auth import authenticate
from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from django.db.utils import IntegrityError
from django.http.response import Http404
from rest_framework import (
    authentication,
    filters,
    generics,
    permissions,
    status,
    viewsets,
)
from rest_framework.fields import CharField, IntegerField
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from api import errors
from api.models import Dm, Follow, Good, Live_register, Live_stream, User

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
        fields = ["id", "user", "user_id", "follow", "follow_id"]

    def create(self, validated_data):
        return User.objects.create_user(request_data=validated_data)


#
# BASIC_QUERYSET_FOLLOW = Follow.objects.annotate(
#     follows=Count("Follow")
# )


class FollowsRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def post(self, request, format=None):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
