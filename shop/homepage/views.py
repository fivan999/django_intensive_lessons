from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """возвращаем главную страницу"""
    return HttpResponse('<body><h1>Главная страница</h1></body>')
