from django.urls import path, re_path, register_converter

from catalog import converters, views


register_converter(converters.GraderZeroIntConverter, 'grader_zero_int')

app_name = 'catalog'

urlpatterns = [
    path(
        '',
        views.ItemListView.as_view(),
        name='item_list'
    ),
    path(
        '<int:pk>/',
        views.ItemDetailView.as_view(),
        name='item_detail'
    ),
    path(
        'new/',
        views.NewItemListView.as_view(),
        name='new_items'
    ),
    path(
        'friday/',
        views.FridayUpdatetItemListView.as_view(),
        name='updated_at_friday_items'
    ),
    path(
        'unchecked/',
        views.UncheckedUpdatetItemListView.as_view(),
        name='unchecked_items'
    ),
    re_path(
        r'^re/(?P<pk>[1-9][0-9]*)/$',
        views.GraderZeroIntItemDetail.as_view(),
    ),
    path(
        'converter/<grader_zero_int:pk>/',
        views.GraderZeroIntItemDetail.as_view(),
    ),
]
