from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    """тестируем страницы приложения homepage"""

    def test_home_endpoint(self) -> None:
        """тестируем главную страницу"""
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)
