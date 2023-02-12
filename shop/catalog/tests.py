from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    """тестируем страницы приложения catalog"""

    def test_item_list_endpoint(self) -> None:
        """тестируем главную страницу"""
        response = Client().get('/catalog')
        self.assertEqual(response.status_code, 301)

    def test_item_detail_endpoint(self) -> None:
        """тестируем отдельные товары"""
        test_cases = [1, 0, 'aboba', 's', 33, 999, '1']

        for test_case in test_cases:
            response = Client().get(f'/catalog/{test_case}')
            if isinstance(test_case, int) or (
                isinstance(test_case, str) and test_case.isdigit()
            ):
                self.assertEqual(response.status_code, 200, test_case)
            else:
                self.assertEqual(response.status_code, 404, test_case)
