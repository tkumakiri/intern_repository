from django.db.models.query import Prefetch
from django.db.models.query_utils import Q
from django.http.response import Http404
from rest_framework.fields import CharField
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from api import errors, views_lives, views_users
from api.models import (
    Follow,
    Live_picture,
    Live_register,
    Live_stream,
    Post,
    User,
)


# これはセキュリティ無視なので注意
def basic_queryset_post_noauth():
    return Post.objects.all().prefetch_related(
        Prefetch(
            "live_picture_set",
            Live_picture.objects.only("data").all(),
            "screenshots",
        )
    )


def queryset_filter_is_allowed(user):
    # 条件「自分がフォローしているユーザーが書き込んでいる投稿」
    is_following = Q(
        author__in=[
            follow.follow for follow in Follow.objects.all().filter(user=user)
        ]
    )

    # 条件「自分が参加登録をしたライブの投稿」
    is_registering = Q(
        live__in=[
            registration.live
            for registration in Live_register.objects.all().filter(user=user)
        ]
    )

    return Q(author=user) | is_following | is_registering


def basic_queryset_post(user):
    return (
        basic_queryset_post_noauth()
        .filter(queryset_filter_is_allowed(user))
        .distinct()
    )


class ScreenshotSerializer(Serializer):
    def to_internal_value(self, _data):
        raise NotImplementedError()

    def to_representation(self, instance):
        return CharField().to_representation(instance.data)


class PostSerializer(ModelSerializer):
    screenshots = ScreenshotSerializer(many=True, read_only=True)

    author = views_users.UserSerializer(read_only=True)
    live = views_lives.LiveSerializer(read_only=True)
    # FIXME: 自己参照なので参照を解かないことにする
    reply_target = None

    author_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    live_id = PrimaryKeyRelatedField(
        queryset=Live_stream.objects.all(), write_only=True
    )
    reply_target_id = PrimaryKeyRelatedField(
        queryset=Post.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author_id",
            "author",
            "reply_target_id",
            "reply_target",
            "live_id",
            "live",
            "text",
            "screenshots",
            "posted_at",
        ]

    def create(self, validated_data):
        resolve(validated_data, "reply_target_id", "reply_target")
        resolve(validated_data, "author_id", "author")
        resolve(validated_data, "live_id", "live")
        return super().create(validated_data)


def resolve(validated_data, id_field, entity_field):
    resolved = validated_data.get(id_field)
    if resolved is not None:
        validated_data[entity_field] = resolved
        del validated_data[id_field]


# 投稿を一覧 / 検索する
class PostsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = basic_queryset_post(request.user)

        # ここからリクエストによる絞り込み
        # live がある場合
        live = request.query_params.get("live")
        if live is not None:
            try:
                live = int(live)
            except ValueError:
                return errors.parse_error_response("live", live)
            queryset = queryset.filter(live=Live_stream.objects.get(id=live))

        # author がある場合
        author = request.query_params.get("author")
        if author is not None:
            try:
                author = int(author)
            except ValueError:
                return errors.parse_error_response("author", author)
            queryset = queryset.filter(author=User.objects.get(id=author))

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            screenshots = request.data["screenshots"]
        except KeyError as ex:
            return errors.error_response(
                400, -1, f"{ex} not found in request"
            )
        del request.data["screenshots"]

        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # チェック
        # 自分ではないアカウントから投稿しようとしていないか？
        # Note: この時点では *_id -> * への resolve() は行われていない
        if serializer.validated_data["author_id"] != self.request.user:
            return errors.invalid_author_response()

        # 参加登録していないライブに投稿しようとしていないか？
        live = serializer.validated_data["live_id"]
        try:
            Live_register.objects.get(user=self.request.user, live=live)
        except Live_register.DoesNotExist:
            return errors.post_unregistered_author_response()

        post = serializer.save()
        result = serializer.data

        # save screenshots
        # FIXME: performance
        for screenshot in screenshots:
            if len(screenshot) == 0:
                continue
            Live_picture(post=post, data=screenshot).save()

        result["screenshots"] = screenshots
        return Response(result, status=201)


# 特定の投稿の情報を取得する
class PostView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return basic_queryset_post(self.request.user).all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return errors.not_found_response(f"post of id {kwargs['pk']}")
