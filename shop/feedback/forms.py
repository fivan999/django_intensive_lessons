import django.forms
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDict

from feedback.models import Feedback, FeedbackFile

import users.models


class FeedbackForm(django.forms.Form):
    """форма для обратной связи"""

    text = django.forms.CharField(
        widget=django.forms.Textarea(
            attrs={'class': 'form-control', 'rows': 4}
        ),
        label='Текст',
        help_text='Введите текст фидбека',
    )
    email = django.forms.EmailField(
        widget=django.forms.EmailInput(attrs={'class': 'form-control'}),
        label='Почта',
        help_text='Введите почту получателя',
    )
    files = django.forms.FileField(
        widget=django.forms.ClearableFileInput(
            attrs={'class': 'form-control', 'multiple': True}
        ),
        required=False,
        label='Файл',
        help_text='Загрузите файл',
    )

    def clean_email(self) -> None:
        """валидируем email"""
        if users.models.ShopUser.objects.filter(
            email=self.cleaned_data['email']
        ).exists():
            return self.cleaned_data['email']
        raise ValidationError('Пользователя с таким email не существует')

    def save(self, files: MultiValueDict) -> None:
        """сохраняем форму"""
        text = self.cleaned_data['text']
        user_email = self.cleaned_data['email']

        user = users.models.ShopUser.objects.get(email=user_email)

        feedback = Feedback.objects.create(text=text, user=user)

        for file in files.getlist('files'):
            FeedbackFile.objects.create(file=file, feedback=feedback)
