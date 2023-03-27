import datetime

from django.conf import settings
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from freezegun import freeze_time

from parameterized import parameterized

import pytz

from users.models import Profile, ShopUser


START_DATETIME = pytz.UTC.localize(timezone.datetime(2023, 1, 1, 0, 0, 0))
END_DATETIME = pytz.UTC.localize(timezone.datetime(2023, 1, 1, 12, 1, 0))
END_DATETIME_WEEK = pytz.UTC.localize(timezone.datetime(2023, 1, 9, 0, 0, 0))


class UserTests(TestCase):
    """тестируем пользователя"""

    register_data = {
        'username': 'aboba',
        'email': 'aboba@yandex.ru',
        'password1': 'ajdfgbjuygfrb',
        'password2': 'ajdfgbjuygfrb',
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
            reverse('users:signup'), self.register_data, follow=True
        )
        self.assertRedirects(response, reverse('homepage:homepage'))

    def test_user_register_success(self) -> None:
        """тестируем появление записи в бд"""
        user_count = ShopUser.objects.count()
        Client().post(reverse('users:signup'), self.register_data, follow=True)
        self.assertEqual(ShopUser.objects.count(), user_count + 1)

    @override_settings(USER_IS_ACTIVE=False)
    def test_user_not_is_active(self) -> None:
        """тестируем неактивность пользователя"""
        Client().post(reverse('users:signup'), self.register_data, follow=True)
        self.assertFalse(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=True)
    def test_user_is_active(self) -> None:
        """тестируем активность пользователя"""
        Client().post(reverse('users:signup'), self.register_data, follow=True)
        self.assertTrue(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=False)
    def test_user_activation(self) -> None:
        """тестируем активацию пользователя"""
        client = Client()
        client.post(reverse('users:signup'), self.register_data, follow=True)
        text = mail.outbox[0].body
        text = text[text.find('http'):].strip('\n')
        client.get(text)
        self.assertTrue(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=False)
    def test_user_activation_error(self) -> None:
        """тестируем ошибку активации юзера"""
        client = Client()
        with freeze_time('2023-01-01 00:00:00'):
            client.post(
                reverse('users:signup'), self.register_data, follow=True
            )
        with freeze_time('2023-01-01 13:00:00'):
            text = mail.outbox[0].body
            text = text[text.find('http'):].strip('\n')
            client.get(text)
            self.assertFalse(ShopUser.objects.get(pk=1).is_active)

    @parameterized.expand(
        [
            [register_data['username'], register_data['password1'], True],
            [register_data['email'], register_data['password1'], True],
            [register_data['username'], 'awrgfkjuagvwf', False],
            ['qwertyuiop[]', register_data['password1'], False],
        ]
    )
    @override_settings(USER_IS_ACTIVE=True)
    def test_user_authenticate(
        self, username: str, password: str, expected: bool
    ) -> None:
        """проверяем возможность аутентификации"""
        client = Client()
        client.post(reverse('users:signup'), self.register_data, follow=True)
        client.get(reverse('users:logout'), follow=True)
        response = client.post(
            reverse('users:login'),
            {'username': username, 'password': password},
            follow=True,
        )
        self.assertEqual(response.context['user'].is_authenticated, expected)

    @parameterized.expand(
        [
            ['aboba@ya.ru', 'aboba@yandex.ru'],
            ['ABOBA@yA.ru', 'aboba@yandex.ru'],
            ['abo.ba.+ger@gmail.com', 'aboba@gmail.com'],
            ['ABo.ba.+ger@gmail.com', 'aboba@gmail.com'],
        ]
    )
    def test_user_normalize_email(self, email: str, expected: str) -> None:
        """тестируем валидацию почты"""
        Client().post(
            reverse('users:signup'),
            {
                'username': self.register_data['username'],
                'email': email,
                'password1': self.register_data['password1'],
                'password2': self.register_data['password2'],
            },
            follow=True,
        )
        self.assertEqual(ShopUser.objects.get(pk=1).email, expected)

    @override_settings(USER_IS_ACTIVE=True)
    def test_user_deactivation(self) -> None:
        """тестируем деактивацию профиля в авторизации"""
        client = Client()
        client.post(reverse('users:signup'), self.register_data, follow=True)
        for _ in range(settings.LOGIN_ATTEMPTS):
            client.post(
                reverse('users:login'),
                {
                    'username': self.register_data['username'],
                    'password': 'testbeb',
                },
                follow=True,
            )
        self.assertFalse(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=True)
    def test_user_reactivation_success(self) -> None:
        """тестируем реактивацию профиля"""
        client = Client()
        client.post(reverse('users:signup'), self.register_data, follow=True)
        user = ShopUser.objects.get(pk=1)
        for _ in range(settings.LOGIN_ATTEMPTS):
            client.post(
                reverse('users:login'),
                {'username': user.username, 'password': 'testbeb'},
                follow=True,
            )
        text = mail.outbox[0].body
        text = text[text.find('http'):].strip('\n')
        client.get(text)
        self.assertTrue(ShopUser.objects.get(pk=1).is_active)

    @override_settings(USER_IS_ACTIVE=True)
    def test_user_reactivation_error(self) -> None:
        """тестируем ошибку реактивации профиля"""
        with freeze_time('2023-01-01'):
            client = Client()
            client.post(
                reverse('users:signup'), self.register_data, follow=True
            )
            user = ShopUser.objects.get(pk=1)
            for _ in range(settings.LOGIN_ATTEMPTS):
                client.post(
                    reverse('users:login'),
                    {'username': user.username, 'password': 'testbeb'},
                    follow=True,
                )
        with freeze_time('2023-01-10'):
            text = mail.outbox[0].body
            text = text[text.find('http'):].strip('\n')
            client.get(text)
            self.assertFalse(ShopUser.objects.get(pk=1).is_active)

    def tearDown(self) -> None:
        """чистим бд после тестов"""
        ShopUser.objects.all().delete()
        super().tearDown()


class TestContextProcessor(TestCase):
    """тестируем работу контекст-процессора"""

    def setUp(self) -> None:
        """подготовка к тестированию, создание тестовых данных"""
        self.test_user1 = ShopUser.objects.create(
            email='testuser1@yandex.ru',
            username='testuser1',
            is_active=True
        )
        self.test_user1.set_password('password')
        self.test_profile1 = Profile.objects.create(
            birthday=datetime.date.today(),
            user=self.test_user1
        )

        self.test_user2 = ShopUser.objects.create(
            email='testuser2@yandex.ru',
            username='testuser2',
            is_active=True
        )
        self.test_user2.set_password('password')
        self.test_profile2 = Profile.objects.create(
            birthday=datetime.date.today() - datetime.timedelta(days=1),
            user=self.test_user2
        )
        super().setUp()

    def test_birthday_users_in_context(self) -> None:
        """проверям наличие дней рождения пользователей в контексте"""
        response = Client().get(reverse('homepage:homepage'))
        self.assertIn('birthday_users', response.context)

    def test_birthday_users_count(self) -> None:
        """проверяем количество пользователей с днем рождения в контексте"""
        response = Client().get(reverse('homepage:homepage'))
        self.assertEqual(len(response.context['birthday_users']), 1)

    def test_birthday_users_exact_user(self) -> None:
        """проверяем id пользователя, у которого сегодня день рождения"""
        response = Client().get(reverse('homepage:homepage'))
        self.assertEqual(response.context['birthday_users'].first().pk, 1)

    def tearDown(self) -> None:
        """удаление тестовых данных"""
        Profile.objects.all().delete()
        ShopUser.objects.all().delete()
        super().tearDown()
