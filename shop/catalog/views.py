import catalog.models

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render


def item_list(request: HttpRequest) -> HttpResponse:
    """Страница со всеми элементами"""
    items = catalog.models.Item.objects.get_published_items().order_by(
        'category__name'
    )
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def item_detail(request: HttpRequest, item_num: int) -> HttpResponse:
    """Страница с одним элементом"""
    item = get_object_or_404(
        catalog.models.Item.objects.get_item_with_galery(),
        pk=item_num
    )
    context = {
        'item': item
    }
    return render(request, 'catalog/detail.html', context=context)


def new_items(request: HttpRequest) -> HttpResponse:
    """страница с товарами, добавленными за последнюю неделю"""
    items = catalog.models.Item.objects.get_new_items().order_by(
        'category__name'
    )
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def friday_updatet_items(request: HttpRequest) -> HttpResponse:
    """страница с товарами, обновленными в пятницу"""
    items = catalog.models.Item.objects.get_friday_updated_items().order_by(
        'category__name'
    )[:5]
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def unchecked_items(request: HttpRequest) -> HttpResponse:
    """страница с не обновленными товарами"""
    items = catalog.models.Item.objects.get_unchecked_items().order_by(
        'category__name'
    )
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def grader_zero_int_item_detail(
    request: HttpRequest, item_num: int
) -> HttpResponse:
    """страница с одним элементом, но регулярное выражение(инт>0)"""
    return HttpResponse(f'<body><h1>Подробно элемент {item_num}</h1></body>')
