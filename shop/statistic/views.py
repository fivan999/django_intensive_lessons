from catalog.models import Item
from catalog.views import ItemListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, QuerySet


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
