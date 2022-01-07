from datetime import datetime
from django.http.response import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from api.models import Live_register, Live_stream, User
from api.serializer import AccountSerializer


# ユーザー情報取得
class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        live_alldata = Live_register.objects.filter(user=user).all()
        old_live_list = []
        new_live_list = []

        for live in live_alldata:
            live_streams = Live_stream.objects.filter(id=live.live.id)
            live_a = {}
            for stream in live_streams:
                live_a["title"] = stream.title
                live_a["started_at"] = stream.started_at
                print(datetime.date.today())
                print(stream.started_at)
                if stream.started_at < datetime.date.today():
                    old_live_list.append((live_a))
                else:
                    new_live_list.append(live_a)

        return Response(data={
            'username': user.username,
            'email': user.email,
            'profile': user.profile,
            'image_name': user.image_name,
            'data': user.data,
            'old_live_list': old_live_list,
            'new_live_list': new_live_list
            },
            status=status.HTTP_200_OK)