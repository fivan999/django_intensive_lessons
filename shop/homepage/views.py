from http import HTTPStatus

from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import catalog.models


def home(request: HttpRequest) -> HttpResponse:
    """возвращаем главную страницу"""
    items = catalog.models.Item.objects.get_items_on_main().order_by('name')
    context = {'items': items}
    return render(request, 'home/homepage.html', context=context)


def coffee(request: HttpRequest) -> HttpResponse:
    """возвращаем 418"""
    if isinstance(request.user, AbstractBaseUser):
        request.user.profile.coffee_count += 1
        request.user.profile.save()
    return HttpResponse(
        '<body><h1>Я чайник</h1><body>', status=HTTPStatus.IM_A_TEAPOT
    )
