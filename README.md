# django_intensive_lessons
[![Python package](https://github.com/fivan999/django_intensive_lessons/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/fivan999/django_intensive_lessons/actions/workflows/python-package.yml)
[![flake8 Lint](https://github.com/fivan999/django_intensive_lessons/actions/workflows/flake8.yml/badge.svg?branch=main)](https://github.com/fivan999/django_intensive_lessons/actions/workflows/flake8.yml)
## Установка и запуск

### Клонировать репозиторий
```
git clone https://github.com/fivan999/django_intensive_lessons
```
### Установка зависимостей
Создайте виртуальное окружение и активируйте его
```
python -m venv venv
venv\Scripts\activate
```

Установите нужные зависимости

Для запуска
```
pip install -r base_requirements.txt
```
Для разработки
```
pip install -r dev_requirements.txt
```
Для тестов
```
pip install -r test_requirements.txt
```
### Запуск
Создайте .env файл в папке shop.<br>

В нем нужно указать значения:<br>
- SECRET_KEY (ваш секретный ключ, по умолчанию - default)<br>
- DEBUG (включать ли режим дебага, по умолчанию - True)<br>
- ALLOWED_HOSTS (если включен DEBUG, он ['*'], иначе по умолчанию  - 127.0.0.1)<br>

Запустите проект:
```
python shop/manage.py runserver
```
