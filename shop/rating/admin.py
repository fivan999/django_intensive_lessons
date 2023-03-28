from django.contrib import admin

import rating.models


@admin.register(rating.models.Rating)
class RatingAdmin(admin.ModelAdmin):
    """отображение модели рейтинг в админке"""

    list_display = ('id', 'get_grade', 'item', 'user')
    list_display_links = ('id',)
