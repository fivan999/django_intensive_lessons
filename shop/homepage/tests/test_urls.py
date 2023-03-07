from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    """тестируем страницы приложения homepage"""

    def test_home(self) -> None:
        """тестируем главную страницу"""
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_coffee_status_code(self) -> None:
        """тестируем код страницы coffee"""
        response = Client().get('/coffee/')
        self.assertEqual(response.status_code, 418)

    def test_coffee_content(self) -> None:
        """тестируем контент страницы coffee"""
        response = Client().get('/coffee/')
        self.assertEqual(
            response.content.decode(), '<body><h1>Я чайник</h1><body>'
        )
