from django.conf import settings
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

import users.services
from users.models import ShopUser


class EmailBackend(ModelBackend):
    """бекенд для аутентификации по почте"""

    def authenticate(
        self, request, username=None, password=None, **kwargs
    ) -> None:
        try:
            user = ShopUser.objects.get(
                Q(email=username) | Q(username=username)
            )
        except ShopUser.DoesNotExist:
            return None
        if user.check_password(password):
            user.login_attempts = 0
            user.save()
            return user
        else:
            user.login_attempts += 1
            if user.login_attempts == settings.LOGIN_ATTEMPTS:
                user.is_active = False
                messages.error(
                    request,
                    'Вы слишком много раз пытались '
                    'войти в аккаунт'
                    ', поэтому нам пришлось его деактивировать. '
                    'Ссылка для восстановления '
                    'отправлена на ваш email.',
                )
                users.services.activation_email(
                    request, 'users:reset_login_attempts', user
                )
            elif user.login_attempts > settings.LOGIN_ATTEMPTS:
                messages.error(request, 'Проверьте свою почту')
            user.save()
        return None
