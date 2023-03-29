from catalog.models import Item
from catalog.views import ItemListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch, Q, QuerySet
from django.shortcuts import render
from django.views.generic import View

from rating.models import Rating


class ListOfRatedUserItems(LoginRequiredMixin, ItemListView):
    """страница со списком товаров, которые оценил пользователь"""
    queryset = None
    template_name = 'statistic/rated_by_user.html'

    def get_queryset(self) -> QuerySet:
        """получаем нужные записи"""
        return Item.objects.get_published_items().prefetch_related().annotate(
            cnt_rates=Count
            (
                'item_rating__id',
                filter=Q(
                    item_rating__user__id=self.request.user.id
                )
            )
        ).filter(cnt_rates__gt=0).order_by('-item_rating__grade')


class UserRatedStatistics(LoginRequiredMixin, View):
    """статистика пользователя по оценкам"""

    def get(self, request) -> dict:
        """метод get"""
        context = {}

        sum_grades = 0

        user_grades = Rating.objects.filter(
            user_id=self.request.user.id
        ).prefetch_related(
            Prefetch(
                'item',
                queryset=Item.objects.get_only_useful_fields()
            )
        ).only(
            'grade',
            'item__id',
            'item__name',
            'item__text',
            'item__category__name',
            'item__tags__name'
        )

        min_rating = 6
        max_rating = 0

        for grade in user_grades:
            sum_grades += grade.grade
            if grade.grade >= max_rating:
                item_card_max_rating = grade.item
                max_rating = grade.grade
            if grade.grade <= min_rating:
                item_card_min_rating = grade.item
                min_rating = grade.grade

        count_user_grades = len(user_grades)
        context['count_user_grades'] = count_user_grades

        if count_user_grades == 0:
            context['average'] = 0
        else:
            context['average'] = sum_grades / count_user_grades
            context['item_card_max_rating'] = item_card_max_rating
            context['item_card_min_rating'] = item_card_min_rating
            context['max_rating'] = max_rating
            context['min_rating'] = min_rating

        template_name = 'statistic/user_statistics.html'
        return render(request, template_name, context=context)
