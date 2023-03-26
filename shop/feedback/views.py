from typing import Union

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FeedbackView(LoginRequiredMixin, FormView):
    """страница с отправкой фидбека"""

    template_name = 'feedback/feedback.html'
    success_url = reverse_lazy('feedback:thanks')
    form_class = FeedbackForm

    def form_valid(self, form: FeedbackForm) -> HttpResponse:
        """отправляем сообщение если форма валидная"""
        send_mail(
            'Feedback',
            form.cleaned_data['text'],
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        form.save(self.request.FILES)
        return super().form_valid(form)


class UserFeedbacks(LoginRequiredMixin, ListView):
    """отображение списка фидбеков юзера"""

    model = Feedback
    template_name = 'feedback/list.html'
    context_object_name = 'feedbacks'
    allow_empty = True

    def dispatch(
        self, request: HttpRequest, *args, **kwargs
    ) -> Union[Http404, HttpResponse]:
        """проверка на соответствие user_id"""
        if (
            request.user.id != self.kwargs['user_id']
            and not request.user.is_staff
        ):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """получаем нужные фидбеки"""
        return (
            Feedback.objects.filter(user__id=self.kwargs['user_id'])
            .prefetch_related('files')
            .only('text', 'created_on', 'status')
        )


class ThanksForFeedback(LoginRequiredMixin, TemplateView):
    """спасибо тебе за фидбек!"""

    template_name = 'feedback/thanks.html'
