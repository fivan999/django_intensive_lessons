from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """возвращаем главную страницу"""
    return HttpResponse('<body><h1>Главная страница</h1></body>')


def coffee(request: HttpRequest) -> HttpResponse:
    """возвращаем 418"""
    return HttpResponse('Я чайник', status=418)
