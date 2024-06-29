from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'no-resize',
                    'cols': 140,
                    'rows': 3,
                    "placeholder": "Введите комментарий",
                }
            ),
        }


