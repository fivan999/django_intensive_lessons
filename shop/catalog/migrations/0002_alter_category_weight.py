# Generated by Django 3.2.16 on 2023-02-19 11:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='weight',
            field=models.PositiveSmallIntegerField(default=100, help_text='Введите вес товара (положительное целое число от 0 до 32767)', validators=[django.core.validators.MaxValueValidator(32767)], verbose_name='Вес'),
        ),
    ]