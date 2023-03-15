import django.forms


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
