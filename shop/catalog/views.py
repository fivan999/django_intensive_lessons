from catalog.models import Item

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render


def item_list(request: HttpRequest) -> HttpResponse:
    """Страница со всеми элементами"""
    items = Item.objects.get_published_items().only(
        'name', 'text', 'main_image__image', 'category__name'
    ).order_by(
        'category__name'
    )
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def item_detail(request: HttpRequest, item_num: int) -> HttpResponse:
    """Страница с одним элементом"""
    item = get_object_or_404(
        Item.objects.get_published_items().prefetch_related(
            'galery'
        ).only(
            'category__name', 'name', 'text', 'main_image__image'
        ),
        pk=item_num
    )
    context = {
        'item': item
    }
    return render(request, 'catalog/detail.html', context=context)


def grader_zero_int_item_detail(
    request: HttpRequest, item_num: int
) -> HttpResponse:
    """страница с одним элементом, но регулярное выражение(инт>0)"""
    return HttpResponse(f'<body><h1>Подробно элемент {item_num}</h1></body>')
