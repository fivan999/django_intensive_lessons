from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import mock

from parameterized import parameterized

import pytz

from users.models import ShopUser


START_DATETIME = pytz.UTC.localize(timezone.datetime(2023, 1, 1, 0, 0, 0))
END_DATETIME = pytz.UTC.localize(timezone.datetime(2023, 1, 1, 12, 1, 0))


class UserTests(TestCase):
    """тестируем пользователя"""

    register_data = {
        'username': 'aboba',
        'email': 'aboba@ya.ru',
        'password1': 'ajdfgbjuygfrb',
        'password2': 'ajdfgbjuygfrb'
    }

    def test_user_register_status_code(self) -> None:
        """тестируем статус код страницы регистрации"""
        response = Client().get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_user_register_context(self) -> None:
        """тестируем контекст страницы регистрации"""
        response = Client().get(reverse('users:signup'))
        self.assertIn('form', response.context)

    def test_user_register_redirect(self) -> None:
        """тестируем редирект на главную страницу"""
        response = Client().post(
            reverse('users:signup'),
            self.register_data,
            follow=True
        )
        self.assertRedirects(response, reverse('homepage:homepage'))

    def test_user_register_success(self) -> None:
        """тестируем появление записи в бд"""
        user_count = ShopUser.objects.count()
        Client().post(
            reverse('users:signup'),
            self.register_data,
            follow=True
        )
        self.assertEqual(ShopUser.objects.count(), user_count + 1)

    @override_settings(USER_IS_ACTIVE=False)
    def test_user_not_is_active(self) -> None:
        """тестируем неактивность пользователя"""
        Client().post(
            reverse('users:signup'),
            self.register_data,
            follow=True
        )
        self.assertFalse(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=True)
    def test_user_is_active(self) -> None:
        """тестируем активность пользователя"""
        Client().post(
            reverse('users:signup'),
            self.register_data,
            follow=True
        )
        self.assertTrue(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=False)
    def test_user_activation(self) -> None:
        """тестируем активацию пользователя"""
        Client().post(
            reverse('users:signup'),
            self.register_data,
            follow=True
        )
        user = ShopUser.objects.get(pk=1)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        Client().get(
            reverse(
                'users:activate_user',
                kwargs={'uidb64': uid, 'token': token}
            )
        )
        self.assertTrue(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=False)
    def test_user_activation_error(self) -> None:
        """тестируем ошибку активации юзера"""
        with mock.patch(
            'django.utils.timezone.now', return_value=START_DATETIME
        ):
            Client().post(
                reverse('users:signup'),
                self.register_data,
                follow=True
            )
        with mock.patch(
            'django.utils.timezone.now', return_value=END_DATETIME
        ):
            user = ShopUser.objects.get(pk=1)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            Client().get(
                reverse(
                    'users:activate_user',
                    kwargs={'uidb64': uid, 'token': token}
                )
            )
            self.assertFalse(user.is_active)

    @parameterized.expand(
        [
            [register_data['username'], register_data['password1'], True],
            [register_data['email'], register_data['password1'], True],
            [register_data['username'], 'awrgfkjuagvwf', False],
            ['qwertyuiop[]', register_data['password1'], False],
        ]
    )
    def test_user_authenticate(
        self, username: str, password: str, expected: bool
    ) -> None:
        """проверяем возможность аутентификации"""
        Client().post(
            reverse('users:signup'),
            self.register_data,
            follow=True
        )
        user = ShopUser.objects.get(pk=1)
        last_login_start = user.last_login
        Client().post(
            reverse('users:login'),
            {'username': username, 'password': password},
            follow=True
        )
        last_login_end = user.last_login
        self.assertFalse(last_login_end != last_login_start)

    def tearDown(self) -> None:
        """чистим бд после тестов"""
        ShopUser.objects.all().delete()
        super().tearDown()
