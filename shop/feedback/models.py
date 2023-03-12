import django.db.models


class Feedback(django.db.models.Model):
    """модель обратной связи"""

    text = django.db.models.TextField(
        verbose_name='текст',
        help_text='Введите текст письма'
    )
    cretated_on = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name='дата и время создания',
        help_text='Когда отправили фидбек'
    )
    email = django.db.models.EmailField(
        verbose_name='электронная почта',
        help_text='Электронная почта получателя'
    )

    class Meta:
        verbose_name = 'фидбек'
        verbose_name_plural = 'фидбеки'
