from django.http import HttpRequest, HttpResponse


def item_list(request: HttpRequest) -> HttpResponse:
    """Страница со всеми элементами"""
    return HttpResponse('<body><h1>Список элементов</h1></body>')


def item_detail(request: HttpRequest, item_num: int) -> HttpResponse:
    """Страница с одним элементом"""
    return HttpResponse(f'<body><h1>Подобно элемент {item_num}</h1></body>')
