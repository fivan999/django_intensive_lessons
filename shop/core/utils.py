import re


def normalize_models_name(value: str) -> str:
    """нормализуем имя модели"""
    # похожие русские буквы заменяем на английские
    replace_letters = {
        'е': 'e',
        'о': 'o',
        'с': 'c',
        'х': 'x',
        'а': 'a',
        'у': 'y',
    }
    result = ''
    for symbol in value.lower():
        if re.fullmatch('[а-яa-z0-9]', symbol):
            result += replace_letters.get(symbol, symbol)
    return result
