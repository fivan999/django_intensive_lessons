from catalog.models import Item

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def item_list(request: HttpRequest) -> HttpResponse:
    """Страница со всеми элементами"""
    context = {
        'items': Item.objects.all()
    }
    print(context['items'][0].main_image.image.url)
    return render(request, 'catalog/list.html', context=context)


def item_detail(request: HttpRequest, item_num: int) -> HttpResponse:
    """Страница с одним элементом"""
    return HttpResponse(f'<body><h1>Подробно элемент {item_num}</h1></body>')


def grader_zero_int_item_detail(
    request: HttpRequest, item_num: int
) -> HttpResponse:
    """страница с одним элементом, но регулярное выражение(инт>0)"""
    return HttpResponse(f'<body><h1>Подробно элемент {item_num}</h1></body>')
