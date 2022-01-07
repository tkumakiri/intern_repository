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
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from api import errors, views_lives
from api.models import Dm, Follow, Good, Live_register, Live_stream, User

from .serializer import AccountSerializer

LOGGER = logging.getLogger("django")


class FollowSerializer(ModelSerializer):
    user = views_lives.UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    target = views_lives.UserSerializer(read_only=True, source="follow")
    target_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Follow
        fields = ["id", "user", "user_id", "target", "target_id"]
        depth = 1

    def create(self, validated_data):
        resolve(validated_data, "user_id", "user")
        resolve(validated_data, "target_id", "follow")
        return super().create(validated_data)


def resolve(validated_data, id_field, entity_field):
    resolved = validated_data.get(id_field)
    if resolved is not None:
        validated_data[entity_field] = resolved
        del validated_data[id_field]


def basic_queryset_follow():
    return Follow.objects.all().prefetch_related(
        Prefetch("user", User.objects.all()),
        Prefetch("follow", User.objects.all()),
    )


class FollowsView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = basic_queryset_follow().all()

        # 絞り込み
        user = self.request.query_params.get("user")
        if user is not None:
            try:
                user = User.objects.get(id=int(user))
            except ValueError:
                return errors.parse_error_response("user", user)
            queryset = queryset.filter(user=user)

        target = self.request.query_params.get("target")
        if target is not None:
            try:
                target = User.objects.get(id=int(target))
            except ValueError:
                return errors.parse_error_response("target", target)
            queryset = queryset.filter(follow=target)

        return queryset


# 特定のフォローの情報を取得・削除する
class FollowView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        return basic_queryset_follow().all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return errors.not_found_response(f"follow of id {kwargs['pk']}")
