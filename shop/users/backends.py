from django.contrib.auth.backends import ModelBackend

from users.models import ShopUser


class EmailBackend(ModelBackend):
    """бекенд для аутентификации по почте"""

    def authenticate(
            self, request, username=None, password=None, **kwargs
    ) -> None:
        try:
            user = ShopUser.objects.get(email=username)
        except ShopUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
