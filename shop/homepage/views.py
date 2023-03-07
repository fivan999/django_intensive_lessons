from http import HTTPStatus

from catalog.models import Item

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """возвращаем главную страницу"""
    items = Item.objects.get_published_items().filter(
        is_on_main=True
    ).only(
        'name', 'text', 'category__name', 'main_image__image'
    ).order_by(
        'name'
    )
    context = {
        'items': items
    }
    return render(request, 'home/homepage.html', context=context)


def coffee(request: HttpRequest) -> HttpResponse:
    """возвращаем 418"""
    return HttpResponse(
        '<body><h1>Я чайник</h1><body>', status=HTTPStatus.IM_A_TEAPOT
    )
