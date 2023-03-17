from django.urls import path

from feedback import views


app_name = 'feedback'

urlpatterns = [
    path('', views.feedback, name='feedback'),
    path('thanks/', views.thanks_for_feedback, name='thanks'),
]
