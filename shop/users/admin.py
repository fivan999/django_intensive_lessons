import django.contrib.admin
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models


class ProfileAdmin(django.contrib.admin.TabularInline):
    """отображение модели Profile в админке"""

    model = users.models.Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileAdmin,)


django.contrib.admin.site.register(users.models.ShopUser, UserAdmin)
