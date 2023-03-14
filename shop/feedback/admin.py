import django.contrib.admin

from .models import Feedback


@django.contrib.admin.register(Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    """отображение модели Feedback в админке"""
    list_display = ('pk', 'status',)
    list_display_links = ('pk',)
    list_editable = ('status',)
