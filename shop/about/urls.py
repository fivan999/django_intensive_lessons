from django.urls import path
from django.views.generic import TemplateView


app_name = 'about'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='about/about.html'),
        name='about'
    ),
]
