from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def description(request: HttpRequest) -> HttpResponse:
    """Страница с информацией о проекте"""
    return render(request, 'about/about.html')
