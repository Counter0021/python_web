from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель пользователя
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send notifications about new comments?')

    class Meta(AbstractUser.Meta):
        pass
