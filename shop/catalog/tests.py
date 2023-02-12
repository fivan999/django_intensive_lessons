from typing import Any

from django.test import Client, TestCase

from parameterized import parameterized


class StaticUrlTests(TestCase):
    """тестируем страницы приложения catalog"""

    def test_item_list_endpoint(self) -> None:
        """тестируем главную страницу"""
        response = Client().get('/catalog')
        self.assertEqual(response.status_code, 301)

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
    def test_item_detail_endpoint(self, test_case: Any, expected: Any) -> None:
        """тестируем отдельные товары"""
        response = Client().get(f'/catalog/{test_case}')
        self.assertEqual(
            response.status_code,
            expected,
            f'Expected: {expected}, got: {response.status_code}, '
            f'testcase: {test_case}',
        )
