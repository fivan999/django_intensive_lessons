from django.urls import path

from homepage import views

app_name = 'homepage'

urlpatterns = [
    path(
        '',
        views.HomeItemListView.as_view(),
        name='homepage'
    ),
    path(
        'coffee/',
        views.CoffeeView.as_view(),
        name='coffee'
    ),
]
