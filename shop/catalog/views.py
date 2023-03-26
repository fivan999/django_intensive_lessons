from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

import catalog.models
import rating.forms
import rating.models


def item_list(request: HttpRequest) -> HttpResponse:
    """Страница со всеми элементами"""
    items = catalog.models.Item.objects.get_published_items().order_by(
        'category__name'
    )
    context = {'items': items}
    return render(request, 'catalog/list.html', context=context)


class ItemDetailView(FormMixin, DetailView):
    model = catalog.models.Item
    form_model = rating.models.Rating
    template_name = 'catalog/detail.html'
    context_object_name = 'item'
    form_class = rating.forms.RatingForm
    get_queryset = catalog.models.Item.objects.get_published_items

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = self.form_class(self.request.POST or None)

        context['grade'] = self.form_model.objects.filter(
            user_id=self.request.user.id,
            item_id=self.kwargs['pk'],
        )
        context['number'] = self.form_model.objects.filter(
            item_id=self.kwargs['pk'],
        ).count()
        context['average'] = round(self.form_model.objects.filter(
            item_id=self.kwargs['pk'],
        ).aggregate(
            Avg('grade')
        )['grade__avg'], 2)

        return context

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            return reverse_lazy(
                'catalog:item_detail',
                kwargs={'pk': kwargs['pk']}
            )
        return reverse_lazy('catalog:item_detail')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            self.form_model.objects.update_or_create(
                user_id=request.user.id,
                item_id=self.kwargs['pk'],
                defaults=form.cleaned_data,
            )

            return redirect(self.get_success_url(**self.kwargs))
        return render(request, self.template_name, self.get_context_data())


def new_items(request: HttpRequest) -> HttpResponse:
    """страница с товарами, добавленными за последнюю неделю"""
    items = catalog.models.Item.objects.get_new_items().order_by(
        'category__name'
    )
    context = {'items': items}
    return render(request, 'catalog/list.html', context=context)


def friday_updatet_items(request: HttpRequest) -> HttpResponse:
    """страница с товарами, обновленными в пятницу"""
    items = catalog.models.Item.objects.get_friday_updated_items().order_by(
        'category__name'
    )[:5]
    context = {'items': items}
    return render(request, 'catalog/list.html', context=context)


def unchecked_items(request: HttpRequest) -> HttpResponse:
    """страница с не обновленными товарами"""
    items = catalog.models.Item.objects.get_unchecked_items().order_by(
        'category__name'
    )
    context = {'items': items}
    return render(request, 'catalog/list.html', context=context)


def grader_zero_int_item_detail(
    request: HttpRequest, item_num: int
) -> HttpResponse:
    """страница с одним элементом, но регулярное выражение(инт>0)"""
    return HttpResponse(f'<body><h1>Подробно элемент {item_num}</h1></body>')
