import datetime
import random

import catalog.models

import django.db.models


class ItemManager(django.db.models.Manager):
    def get_published_items(self) -> django.db.models.QuerySet:
        """возвращаем опубликованные товары"""
        return self.get_only_useful_fields().filter(
            is_published=True, category__is_published=True
        )

    def get_items_on_main(self) -> django.db.models.QuerySet:
        """опубликованные товары на главноq странице"""
        return self.get_published_items().filter(is_on_main=True)

    def get_item_with_galery(self) -> django.db.models.QuerySet:
        """опубликованный товар с галереей"""
        return self.get_published_items().prefetch_related('galery')

    def get_new_items(self) -> django.db.models.QuerySet:
        """5 рандомных товаров, добавленных за последнюю неделю"""
        item_ids = self.get_queryset().filter(
            is_published=True, category__is_published=True
        ).values_list('id', flat=True)
        return self.get_published_items().filter(
            created_at__gte=django.db.models.F(
                'created_at'
            ) - datetime.timedelta(days=7),
            id__in=random.sample(list(item_ids), 5)
        )

    def get_friday_updated_items(self) -> django.db.models.QuerySet:
        """товары обновленные в пятницу"""
        return self.get_published_items().filter(updated_at__week_day=6)

    def get_unchecked_items(self) -> django.db.models.QuerySet:
        """не обновленные товары"""
        return self.get_published_items().filter(
            created_at=django.db.models.F('updated_at')
        )

    def get_only_useful_fields(self) -> django.db.models.QuerySet:
        """только нужные поля"""
        return self.get_queryset().select_related(
            'main_image', 'category'
        ).prefetch_related(
            django.db.models.Prefetch(
                'tags',
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True
                ).only('name')
            )
        ).only(
            'name', 'text', 'main_image__image', 'category__name'
        )
