from http import HTTPStatus

from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """возвращаем главную страницу"""
    return HttpResponse('<body><h1>Главная страница</h1></body>')


def coffee(request: HttpRequest) -> HttpResponse:
    """возвращаем 418"""
    return HttpResponse(
        '<body><h1>Я чайник</h1><body>', status=HTTPStatus.IM_A_TEAPOT
    )
