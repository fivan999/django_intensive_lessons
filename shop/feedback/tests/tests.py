import os
import pathlib
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback, FeedbackFile

from users.models import ShopUser


@override_settings(
    MEDIA_ROOT=os.path.join(
        os.path.join(
            pathlib.Path(__name__).resolve().parent, 'feedback/tests/test_data'
        )
    )
)
class FormsTest(TestCase):
    """тестируем формы"""

    fixtures = ['fixtures/tests/feedback_tests.json', ]

    feedback_form = FeedbackForm()

    feedback_form_data = {
        'text': 'hello',
        'email': 'testuser@yandex.ru'
    }

    def tearDown(self) -> None:
        """удаление тестовых данных"""
        Feedback.objects.all().delete()
        dir_name = str(settings.MEDIA_ROOT) + '/uploads/feedbacks/1'
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
        super().tearDown()

    def test_user_can_not_give_feedback(self) -> None:
        """
        обычный пользователь не может давать фидбеки,
        будет редирект на страницу входа в админку
        """
        client = Client()
        user = ShopUser.objects.get(pk=2)
        client.post(
            reverse('users:login'),
            {
                'username': user.username,
                'password': 'mutter77'
            },
            follow=True
        )
        response = client.get(reverse('feedback:feedback'))
        self.assertEqual(response.url, '/admin/login/?next=/feedback/')

    def test_form_in_feedback_context(self) -> None:
        """тестируем передачу формы в контекст"""
        client = Client()
        user = ShopUser.objects.get(pk=1)
        response = client.post(
            reverse('users:login'),
            {
                'username': user.username,
                'password': 'mutter77'
            }
        )
        self.assertEqual(response.context['user'], 1)
        self.assertIn('form', response.context)

    def test_feedback_form_correct_text_label(self) -> None:
        """тестируем корректный label у текста"""
        label_text = self.feedback_form.fields['text'].label
        self.assertEqual(label_text, 'Текст')

    def test_feedback_form_correct_email_label(self) -> None:
        """тестируем корректный label у email"""
        label_text = self.feedback_form.fields['email'].label
        self.assertEqual(label_text, 'Почта')

    def test_feedback_form_correct_text_help_text(self) -> None:
        """тестируем корректный help_text у текста"""
        help_text = self.feedback_form.fields['text'].help_text
        self.assertEqual(help_text, 'Введите текст фидбека')

    def test_feedback_form_correct_email_help_text(self) -> None:
        """тестируем корректный help_text у email"""
        help_text = self.feedback_form.fields['email'].help_text
        self.assertEqual(help_text, 'Введите почту получателя')

    def test_feedback_form_redirects_to_thanks(self) -> None:
        """тестируем редирект на страницу с благодарностью"""
        client = Client()
        user = ShopUser.objects.get(pk=1)
        response = client.post(
            reverse('users:login'),
            {
                'username': user.username,
                'password': 'mutter77'
            }
        )
        response = client.post(
            reverse('feedback:feedback'),
            self.feedback_form_data
        )
        self.assertRedirects(response, reverse('feedback:thanks'))

    def test_create_feedback(self) -> None:
        """тестируем создание фидбека"""
        start_count = Feedback.objects.count()
        client = Client()
        user = ShopUser.objects.get(pk=1)
        client.post(
            reverse('users:login'),
            {
                'username': user.username,
                'password': 'mutter77'
            }
        )
        client.post(
            reverse('feedback:feedback'),
            self.feedback_form_data
        )
        end_count = Feedback.objects.count()
        self.assertEqual(start_count + 1, end_count)

    def test_attach_files_in_feedback(self) -> None:
        """тестируем возможность прикрепить файлы в фидбеке"""
        client = Client()
        self.feedback_form_data['files'] = [
            SimpleUploadedFile('file1.txt', b'aboba'),
            SimpleUploadedFile('file2.txt', b'bebra')
        ]
        response = client.post(
            reverse('feedback:feedback'),
            self.feedback_form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_attached_feedback_files_exists(self) -> None:
        """проверяем, существуют ли прикрепленные файлы"""
        self.feedback_form_data['files'] = [
            SimpleUploadedFile('file1.txt', b'aboba')
        ]
        Client().post(
            reverse('feedback:feedback'),
            self.feedback_form_data,
            follow=True
        )
        file_path = FeedbackFile.objects.get(pk=1).file.path
        self.assertTrue(os.path.isfile(file_path))
