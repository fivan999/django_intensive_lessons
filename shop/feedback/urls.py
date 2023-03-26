from django.urls import path

from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackView.as_view(), name='feedback'),
    path('thanks/', views.ThanksForFeedback.as_view(), name='thanks'),
    path(
        '<int:user_id>/', views.UserFeedbacks.as_view(), name='user_feedbacks'
    ),
]
