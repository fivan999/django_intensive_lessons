from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('catalog/', include('catalog.urls')),
    path('about/', include('about.urls')),
    path('download/', include('download.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('feedback/', include('feedback.urls')),
    path('statistic/', include('statistic.urls')),
    path('basket/', include('basket.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    if settings.MEDIA_ROOT:
        urlpatterns += static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
    else:
        urlpatterns += staticfiles_urlpatterns()
