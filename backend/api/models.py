from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(AbstractUser):

    email = models.EmailField(
        verbose_name='メールアドレス',
        unique=True,
        null=False
    )

    profile = models.TextField(
        verbose_name='プロフィール',
        max_length=200,
        blank=False,
        null=True
    )

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='フォロー元',
        on_delete=models.CASCADE

    )

    follow = models.ForeignKey(
        User,
        verbose_name='フォロー先',
        on_delete=models.CASCADE

    )


class Dm(models.Model):
    text = models.TextField(
        verbose_name='内容',
        max_length=200,
        blank=False,
        null=False
    )

    sender = models.ForeignKey(
        User,
        verbose_name='書いたユーザー',
        on_delete=models.CASCADE
    )

    sent_at = models.DateField(
        verbose_name='書き込み時刻',
        default=timezone.now,
        blank=False,
        null=False
    )

    receiver = models.ForeignKey(
        User,
        verbose_name='送信先ユーザー',
        on_delete=models.CASCADE
    )

class Live_stream(models.Model):
    title = models.TextField(
        verbose_name='タイトル',
        max_length=200,
        blank=False,
        null=False
    )

    started_at = models.DateField(
        verbose_name='日時',
        default=timezone.now,
        blank=False,
        null=False
    )

    live_url = models.CharField(
        verbose_name='ライブ視聴URL',
        blank=False,
        null=True
    )

    ticket_url = models.CharField(
        verbose_name='ライブチケット購入URL',
        blank=False,
        null=True
    )

class Ticket(models.Model):
    live = models.ForeignKey(
        Live_stream,
        verbose_name='ライブ',
        on_delete=models.CASCADE
    )

    ticket_number = models.charField(
        verbose_name='チケット番号',
        blank=False,
        null=False
    )

class Live_register(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    live = models.ForeignKey(
        Live_stream,
        verbose_name='ライブ配信',
        on_delete=models.CASCADE
    )

class Post(models.Model):
    text = models.TextField(
        verbose_name='内容',
        max_length=200,
        blank=False,
        null=False
    )

    auther = models.ForeignKey(
        User,
        verbose_name='書いたユーザー',
        on_delete=models.CASCADE
    )

    posted_at = models.DateField(
        default=timezone.now,
        blank=False,
        null=False
    )

    live = models.ForeignKey(
        Live_stream,
        verbose_name='ライブ配信',
        on_delete=models.CASCADE
    )

    reply_target = models.ForeignKey(
        "self",
        verbose_name='リプライ先投稿',
        # on_delete=models.CASCADE
    )


class Live_picture(models.Model):

    post = models.ForeignKey(
        Post,
        verbose_name='投稿',
        on_delete=models.CASCADE
    )

    image_name = models.CharField(
        verbose_name='投稿名',
        blank=False,
        null=False
    )

    data = models.CharField(
        verbose_name='画像データ',
        blank=False,
        null=False
    )

class Good(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name='投稿',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        verbose_name='書いたユーザー',
        on_delete=models.CASCADE
    )





