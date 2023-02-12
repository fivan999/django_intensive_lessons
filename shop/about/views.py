from django.http import HttpRequest, HttpResponse


def description(request: HttpRequest) -> HttpResponse:
    """Страница с информацией о проекте"""
    return HttpResponse('<body><h1>О проекте</h1></body>')
