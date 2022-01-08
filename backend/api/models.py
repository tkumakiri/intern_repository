from django.db import models
from django.db.models import constraints
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data['email']:
            raise ValueError('Users must have an email address.')

        profile = ""
        if request_data.get('profile'):
            profile = request_data['profile']

        user = self.model(
            username=request_data['username'],
            email=self.normalize_email(request_data['email']),
            is_active=True,
            last_login=now,
            date_joined=now,
            profile=profile
        )

    # if request_data.get('image_name'):
        if request_data.get('data'):
            # user.image_name = request_data['image_name']
            user.data = request_data['data']

        user.set_password(request_data['password'])
        user.save(using=self._db)

        # トークンの作成
        Token.objects.create(user=user)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        request_data = {
            'username': username,
            'email': email,
            'password': password
        }
        user = self.create_user(request_data)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
        null=False
    )
    profile = models.CharField(
        verbose_name='プロフィール',
        max_length=200,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    image_name = models.CharField(
        verbose_name='画像名',
        max_length=200,
        blank=False,
        null=True
    )

    data = models.TextField(
        verbose_name='画像データ',
        blank=False,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def user_has_perm(user, perm, obj):
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = 'api_user'
        swappable = 'AUTH_USER_MODEL'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='フォロー元',
        related_name='follow_user',
        on_delete=models.CASCADE

    )

    follow = models.ForeignKey(
        User,
        verbose_name='フォロー先',
        related_name='follow_follow',
        on_delete=models.CASCADE

    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "follow"],
                name = "unique_follow",
            ),
        ]


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
        related_name='Dm_sender',
        on_delete=models.CASCADE
    )

    sent_at = models.DateTimeField(
        verbose_name='書き込み時刻',
        default=timezone.now,
        blank=False,
        null=False
    )

    receiver = models.ForeignKey(
        User,
        verbose_name='送信先ユーザー',
        related_name='Dm_receiver',
        on_delete=models.CASCADE
    )

class Live_stream(models.Model):
    title = models.TextField(
        verbose_name='タイトル',
        max_length=200,
        blank=False,
        null=False
    )

    started_at = models.DateTimeField(
        verbose_name='日時',
        default=timezone.now,
        blank=False,
        null=False
    )

    live_url = models.CharField(
        verbose_name='ライブ視聴URL',
        max_length=2000,
        blank=False,
        null=True
    )

    ticket_url = models.CharField(
        verbose_name='ライブチケット購入URL',
        max_length=2000,
        blank=False,
        null=True
    )

class Ticket(models.Model):
    live = models.ForeignKey(
        Live_stream,
        verbose_name='ライブ',
        on_delete=models.CASCADE
    )

    ticket_number = models.CharField(
        verbose_name='チケット番号',
        max_length=200,
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "live"],
                name = "unique_registration",
            ),
        ]

class Post(models.Model):
    text = models.TextField(
        verbose_name='内容',
        max_length=200,
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        User,
        verbose_name='書いたユーザー',
        on_delete=models.CASCADE
    )

    posted_at = models.DateTimeField(
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
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

class Live_picture(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name='投稿',
        on_delete=models.CASCADE
    )

    data = models.TextField(
        verbose_name='画像データ',
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["post", "user"],
                name = "unique_good",
            ),
        ]
