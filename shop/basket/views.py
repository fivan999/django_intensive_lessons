from basket.models import Basket

from catalog.models import Item
from catalog.views import ItemDetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View


class UserBasketView(LoginRequiredMixin, ListView):
    """отображение товаров польвователя, добавленных в корзину"""
    template_name = 'basket/basket.html'
    context_object_name = 'items'

    def get_queryset(self) -> QuerySet:
        """получаем необходимые записи"""
        print(Basket.objects.all())
        return Item.objects.get_published_items().filter(
            basket_items__user__pk=self.request.user.pk
        ).distinct()


class DeleteFromBasketView(LoginRequiredMixin, View):
    """удаляем товар из корзины пользователя"""
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """метод гет"""
        item = get_object_or_404(Item, pk=pk)
        Basket.objects.filter(
            user__pk=request.user.id, item__pk=item.id
        ).delete()
        return redirect('basket:basket')


class AddToBasketView(LoginRequiredMixin, View):
    """добавляем товар в корзину пользователя"""
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """метод гет"""
        item = get_object_or_404(Item, pk=pk)
        Basket.objects.update_or_create(user=request.user, item=item)
        return redirect('basket:basket')


class BasketDetailView(ItemDetailView):
    """один товар в корзине"""
    queryset = None

    def get_queryset(self) -> QuerySet:
        """получаем записи из которых будем выбирать нужную"""
        return Item.objects.get_published_items().filter(
            basket_items__user__pk=self.request.user.id
        )
