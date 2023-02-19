from django.core.exceptions import ValidationError


def awesome_validator(value: str) -> None:
    """проверка, есть ли превосходно в значении"""

    lowered_value = value.lower()
    if 'превосходно' not in lowered_value and 'роскошно' not in lowered_value:
        raise ValidationError('Нет слова превосходно или роскошно')
