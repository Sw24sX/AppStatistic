from django.db import models
from datetime import datetime

from django.db import models
from .custom_validators.username_validators import CustomUnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = CustomUnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), blank=False, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Apps(models.Model):
    name = models.CharField(max_length=150)
    google_play_id = models.TextField()
    app_store_id = models.TextField(default=None)
    app_gallery = models.TextField(default=None)

    class Meta:
        db_table = 'Apps'

    def __str__(self):
        return self.name


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Subscriptions'
        unique_together = ('user', 'app')


class Platform(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'Platform'

    def __str__(self):
        return self.name


class PeriodData(models.Model):
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    score_5 = models.IntegerField(default=0)
    score_4 = models.IntegerField(default=0)
    score_3 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_1 = models.IntegerField(default=0)
    update_date = models.DateTimeField()

    class Meta:
        db_table = 'Period Data'
        unique_together = ('app', 'platform')


class HistoricalData(models.Model):
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    score_5 = models.IntegerField(default=0)
    score_4 = models.IntegerField(default=0)
    score_3 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_1 = models.IntegerField(default=0)
    update_date = models.DateTimeField()
    last_update_app = models.DateTimeField()
    last_update_data = models.DateTimeField()

    class Meta:
        db_table = 'Historical Data'
        unique_together = ('app', 'platform')
