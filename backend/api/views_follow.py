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

from api import errors
from api.models import Live_register, Live_stream, User, Dm, Follow, Good

LOGGER = logging.getLogger("django")

# ユーザーの Serializer
# TODO: 適当な場所に移動させるべし
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # TODO: 現状モデルに icon がない
        fields = ["id", "username", "email", "profile"]

# FFのSerializer
class FollowSerializer(ModelSerializer):
    #registerers = IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Follow
        fields = [
            "id",
	    "user",
            "follow",
        ]


BASIC_QUERYSET_FOLLOW = Follow.objects.annotate(
    follows=Count("Follow")
)

# フォローを一覧 / 検索する
class FollowsView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = BASIC_QUERYSET_FOLLOW.all()

        # ユーザーを指定して検索する
        querystr = self.request.query_params.get("user")
        if querystr is not None:
            queries = querystr.split(" ")
            LOGGER.debug("search query: " + ", ".join(queries))
            for query in queries:
                queryset = queryset.filter(user__contains=query)

        follow = self.request.query_params.get("follow")
        if follow is not None:
            try:
                follow = (follow)
            except ValueError as ex:
                raise errors.ProcessRequestError(
                    errors.parse_error_response("follow", follow)
                ) from ex
            queryset = queryset.filter(registerers__gte=follow)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, args, kwargs)
        except errors.ProcessRequestError as ex:
            return ex.response

# 特定のユーザーのフォロー情報を取得する
class FollowView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LiveSerializer
    queryset = BASIC_QUERYSET_FOLLOW.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return errors.not_found_response(f"follow of id {kwargs['pk']}")
