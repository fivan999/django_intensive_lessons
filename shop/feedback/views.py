from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import FeedbackForm
from .models import Feedback, FeedbackFile, FeedbackUserData


def feedback(request: HttpRequest) -> HttpResponse:
    """обработчик форма обратной связи"""
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        text = form.cleaned_data['text']
        user_email = form.cleaned_data['email']
        user = FeedbackUserData.objects.filter(email=user_email)
        if user:
            user = user.first()
        else:
            user = FeedbackUserData.objects.create(email=user_email)
        feedback = Feedback.objects.create(text=text, user=user)
        for file in request.FILES.getlist('files'):
            FeedbackFile.objects.create(
                file=file,
                feedback=feedback
            )
        send_mail(
            'Feedback',
            text,
            settings.EMAIL,
            [user_email],
            fail_silently=False
        )
        return redirect('feedback:thanks')
    context = {
        'form': form
    }
    return render(request, 'feedback/feedback.html', context=context)


def thanks_for_feedback(request: HttpRequest) -> HttpResponse:
    """спасибо тебе за фидбек!"""
    return render(request, 'feedback/thanks.html')
