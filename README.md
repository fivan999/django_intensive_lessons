# django_intensive_lessons

## Установка и запуск

### Клонировать репозиторий
```
git clone https://github.com/fivan999.django_intensive_lessons
```
### Установка зависимостей
Создайте виртуальное окружение и активируйте его
```
python -m venv venv
venv\Scripts\activate
```

Установите нужные зависимости
```
pip install -r requirements.txt
```
### Запуск
Создайте .env файл в папке shop.<br>

В нем нужно указать значения:<br>
- SECRET_KEY (ваш секретный ключ, по умолчанию - default)<br>
- DEBUG (включать ли режим дебага, по умолчанию - True)<br>
- ALLOWED_HOSTS (если включен DEBUG, он ['*'], иначе по умолчанию  - [])<br>

Запустите проект:
```
python shop/manage.py runserver
```