import logging

from django.db.models.aggregates import Count
from rest_framework.fields import IntegerField
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer

from api import errors
from api.models import Live_stream

LOGGER = logging.getLogger("django")


# ライブの Serializer
#
# API の結果に合わせ、モデルに registerers を追加している。
class LiveSerializer(ModelSerializer):
    registerers = IntegerField()

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
