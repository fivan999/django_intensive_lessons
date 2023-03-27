from django import forms

import rating.models


class RatingForm(forms.ModelForm):
    """форма рейтинга"""

    class Meta:
        model = rating.models.Rating
        fields = ('grade',)
        widgets = {
            'grade': forms.widgets.Select(
                attrs={'class': 'form-select'}
            )
        }
