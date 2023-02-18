import re

from django.conf import settings
from django.http import HttpRequest, HttpResponse


class ReverseRussianMiddleware:
    """реверс русских слов в каждом 10м запросе"""

    def __init__(self, get_response) -> None:
        """инициализируем класс"""
        self.get_response = get_response
        self.counter = 0

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """обрабатываем запрос"""
        response = self.get_response(request)
        if request.method == 'GET' and settings.REVERSE_RUSSIAN_WORDS:
            self.counter += 1
            if self.counter % 10 == 0:
                words = response.content.decode()
                return HttpResponse(self.reverse_russian_words(words))
        return response

    @staticmethod
    def reverse_russian_words(text: str) -> str:
        """переворачиваем русские слова в тексте"""
        result = ''
        russian_word = ''
        for symbol in text:
            if bool(re.search('[а-я]', symbol.lower())):
                russian_word += symbol
            else:
                result += russian_word[::-1]
                result += symbol
                russian_word = ''
        return result + russian_word[::-1]
