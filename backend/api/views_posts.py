from django.db.models.query import Prefetch
from rest_framework.fields import CharField
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView

from api import errors, views_lives
from api.models import Live_picture, Live_stream, Post, User

BASIC_QUERYSET_POST = Post.objects.all().prefetch_related("live_picture_set")


class ScreenshotSerializer(Serializer):
    def to_internal_value(self, _data):
        raise NotImplementedError()

    def to_representation(self, instance):
        return CharField().to_representation(instance.data)


class PostSerializer(ModelSerializer):
    screenshots = ScreenshotSerializer(many=True, read_only=True)

    author = views_lives.UserSerializer(read_only=True)
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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = BASIC_QUERYSET_POST.all().prefetch_related(
            Prefetch(
                "live_picture_set",
                Live_picture.objects.only("data").all(),
                "screenshots",
            )
        )
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            screenshots = request.data["screenshots"]
            del request.data["screenshots"]

            serializer = PostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            result = serializer.data

            # save screenshots
            # FIXME: performance
            for screenshot in screenshots:
                Live_picture(post=post, data=screenshot).save()

            result["screenshots"] = screenshots
            return Response(result, status=201)
        except KeyError as ex:
            return errors.error_response(
                400, -1, f"{ex} not found in request"
            )
