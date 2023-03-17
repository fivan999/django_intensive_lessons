from catalog import converters
from catalog import views

from django.urls import path, re_path, register_converter


register_converter(converters.GraderZeroIntConverter, 'grader_zero_int')

app_name = 'catalog'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:item_num>/', views.item_detail, name='item_detail'),
    path('new/', views.new_items, name='new_items'),
    path(
        'friday/', views.friday_updatet_items, name='updated_at_friday_items'
    ),
    path('unchecked/', views.unchecked_items, name='unchecked_items'),
    re_path(
        r'^re/(?P<item_num>[1-9][0-9]*)/$',
        views.grader_zero_int_item_detail,
    ),
    path(
        'converter/<grader_zero_int:item_num>/',
        views.grader_zero_int_item_detail,
    ),
]
