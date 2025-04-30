from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.manager import UserManager
from utils.db.models import BaseModel


class User(AbstractUser, BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    is_merchant = models.BooleanField(default=False)
    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        ordering = [
            "name",
            "email",
        ]
