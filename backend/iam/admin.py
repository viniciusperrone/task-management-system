from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from iam.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ["username", "email", "nickname"]
