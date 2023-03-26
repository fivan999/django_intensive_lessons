import catalog.models

from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView


class ItemListView(ListView):
    """Страница со всеми элементами"""
    queryset = catalog.models.Item.objects.get_published_items().order_by(
        'category__name'
    )
    context_object_name = 'items'
    template_name = 'catalog/list.html'


class ItemDetailView(DetailView):
    """Страница с одним элементом"""

    model = catalog.models.Item
    queryset = catalog.models.Item.objects.get_item_with_galery()
    template_name = 'catalog/detail.html'


class NewItemListView(ItemListView):
    """страница с товарами, добавленными за последнюю неделю"""
    queryset = catalog.models.Item.objects.get_new_items().order_by(
        'category__name'
    )


class FridayUpdatetItemListView(ItemListView):
    """страница с товарами, обновленными в пятницу"""
    queryset = catalog.models.Item.objects.get_friday_updated_items().order_by(
        'category__name'
    )[:5]


class UncheckedUpdatetItemListView(ItemListView):
    """страница с не обновленными товарами"""
    queryset = catalog.models.Item.objects.get_unchecked_items().order_by(
        'category__name'
    )


class GraderZeroIntItemDetail(View):
    """страница с одним элементом, но регулярное выражение(инт>0)"""
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        return HttpResponse(
            f'<body>{pk}<body>'
        )
