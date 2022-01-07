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

# DMのSerializer
class DmSerializer(ModelSerializer):
    #registerers = IntegerField(read_only=True)

    class Meta:
        model = Dm
        fields = [
            "id",
            "text",
            "sender",
            "sent_at",
            "receiver",
        ]


BASIC_QUERYSET_DM = Dm.objects.annotate(
    directmessages=Count("Dm")
)

# DMを一覧 / 検索する
class DmsView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DmSerializer

    def get_queryset(self):
        queryset = BASIC_QUERYSET_DM.all()

        # ターゲットの指定があればタイトルで検索する
        querystr = self.request.query_params.get("receiver")
        if querystr is not None:
            queries = querystr.split(" ")
            LOGGER.debug("search query: " + ", ".join(queries))
            for query in queries:
                queryset = queryset.filter(receiver__contains=query)

        sender = self.request.query_params.get("sender")
        if sender is not None:
            try:
                sender = (sender)
            except ValueError as ex:
                raise errors.ProcessRequestError(
                    errors.parse_error_response("sender", sender)
                ) from ex
            queryset = queryset.filter(registerers__gte=sender)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, args, kwargs)
        except errors.ProcessRequestError as ex:
            return ex.response

# 特定のDMの情報を取得する
class DmView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LiveSerializer
    queryset = BASIC_QUERYSET_DM.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return errors.not_found_response(f"directmessages of id {kwargs['pk']}")
