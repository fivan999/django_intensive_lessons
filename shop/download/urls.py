from django.urls import re_path

from download.views import DownloadImageView

app_name = 'download'

urlpatterns = [
    re_path(
        r'(?P<file_name>.*)/$',
        DownloadImageView.as_view(),
        name='download_image'
    ),
]
