import catalog.models

from django.db import models

import users.models


class Rating(models.Model):
    """модель рейтинга"""

    class Grades(models.IntegerChoices):
        HATE = 1, 'Ненависть'
        DISAFECTION = 2, 'Неприязнь'
        NORMAL = 3, 'Нейтрально'
        ADORATION = 4, 'Обожание'
        LOVE = 5, 'Любовь'

    grade = models.IntegerField(
        'оценка',
        choices=Grades.choices,
        blank=True,
        help_text='Оцените товар',
        default=5
    )
    user = models.ForeignKey(
        users.models.ShopUser,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='user_rating',
        help_text='пользователь, который оставил рейтинг'
    )
    item = models.ForeignKey(
        catalog.models.Item,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='item_rating',
        help_text='товар, к которому относится рейтинг',
    )

    class Meta:
        unique_together = ('user', 'item')
        verbose_name = 'рейтинг'
        verbose_name_plural = 'рейтинги'

    def __str__(self) -> str:
        """строковое представление"""
        return self.get_grade()

    def get_grade(self) -> str:
        """строковое представление оценки"""
        return self.Grades(self.grade).label
