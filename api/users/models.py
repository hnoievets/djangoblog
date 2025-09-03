from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = 'users'

    avatar = models.ForeignKey(
        'api.File',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email address',
        error_messages={'unique': 'A user with that email already exists.'}
    )
    is_verified = models.BooleanField(default=False, verbose_name='verified')
    bio = models.TextField(max_length=500, verbose_name='bio', null=True)
