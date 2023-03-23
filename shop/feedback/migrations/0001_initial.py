# Generated by Django 3.2.16 on 2023-03-20 14:11

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст фидбека', verbose_name='текст')),
                ('cretated_on', models.DateTimeField(auto_now_add=True, help_text='Когда отправили фидбек', verbose_name='дата и время создания')),
                ('status', models.CharField(choices=[('получено', 'получено'), ('в обработке', 'в обработке'), ('ответ дан', 'ответ дан')], default='получено', help_text='Статус обработки формы', max_length=100, verbose_name='статус')),
            ],
            options={
                'verbose_name': 'фидбек',
                'verbose_name_plural': 'фидбеки',
                'db_table': 'feedback_feedback',
            },
        ),
        migrations.CreateModel(
            name='FeedbackUserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Электронная почта получателя', max_length=254, verbose_name='электронная почта')),
            ],
            options={
                'verbose_name': 'данные пользователя',
                'db_table': 'feedback_feedbackuserdata',
            },
        ),
        migrations.CreateModel(
            name='FeedbackFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Загрузите файл', upload_to=feedback.models.generate_file_path, verbose_name='файл')),
                ('feedback', models.ForeignKey(help_text='Фидбек, к которому привязан файл', on_delete=django.db.models.deletion.CASCADE, related_name='files', to='feedback.feedback', verbose_name='фидбек')),
            ],
            options={
                'verbose_name': 'файл фидбека',
                'verbose_name_plural': 'файлы фидбека',
                'db_table': 'feedback_feedbackfile',
            },
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(help_text='Пользователь, к которому привязан фидбек', on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='feedback.feedbackuserdata', verbose_name='пользователь'),
        ),
    ]