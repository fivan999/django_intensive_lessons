from django.db import models

import catalog.models
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
        null=True,
    )

    user = models.ForeignKey(
        users.models.ShopUser,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
        related_name='user_rating',
    )
    item = models.ForeignKey(
        catalog.models.Item,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='item_rating',
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
