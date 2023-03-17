import django.forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.datastructures import MultiValueDict

from feedback.models import Feedback, FeedbackFile, FeedbackUserData


class FeedbackForm(django.forms.Form):
    """форма для обратной связи"""

    text = django.forms.CharField(
        widget=django.forms.Textarea(
            attrs={'class': 'form-control', 'rows': 4}
        ),
        label='Текст',
        help_text='Введите текст фидбека'
    )
    email = django.forms.EmailField(
        widget=django.forms.EmailInput(
            attrs={'class': 'form-control'}
        ),
        label='Почта',
        help_text='Введите почту получателя'
    )
    files = django.forms.FileField(
        widget=django.forms.ClearableFileInput(
            attrs={'class': 'form-control', 'multiple': True}
        ),
        required=False,
        label='Файл',
        help_text='Загрузите файл'
    )

    def save(self, files: MultiValueDict) -> None:
        """сохраняем форму"""
        text = self.cleaned_data['text']
        user_email = self.cleaned_data['email']

        user = FeedbackUserData.objects.filter(email=user_email)
        if user:
            user = user.first()
        else:
            user = FeedbackUserData.objects.create(email=user_email)

        feedback = Feedback.objects.create(text=text, user=user)

        for file in files.getlist('files'):
            FeedbackFile.objects.create(file=file, feedback=feedback)
