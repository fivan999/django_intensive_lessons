import secrets

import django.db.models

from transliterate import translit

import users.models


def generate_file_path(obj: django.db.models.Model, filename: str) -> str:
    """путь к файлу"""
    filename = translit(filename, 'ru', reversed=True)
    filename = (
        filename[:filename.rfind('.')]
        + secrets.token_hex(6)
        + filename[filename.rfind('.'):]
    )
    return f'uploads/{obj.feedback.pk}/{filename}'


class Feedback(django.db.models.Model):
    """модель обратной связи"""

    STATUS_CHOICES = [
        ('получено', 'получено'),
        ('в обработке', 'в обработке'),
        ('ответ дан', 'ответ дан'),
    ]

    text = django.db.models.TextField(
        verbose_name='текст',
        help_text='Введите текст фидбека'
    )
    cretated_on = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата и время создания',
        help_text='Когда отправили фидбек'
    )
    status = django.db.models.CharField(
        verbose_name='статус',
        help_text='Статус обработки формы',
        default='получено',
        choices=STATUS_CHOICES,
        max_length=100
    )
    user = django.db.models.ForeignKey(
        users.models.ShopUser,
        on_delete=django.db.models.CASCADE,
        verbose_name='пользователь',
        help_text='Пользователь, к которому привязан фидбек',
        related_name='feedbacks'
    )

    class Meta:
        verbose_name = 'фидбек'
        verbose_name_plural = 'фидбеки'
        db_table = 'feedback_feedback'


class FeedbackFile(django.db.models.Model):
    """модель файла для фидбека"""

    file = django.db.models.FileField(
        verbose_name='файл',
        help_text='Загрузите файл',
        upload_to=generate_file_path
    )
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        verbose_name='фидбек',
        help_text='Фидбек, к которому привязан файл',
        related_name='files'
    )

    class Meta:
        verbose_name = 'файл фидбека'
        verbose_name_plural = 'файлы фидбека'
        db_table = 'feedback_feedbackfile'

    def __str__(self) -> str:
        """строковое представление файла фидбека"""
        return f'Файл фидбека {self.pk}'
