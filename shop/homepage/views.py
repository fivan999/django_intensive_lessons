from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """возвращаем главную страницу"""
    return render(request, 'home/homepage.html')


def coffee(request: HttpRequest) -> HttpResponse:
    """возвращаем 418"""
    return HttpResponse(
        '<body><h1>Я чайник</h1><body>', status=HTTPStatus.IM_A_TEAPOT
    )
