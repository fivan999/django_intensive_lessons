# django_intensive_lessons

## Установка и запуск

### Клонировать репозиторий
```
git clone https://github.com/fivan999.django_intensive_lessons
```
### Зависимости
Зависимости для запуска
```
pip install -r base_requirements.txt
```
Зависимости для тестирования
```
pip install -r test_requirements.txt
```
Зависимости для разработки
```
pip install -r dev_requirements.txt
```
### Запуск
Создайте .env файл в папке shop, рядом с manage.py и запишите в него:
```
SECRET_KEY=вашсекретныйключ
```
Запустите проект:
```
python shop/manage.py runserver
```