from django.urls import re_path

from . import views


app_name = 'download'

urlpatterns = [
    re_path(
        r'(?P<file_name>.*)/$',
        views.download_image,
        name='download_image'
    ),
]
