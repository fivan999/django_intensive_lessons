from django import forms

import rating.models


class RatingForm(forms.ModelForm):
    """форма рейтинга"""

    class Meta:
        model = rating.models.Rating
        fields = (
            rating.models.Rating.grade.field.name,
        )
