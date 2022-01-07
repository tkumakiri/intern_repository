import logging

from django.db.models.query import Prefetch
from django.http.response import Http404
from rest_framework import generics
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from api import errors, views_posts, views_users
from api.models import Good, Post, User

LOGGER = logging.getLogger("django")


class GoodSerializer(ModelSerializer):
    user = views_users.UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    post = views_posts.PostSerializer(read_only=True)
    post_id = PrimaryKeyRelatedField(
        queryset=views_posts.basic_queryset_post_noauth(), write_only=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Good
        fields = ["id", "user", "user_id", "post", "post_id"]
        depth = 1

    def create(self, validated_data):
        resolve(validated_data, "user_id", "user")
        resolve(validated_data, "post_id", "post")
        # TODO: いいねする権限があるか確認する
        return super().create(validated_data)


def resolve(validated_data, id_field, entity_field):
    resolved = validated_data.get(id_field)
    if resolved is not None:
        validated_data[entity_field] = resolved
        del validated_data[id_field]


def basic_queryset_good(user):
    return Good.objects.all().prefetch_related(
        Prefetch("user", User.objects.all()),
        Prefetch("post", views_posts.basic_queryset_post(user).all()),
    )


class GoodsView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs["user"] = self.request.user
        return GoodSerializer(*args, **kwargs)

    def get_queryset(self):
        queryset = basic_queryset_good(self.request.user).all()

        # 絞り込み
        user = self.request.query_params.get("user")
        if user is not None:
            try:
                user = User.objects.get(id=int(user))
            except ValueError:
                return errors.parse_error_response("user", user)
            queryset = queryset.filter(user=user)

        post = self.request.query_params.get("post")
        if post is not None:
            try:
                post = Post.objects.get(id=int(post))
            except ValueError:
                return errors.parse_error_response("post", post)
            queryset = queryset.filter(post=post)

        return queryset


# 特定のいいねの情報を取得・削除する
class GoodView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs["user"] = self.request.user
        return GoodSerializer(*args, **kwargs)

    def get_queryset(self):
        return basic_queryset_good(self.request.user).all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return errors.not_found_response(f"good of id {kwargs['pk']}")
