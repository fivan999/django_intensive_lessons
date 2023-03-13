from django.test import Client, TestCase
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback


class FormsTest(TestCase):
    """тестируем формы"""

    feedback_form_data = {
        'text': 'Письмо админу',
        'email': 'aboba@ya.ru',
        'status': 'получено'
    }

    def setUp(self) -> None:
        self.feedback_form = FeedbackForm()
        super().setUp()

    def test_form_in_feedback_context(self) -> None:
        """тестируем передачу формы в контекст"""
        response = Client().get(reverse('feedback:feedback'))
        self.assertIn('form', response.context)

    def test_feedback_form_correct_text_label(self) -> None:
        """тестируем корректный label у текста"""
        label_text = self.feedback_form.fields['text'].label
        self.assertEqual(label_text, 'Текст')

    def test_feedback_form_correct_email_label(self) -> None:
        """тестируем корректный label у email"""
        label_text = self.feedback_form.fields['email'].label
        self.assertEqual(label_text, 'Электронная почта')

    def test_feedback_form_correct_text_help_text(self) -> None:
        """тестируем корректный help_text у текста"""
        help_text = self.feedback_form.fields['text'].help_text
        self.assertEqual(help_text, 'Введите текст письма')

    def test_feedback_form_correct_email_help_text(self) -> None:
        """тестируем корректный help_text у email"""
        help_text = self.feedback_form.fields['email'].help_text
        self.assertEqual(help_text, 'Электронная почта получателя')

    def test_feedback_form_redirects_to_thanks(self) -> None:
        """тестируем редирект на страницу с благодарностью"""
        response = Client().post(
            reverse('feedback:feedback'),
            self.feedback_form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('feedback:thanks'))

    def test_create_feedback(self) -> None:
        """тестируем создание фидбека"""
        start_count = Feedback.objects.count()
        Client().post(
            reverse('feedback:feedback'),
            self.feedback_form_data
        )
        end_count = Feedback.objects.count()
        self.assertEqual(start_count + 1, end_count)
