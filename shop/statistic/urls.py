from django.urls import path

from statistic import views


app_name = 'statistic'

urlpatterns = [
    path(
        'user_items/',
        views.ListOfRatedUserItems.as_view(),
        name='user_rated_items'
    ),
    path(
        'user/',
        views.UserRatedStatistics.as_view(),
        name='user_statistics'
    ),
]
