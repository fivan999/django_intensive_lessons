from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    """тестируем страницы приложения about"""

    def test_description_endpoint(self) -> None:
        """тестируем главную страницу about"""
        response = Client().get('/about')
        self.assertIn(response.status_code, (200, 301))
