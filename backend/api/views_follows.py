import logging

from django.db.models.query import Prefetch
from django.db.utils import IntegrityError
from django.http.response import Http404
from rest_framework import generics
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from api import errors, views_users
from api.models import Follow, User

LOGGER = logging.getLogger("django")


class FollowSerializer(ModelSerializer):
    user = views_users.UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    target = views_users.UserSerializer(read_only=True, source="follow")
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
                raise errors.ProcessRequestError(
                    errors.parse_error_response("user", user)
                )
            except User.DoesNotExist:
                raise errors.ProcessRequestError(
                    errors.follow_query_user_not_found()
                )
            queryset = queryset.filter(user=user)

        target = self.request.query_params.get("target")
        if target is not None:
            try:
                target = User.objects.get(id=int(target))
            except ValueError:
                return errors.ProcessRequestError(
                    errors.parse_error_response("target", target)
                )
            except User.DoesNotExist:
                raise errors.ProcessRequestError(
                    errors.follow_query_user_not_found()
                )
            queryset = queryset.filter(follow=target)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except errors.ProcessRequestError as ex:
            return ex.response
        except IntegrityError:
            return errors.integrity_error_response(["user", "target"])

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return errors.integrity_error_response(["user", "target"])


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

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(request, *args, **kwargs)
            res.data = {}
            return res
        except errors.ProcessRequestError as ex:
            return ex.response

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise errors.ProcessRequestError(
                errors.delete_others_follow_response()
            )

        return super().perform_destroy(instance)
