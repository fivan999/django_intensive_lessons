import re

from django.core.exceptions import ValidationError


def awesome_validator(value: str) -> None:
    """проверка, есть ли превосходно в значении"""

    current_word = ''
    for symbol in value.lower():
        if re.fullmatch('[a-zа-я0-9]', symbol):
            current_word += symbol
        else:
            if current_word in ('роскошно', 'превосходно'):
                return
            current_word = ''
    if current_word not in ('роскошно', 'превосходно'):
        raise ValidationError('Нет слова превосходно или роскошно')


# def validate_must_contain(*values):
