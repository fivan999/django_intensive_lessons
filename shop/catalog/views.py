import catalog.models

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

import rating.forms
import rating.models


class ItemListView(ListView):
    """Страница со всеми элементами"""
    queryset = catalog.models.Item.objects.get_published_items().order_by(
        'category__name'
    )
    context_object_name = 'items'
    template_name = 'catalog/list.html'


class ItemDetailView(FormMixin, DetailView):
    """подробно товар"""
    model = catalog.models.Item
    form_model = rating.models.Rating
    template_name = 'catalog/detail.html'
    context_object_name = 'item'
    form_class = rating.forms.RatingForm
    queryset = catalog.models.Item.objects.get_published_items()

    def get_context_data(self, *args, **kwargs) -> dict:
        """дополняем контекст"""
        context = super().get_context_data(*args, **kwargs)

        sum_grades, number = 0, 0
        item_grades = rating.models.Rating.objects.filter(
            item_id=self.kwargs['pk']
        ).select_related('user').only('grade', 'user__id', 'user__username')
        minrating, maxrating = 6, 0
        for grade in item_grades:
            sum_grades += grade.grade
            number += 1
            if grade.grade >= maxrating:
                user_maxrating = grade.user.username
                maxrating = grade.grade
            if grade.grade <= minrating:
                user_minrating = grade.user.username
                minrating = grade.grade
            if self.request.user.id == grade.user.id:
                context['user_grade'] = grade

        context['number'] = number
        if number == 0:
            context['average'] = 0
        else:
            context['average'] = sum_grades / number
            context['user_maxrating'] = user_maxrating
            context['user_minrating'] = user_minrating
        return context

    def get_success_url(self, **kwargs):
        """
        перенаправляем полователя после
        успешного заполнения формы
        """
        return reverse_lazy(
            'catalog:item_detail',
            kwargs={'pk': kwargs['pk']}
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """обновляем оценку пользователя"""
        form = self.form_class(request.POST or None)
        if form.is_valid():
            if form.cleaned_data['grade']:
                self.form_model.objects.update_or_create(
                    user_id=request.user.id,
                    item_id=self.kwargs['pk'],
                    defaults=form.cleaned_data,
                )
                messages.success(request, 'Товар оценён')
            else:
                self.form_model.objects.filter(
                    user_id=request.user.id,
                    item_id=self.kwargs['pk']
                ).delete()
                messages.success(request, 'Оценка удалена')
        return redirect(self.get_success_url(**self.kwargs))


class NewItemListView(ItemListView):
    """страница с товарами, добавленными за последнюю неделю"""
    queryset = catalog.models.Item.objects.get_new_items().order_by(
        'category__name'
    )


class FridayUpdatetItemListView(ItemListView):
    """страница с товарами, обновленными в пятницу"""
    queryset = catalog.models.Item.objects.get_friday_updated_items().order_by(
        'category__name'
    )[:5]


class UncheckedUpdatetItemListView(ItemListView):
    """страница с не обновленными товарами"""
    queryset = catalog.models.Item.objects.get_unchecked_items().order_by(
        'category__name'
    )


class GraderZeroIntItemDetail(View):
    """страница с одним элементом, но регулярное выражение(инт>0)"""
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        return HttpResponse(
            f'<body>{pk}<body>'
        )
