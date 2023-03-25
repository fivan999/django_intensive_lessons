# Generated by Django 3.2.16 on 2023-03-22 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='cleaned_email',
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='email',
            field=models.EmailField(
                blank=True,
                max_length=100,
                unique=True,
                verbose_name='email address',
            ),
        ),
    ]
