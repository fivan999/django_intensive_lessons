from datetime import datetime, time

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class TokenGeneratorWithTimestamp(PasswordResetTokenGenerator):
    """генератор токенов с заданным временем"""

    def __init__(self, token_validity_period: int) -> None:
        """создаем генератор с заданным временем"""
        self.token_validity_period = token_validity_period
        super().__init__()

    def check_token(self, user: AbstractBaseUser, token: str):
        """
        взял это из исходников, ибо нужно было просто
        заменить PASSWORD RESET TIMEOUT на кастомное
        """
        if not (user and token):
            return False

        try:
            ts_b36, _ = token.split('-')
            legacy_token = len(ts_b36) < 4
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if not constant_time_compare(
            self._make_token_with_timestamp(user, ts), token
        ):
            if not constant_time_compare(
                self._make_token_with_timestamp(user, ts, legacy=True),
                token,
            ):
                return False

        now = self._now()
        if legacy_token:
            ts *= 24 * 60 * 60
            ts += int(
                (now - datetime.combine(now.date(), time.min)).total_seconds()
            )
        if (self._num_seconds(now) - ts) > self.token_validity_period:
            return False

        return True


token_7_days = TokenGeneratorWithTimestamp(604800)
