import catalog.models

import django.contrib.admin

import rating.models


class ImageToItemAdmin(django.contrib.admin.TabularInline):
    """отображение главной картинки в админке"""
    model = catalog.models.ImageToItem


class GaleryToItemAdmin(django.contrib.admin.TabularInline):
    """отображение галереи в админке"""
    model = catalog.models.GaleryToItem
    extra = 1


class RatingInline(django.contrib.admin.TabularInline):
    """отображение модели рейтинга в админке"""
    model = rating.models.Rating


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    """отображение модели Item в админке"""

    list_display = (
        'name',
        'is_published',
        'image_thumb',
    )
    inlines = (
        ImageToItemAdmin,
        GaleryToItemAdmin,
        RatingInline,
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
        'weight',
    )
    list_editable = ('is_published',)
    list_display_links = ('name',)
