import django.db.models


class Feedback(django.db.models.Model):
    """модель обратной связи"""

    STATUS_CHOICES = [
        ('получено', 'получено'),
        ('в обработке', 'в обработке'),
        ('ответ дан', 'ответ дан'),
    ]

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
    status = django.db.models.CharField(
        verbose_name='статус',
        help_text='Статус обработки формы',
        default='получено',
        choices=STATUS_CHOICES,
        max_length=100
    )

    class Meta:
        verbose_name = 'фидбек'
        verbose_name_plural = 'фидбеки'
        db_table = 'feedback_feedback'
