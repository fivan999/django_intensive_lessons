from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.tokens import token_7_days


def activation_email(
    request: HttpRequest, where_to: str, user: AbstractBaseUser
) -> None:
    """письмо с активацией пользователя"""
    if where_to == 'users:reset_login_attempts':
        token = token_7_days.make_token(user)
    elif where_to == 'users:activate_user':
        token = default_token_generator.make_token(user)
    message = render_to_string(
        'users/activate_user.html',
        {
            'username': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
            'protocol': 'https' if request.is_secure() else 'http',
            'where_to': where_to
        }
    )
    send_mail(
        'Activate your account',
        message,
        settings.EMAIL,
        [user.email],
        fail_silently=False
    )
