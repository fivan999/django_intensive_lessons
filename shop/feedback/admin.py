import django.contrib.admin

import feedback.models


class FeedbackFileAdmin(django.contrib.admin.TabularInline):
    """отображение файла фидбека в админке"""

    model = feedback.models.FeedbackFile
    extra = 1


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    """отображение модели Feedback в админке"""

    list_display = ('pk', 'status', 'user')
    list_display_links = ('pk',)
    list_editable = ('status',)
    inlines = (FeedbackFileAdmin,)
