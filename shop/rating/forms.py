from django import forms

import rating.models


class RatingForm(forms.ModelForm):
    """форма рейтинга"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].empty_label = None

    class Meta:
        model = rating.models.Rating
        fields = (
            rating.models.Rating.grade.field.name,
        )
        widgets = {
            'grade': forms.widgets.Select(
                attrs={'class': 'form-select'}
            )
        }
