import datetime
import random

from catalog.models import Item

from django.db.models import F
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


def new_items(request: HttpRequest) -> HttpResponse:
    """страница с товарами, добавленными за последнюю неделю"""
    items_ids = Item.objects.filter(
        is_published=True, category__is_published=True
    ).values_list('id', flat=True)
    items = Item.objects.get_published_items().filter(
        created_at__gte=F('created_at') - datetime.timedelta(days=7),
        id__in=random.sample(list(items_ids), 5)
    ).only(
        'name', 'text', 'main_image__image', 'category__name'
    ).order_by(
        'category__name'
    )
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def friday_updatet_items(request: HttpRequest) -> HttpResponse:
    """страница с товарами, обновленными в пятницу"""
    items = Item.objects.get_published_items().filter(
        updated_at__week_day=6
    ).only(
        'name', 'text', 'main_image__image', 'category__name'
    ).order_by(
        'category__name'
    )[:5]
    context = {
        'items': items
    }
    return render(request, 'catalog/list.html', context=context)


def unchecked_items(request: HttpRequest) -> HttpResponse:
    """страница с не обновленными товарами"""
    items = Item.objects.get_published_items().filter(
        created_at=F('updated_at')
    ).only(
        'name', 'text', 'main_image__image', 'category__name'
    ).order_by(
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
