# Generated by Django 3.2.16 on 2023-02-28 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagetoitem',
            options={'verbose_name': 'главное изображение', 'verbose_name_plural': 'главные изображения'},
        ),
    ]
