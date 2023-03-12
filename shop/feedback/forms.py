import django.forms

from .models import Feedback


class FeedbackForm(django.forms.ModelForm):
    """форма для обратной связи"""

    class Meta:
        model = Feedback
        exclude = ('created_on', )
        widgets = {
            'text': django.forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
            'email': django.forms.EmailInput(
                attrs={'class': 'form-control', 'type': 'email'}
            )
        }
