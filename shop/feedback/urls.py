from django.urls import path

from feedback import views


app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackView.as_view(), name='feedback'),
    path('thanks/', views.thanks_for_feedback, name='thanks'),
    path(
        '<int:user_id>/', views.UserFeedbacks.as_view(), name='user_feedbacks'
    ),
]
