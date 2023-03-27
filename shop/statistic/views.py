from catalog.models import Item
from catalog.views import ItemListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, QuerySet

from rating.models import Rating


class ListOfRatedUserItems(LoginRequiredMixin, ItemListView):
    """страница со списком товаров, которые оценил пользователь"""
    queryset = None
    template_name = 'statistic/rated_by_user.html'

    def get_queryset(self) -> QuerySet:
        """получаем нужные записи"""
        return Item.objects.get_published_items().prefetch_related(
            Prefetch(
                'item_rating',
                queryset=Rating.objects.filter(
                    user__id=self.request.user.id
                )
            )
        ).order_by('-item_rating__grade')
