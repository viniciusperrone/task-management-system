from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import BaseModel, SoftDeleteManager


class UserSoftDeleteManager(SoftDeleteManager):
    pass


class User(AbstractUser, BaseModel):
    email = models.EmailField("E-mail", unique=True, db_index=True)
    nickname = models.CharField("Nickname", max_length=10, blank=True, null=True)

    @property
    def full_name(self):
        return self.get_full_name()
