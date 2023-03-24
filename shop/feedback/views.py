from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


@staff_member_required
def feedback(request: HttpRequest) -> HttpResponse:
    """обработчик форма обратной связи"""
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        send_mail(
            'Feedback',
            form.cleaned_data['text'],
            settings.EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False
        )
        form.save(request.FILES)
        return redirect('feedback:thanks')
    context = {
        'form': form
    }
    return render(request, 'feedback/feedback.html', context=context)


def thanks_for_feedback(request: HttpRequest) -> HttpResponse:
    """спасибо тебе за фидбек!"""
    return render(request, 'feedback/thanks.html')
