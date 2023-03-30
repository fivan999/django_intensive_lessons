import os
import pathlib
import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback, FeedbackFile

from parameterized import parameterized

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

    feedback_form = FeedbackForm()

    feedback_form_data = {'text': 'hello', 'email': 'testuser2@yandex.ru'}

    def setUp(self) -> None:
        """подготовка к тестированию, создание тестовых данных"""
        self.test_user1 = ShopUser.objects.create(
            email='testuser1@yandex.ru',
            username='testuser1',
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        self.test_user1.set_password('password')
        self.test_user1.save()
        self.test_user2 = ShopUser.objects.create(
            email='testuser2@yandex.ru',
            username='testuser2',
            is_active=True
        )
        self.test_user2.set_password('password')
        self.test_user2.save()
        super().setUp()

    def test_form_not_in_feedback_context(self) -> None:
        """
        тестируем не передачу формы в контекст,
        тк пользователь не авторизован
        """
        response = Client().get(reverse('feedback:feedback'))
        self.assertIsNone(response.context)

    def test_form_in_feedback_context(self) -> None:
        """тестируем передачу формы в контекст"""
        client = Client()
        client.post(
            reverse('users:login'),
            {'username': self.test_user1.username, 'password': 'password'},
        )
        response = client.get(reverse('feedback:feedback'))
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
        response = client.post(
            reverse('users:login'),
            {'username': self.test_user1.username, 'password': 'password'},
        )
        response = client.post(
            reverse('feedback:feedback'), self.feedback_form_data
        )
        self.assertRedirects(response, reverse('feedback:thanks'))

    def test_create_feedback(self) -> None:
        """тестируем создание фидбека"""
        start_count = Feedback.objects.count()
        client = Client()
        client.post(
            reverse('users:login'),
            {'username': self.test_user1.username, 'password': 'password'},
        )
        client.post(reverse('feedback:feedback'), self.feedback_form_data)
        end_count = Feedback.objects.count()
        self.assertEqual(start_count + 1, end_count)

    def test_attach_files_in_feedback(self) -> None:
        """тестируем возможность прикрепить файлы в фидбеке"""
        client = Client()
        self.feedback_form_data['files'] = [
            SimpleUploadedFile('file1.txt', b'aboba'),
        ]
        client.post(
            reverse('users:login'),
            {'username': self.test_user1.username, 'password': 'password'},
        )
        client.post(reverse('feedback:feedback'), self.feedback_form_data)
        file_path = FeedbackFile.objects.get(pk=1).file.path
        self.assertTrue(os.path.isfile(file_path))

    @parameterized.expand([(1,), (2,)])
    def test_admin_can_view_all_feedbacks(self, user_id: int) -> None:
        """админ может посмотреть фидбеки всех пользователей"""
        client = Client()
        client.post(
            reverse('users:login'),
            {'username': self.test_user1.username, 'password': 'password'},
        )
        response = client.get(
            reverse('feedback:user_feedbacks', kwargs={'user_id': user_id})
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        """удаление тестовых данных"""
        ShopUser.objects.all().delete()
        Feedback.objects.all().delete()
        dir_name = str(settings.MEDIA_ROOT) + '/uploads/feedbacks/1'
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
        super().tearDown()
