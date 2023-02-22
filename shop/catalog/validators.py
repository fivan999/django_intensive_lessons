import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateMustContain:
    """валидатор для проверки вхождения слов"""

    def __init__(self, *required_words: tuple) -> None:
        """принимаем нужные слова"""
        self.required_words = list(map(lambda x: x.lower(), required_words))

    def __call__(self, text: str) -> None:
        """валидируем"""
        current_word = ''
        for symbol in text.lower():
            if re.fullmatch('[a-zа-я0-9]', symbol):
                current_word += symbol
            else:
                if current_word in self.required_words:
                    return
                current_word = ''
        if current_word not in self.required_words:
            raise ValidationError('Нет нужных слов')
