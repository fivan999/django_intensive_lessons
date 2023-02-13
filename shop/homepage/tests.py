from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    """тестируем страницы приложения homepage"""

    def test_home_endpoint(self) -> None:
        """тестируем главную страницу"""
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint(self) -> None:
        """тестируем страницу с кодом 418"""
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode(), 'Я чайник')
