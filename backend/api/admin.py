from django.contrib import admin
from .models import User, Follow, Dm, Live_stream, Ticket, Live_register, Post, Live_picture, Good

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Dm)
admin.site.register(Live_stream)
admin.site.register(Ticket)
admin.site.register(Live_register)
admin.site.register(Post)
admin.site.register(Live_picture)
admin.site.register(Good)
