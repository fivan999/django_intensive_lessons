from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import FeedbackForm
from .models import Feedback


def feedback(request: HttpRequest) -> HttpResponse:
    """обработчик форма обратной связи"""
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        text = form.cleaned_data['text']
        user_email = form.cleaned_data['email']
        status = form.cleaned_data['status']
        email_text = f'{text}\nСтатус: {status}'
        send_mail(
            'Feedback',
            email_text,
            settings.EMAIL,
            [user_email],
            fail_silently=False
        )
        Feedback.objects.create(
            text=text,
            email=user_email,
            status=status
        )
        return redirect('feedback:thanks')
    context = {
        'form': form
    }
    return render(request, 'feedback/feedback.html', context=context)


def thanks_for_feedback(request: HttpRequest) -> HttpResponse:
    """спасибо тебе за фидбек!"""
    return render(request, 'feedback/thanks.html')
