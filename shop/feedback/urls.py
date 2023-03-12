from django.urls import path

from . import views


app_name = 'feedback'

urlpatterns = [
    path('', views.feedback, name='feedback'),
    path('thanks/', views.thanks_for_feedback, name='thanks'),
]
