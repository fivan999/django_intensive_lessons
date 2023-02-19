import re

import django.core.exceptions


def awesome_validator(value: str) -> None:
    """проверка, есть ли превосходно в значении"""
    if 'превосходно' not in value and 'роскошно' not in value:
        raise django.core.exceptions.ValidationError('Нет слова превосходно')


def slug_validator(value: str) -> None:
    """валидатор для уникального поля slug"""
    if not re.fullmatch('[a-zA-Z]*[0-9]*-*_*', value):
        raise django.core.exceptions.ValidationError(
            'Строка должна содержать только цифры, '
            'буквы латиницы и символы - и _'
        )
