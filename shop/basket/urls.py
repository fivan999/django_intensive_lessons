from basket import views

from django.urls import path


app_name = 'basket'

urlpatterns = [
    path('', views.UserBasketView.as_view(), name='basket'),
    path('<int:pk>/', views.BasketDetailView.as_view(), name='item_detail'),
    path(
        'delete/<int:pk>/',
        views.DeleteFromBasketView.as_view(),
        name='delete'
    ),
    path(
        'add/<int:pk>/',
        views.AddToBasketView.as_view(),
        name='add'
    ),
]
