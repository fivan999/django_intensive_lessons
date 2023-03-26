from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackView.as_view(), name='feedback'),
    path(
        'thanks/',
        login_required(TemplateView.as_view(
            template_name='feedback/thanks.html'
        )),
        name='thanks'
    ),
    path(
        '<int:user_id>/', views.UserFeedbacks.as_view(), name='user_feedbacks'
    ),
]
