import datetime

from django.http import HttpRequest

import pytz

from users.models import ShopUser


def users_with_birthdays(request: HttpRequest) -> dict:
    """пользователи, у которых сегодня день рождения"""
    try:
        today_user_datetime = datetime.datetime.now(pytz.timezone(
            request.COOKIES.get('django_timezone')
        ))
    except Exception:
        today_user_datetime = datetime.datetime.now()
    birthday_users = ShopUser.objects.filter(
        profile__birthday__month=today_user_datetime.month,
        profile__birthday__day=today_user_datetime.day,
        is_active=True
    ).only('email', 'first_name')
    return {'birthday_users': birthday_users}
