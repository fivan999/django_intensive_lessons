from django.urls import path, re_path, register_converter

from . import converters
from . import views


register_converter(converters.GraderZeroIntConverter, 'grader_zero_int')

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:item_num>/', views.item_detail, name='item_detail'),
    re_path(
        r'^re/(?P<item_num>[1-9][0-9]*)/$',
        views.grader_zero_int_item_detail,
    ),
    path(
        'converter/<grader_zero_int:item_num>/',
        views.grader_zero_int_item_detail,
    ),
]
