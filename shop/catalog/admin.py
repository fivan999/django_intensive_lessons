import catalog.models

import django.contrib.admin


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    """отображение модели Item в админке"""

    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    list_display_links = ('name',)
    filter_horizontal = ('tags',)


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    """отображение модели Tag в админке"""

    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    list_display_links = ('name',)


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    """отображение модели Category в админке"""
    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    list_display_links = ('name',)
