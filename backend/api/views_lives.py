import logging

from django.db.models.aggregates import Count
from django.db.models.query import Prefetch
from django.db.utils import IntegrityError
from django.http.response import Http404
from rest_framework.exceptions import NotAuthenticated
from rest_framework.fields import CharField, IntegerField
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from api import errors, views_users
from api.models import Live_register, Live_stream, User

LOGGER = logging.getLogger("django")


# ライブの Serializer
#
# API の結果に合わせ、モデルに registerers を追加している。
class LiveSerializer(ModelSerializer):
    registerers = IntegerField(read_only=True)

    class Meta:
        model = Live_stream
        fields = [
            "id",
            "title",
            "started_at",
            "live_url",
            "ticket_url",
            "registerers",
        ]


BASIC_QUERYSET_LIVE = Live_stream.objects.annotate(
    registerers=Count("live_register")
)


# ライブを一覧 / 検索する
class LivesView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LiveSerializer

    def get_queryset(self):
        queryset = BASIC_QUERYSET_LIVE.all()

        # クエリの指定があればタイトルで検索する
        querystr = self.request.query_params.get("q")
        if querystr is not None:
            queries = querystr.split(" ")
            LOGGER.debug("search query: " + ", ".join(queries))
            for query in queries:
                queryset = queryset.filter(title__contains=query)

        popularity = self.request.query_params.get("popularity")
        if popularity is not None:
            try:
                popularity = int(popularity)
            except ValueError as ex:
                raise errors.ProcessRequestError(
                    errors.parse_error_response("popularity", popularity)
                ) from ex
            queryset = queryset.filter(registerers__gte=popularity)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, args, kwargs)
        except errors.ProcessRequestError as ex:
            return ex.response


# 特定のライブの情報を取得する
class LiveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LiveSerializer
    queryset = BASIC_QUERYSET_LIVE.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return errors.not_found_response("specified live not found", 3000)


# ライブ登録の Serializer
class LiveRegistrationSerializer(ModelSerializer):
    user = views_users.UserSerializer(read_only=True)
    live = LiveSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    live_id = PrimaryKeyRelatedField(
        queryset=Live_stream.objects.all(), write_only=True
    )

    class Meta:
        model = Live_register
        fields = ["id", "user", "user_id", "live", "live_id"]
        depth = 1

    def create(self, validated_data):
        resolve(validated_data, "user_id", "user")
        resolve(validated_data, "live_id", "live")
        return super().create(validated_data)


def resolve(validated_data, id_field, entity_field):
    resolved = validated_data.get(id_field)
    if resolved is not None:
        validated_data[entity_field] = resolved
        del validated_data[id_field]


# ライブの参加登録を行う
class LiveRegistrationView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Live_register.objects.all().prefetch_related(
        Prefetch("live", BASIC_QUERYSET_LIVE.all())
    )
    serializer_class = LiveRegistrationSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)

        # 自分ではないユーザー ID から登録していないことを確認
        if serializer.validated_data["user_id"] != self.request.user:
            raise errors.ProcessRequestError(errors.invalid_user_response())

        # TODO: ライブのチケットが有効であることを確認

        return super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except NotAuthenticated:
            return errors.not_authenticated_response()
        except errors.ProcessRequestError as ex:
            return ex.response

    # TODO: error 1001, 3001, 3002
