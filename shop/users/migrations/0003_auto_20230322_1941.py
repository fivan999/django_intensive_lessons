# Generated by Django 3.2.16 on 2023-03-22 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230322_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='datetime_blocked',
            field=models.DateTimeField(blank=True, help_text='Дата и время блокировки за попытки входа', null=True, verbose_name='дата и время блокировки'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='unsuccesful_login',
            field=models.IntegerField(default=0, help_text='Количество неудачных попыток входа в аккаунт', verbose_name='неудачные попытки'),
        ),
    ]
