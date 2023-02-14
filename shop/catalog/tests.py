from typing import Any

from django.conf import settings
from django.test import Client, TestCase

from parameterized import parameterized

from .middleware import reverse_russian_words


class StaticUrlTests(TestCase):
    """тестируем страницы приложения catalog"""

    def test_item_list(self) -> None:
        """тестируем главную страницу"""
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            [1, 200],
            [0, 200],
            ['aboba', 404],
            ['s', 404],
            [33, 200],
            [999, 200],
            [1, 200],
            [-1, 404],
            [-0, 200],
        ]
    )
    def test_item_detail(self, test_case: Any, expected: Any) -> None:
        """тестируем отдельные товары"""
        response = Client().get(f'/catalog/{test_case}/')
        self.assertEqual(
            response.status_code,
            expected,
            f'Expected: {expected}, got: {response.status_code}, '
            f'testcase: {test_case}',
        )

    @parameterized.expand(
        [
            [1, 200],
            [0, 404],
            ['aboba', 404],
            ['s', 404],
            ['ad43', 404],
            ['43&&&', 404],
            [33, 200],
            [999, 200],
            [1, 200],
            [-1, 404],
        ]
    )
    def test_re_grader_zero_int_item_detail(
        self, test_case: Any, expected: Any
    ) -> None:
        """тестируем регулярку с инт>0"""
        response = Client().get(f'/catalog/re/{test_case}/')
        self.assertEqual(
            response.status_code,
            expected,
            f'Expected: {expected}, got: {response.status_code}, '
            f'testcase: {test_case}',
        )

    @parameterized.expand(
        [
            [1, 200],
            [0, 404],
            ['aboba', 404],
            ['s', 404],
            ['ad43', 404],
            ['43&&&', 404],
            [33, 200],
            [999, 200],
            [1, 200],
            [-1, 404],
        ]
    )
    def test_converter_grader_zero_int_item_detail(
        self, test_case: Any, expected: Any
    ) -> None:
        """тестируем конвертер с инт>0"""
        response = Client().get(f'/catalog/converter/{test_case}/')
        self.assertEqual(
            response.status_code,
            expected,
            f'Expected: {expected}, got: {response.status_code}, '
            f'testcase: {test_case}',
        )


class TestReverseRussianWordsMiddleware(TestCase):
    """тестируем работоспособность ReverseRussianMiddleware"""

    default_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    def test_home_status_code_without_reverse(self) -> None:
        """тестируем статус код без reverse middleware"""
        settings.MIDDLEWARE = (
            TestReverseRussianWordsMiddleware.default_middleware
        )

        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_home_content_without_middleware(self) -> None:
        """тестируем контент страницы без reverse middleware"""
        settings.MIDDLEWARE = (
            TestReverseRussianWordsMiddleware.default_middleware
        )

        client = Client()
        responses = [client.get('').content.decode() for _ in range(10)]
        self.assertEqual(
            len(set(responses)), 1, 'Значения ответов не одинаковые'
        )

    def test_home_status_code_with_middleware(self) -> None:
        """тестируем статус код с reverse middleware"""
        settings.MIDDLEWARE = (
            TestReverseRussianWordsMiddleware.default_middleware
        ) + ['catalog.middleware.ReverseRussianMiddleware']

        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_home_content_with_middleware(self) -> None:
        """тестируем контент страницы с reverse middleware"""
        settings.MIDDLEWARE = (
            TestReverseRussianWordsMiddleware.default_middleware
        ) + ['catalog.middleware.ReverseRussianMiddleware']

        client = Client()
        responses = [client.get('').content.decode() for _ in range(10)]
        test_passed = (
            len(set(responses[0:-1])) == 1
            and reverse_russian_words(responses[0]) == responses[-1]
        )
        self.assertEqual(test_passed, True)
