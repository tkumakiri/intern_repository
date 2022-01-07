from django.db.models.expressions import ValueRange
from django.db.models.query import Prefetch
from django.db.models.query_utils import Q
from django.http.response import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from api import errors, views_lives
from api.models import Dm, User


class DirectMessageSerializer(ModelSerializer):
    sender = views_lives.UserSerializer(read_only=True)
    receiver = views_lives.UserSerializer(read_only=True)
    sender_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    receiver_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Dm
        fields = [
            "id",
            "sender",
            "sender_id",
            "receiver",
            "receiver_id",
            "text",
            "sent_at",
        ]

    def create(self, validated_data):
        resolve(validated_data, "sender_id", "sender")
        resolve(validated_data, "receiver_id", "receiver")
        return super().create(validated_data)


def resolve(validated_data, id_field, entity_field):
    resolved = validated_data.get(id_field)
    if resolved is not None:
        validated_data[entity_field] = resolved
        del validated_data[id_field]


def basic_queryset_post_noauth():
    return Dm.objects.all().prefetch_related(
        Prefetch("sender", User.objects.all()),
        Prefetch("receiver", User.objects.all()),
    )


def queryset_filter_is_allowed(user):
    # 条件「自分が送信している」か「自分が受け取っている」
    return Q(sender=user) | Q(receiver=user)


def basic_queryset_post(user):
    return (
        basic_queryset_post_noauth()
        .all()
        .filter(queryset_filter_is_allowed(user))
        .distinct()
    )


# ダイレクトメッセージを一覧・作成する
class DirectMessagesView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectMessageSerializer

    def get_queryset(self):
        queryset = basic_queryset_post(self.request.user).all()

        # 絞り込み
        central = self.request.query_params.get("central")
        if central is not None:
            try:
                central = User.objects.get(id=int(central))
            except ValueError:
                return errors.parse_error_response("sender", sender)
            queryset = queryset.filter(
                Q(sender=central) | Q(receiver=central)
            )

        target = self.request.query_params.get("target")
        if target is not None:
            if central is None:
                return errors.error_response(
                    400,
                    -1,
                    "central must be specified when target is specified",
                )
            try:
                target = User.objects.get(id=int(target))
            except ValueError:
                return errors.parse_error_response("target", target)
            queryset = queryset.filter(
                Q(receiver=central, sender=target)
                | Q(receiver=target, sender=central)
            )

        return queryset


class DirectMessageView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectMessageSerializer

    def get_queryset(self):
        return basic_queryset_post(self.request.user).all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *kwargs, **kwargs)
        except Http404:
            return errors.not_found_response(
                f"directmessage of id {kwargs['pk']}"
            )
