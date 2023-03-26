from http import HTTPStatus

import catalog.models

from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import ListView


class HomeItemListView(ListView):
    """возвращаем главную страницу"""
    queryset = catalog.models.Item.objects.get_items_on_main().order_by('name')
    template_name = 'home/homepage.html'
    context_object_name = 'items'


class CoffeeView(View):
    """возвращаем 418"""
    def get(self, request: HttpRequest) -> HttpResponse:
        """По запросу get увеличивает кол-во выпитого кофе
        на 1 у авторизованного пользователя"""
        if isinstance(request.user, AbstractBaseUser):
            request.user.profile.coffee_count += 1
            request.user.profile.save()
        return HttpResponse(
            '<body><h1>Я чайник</h1><body>', status=HTTPStatus.IM_A_TEAPOT
        )
