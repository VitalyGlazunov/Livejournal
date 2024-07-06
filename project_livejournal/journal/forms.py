from django import forms
from .models import Comment, Article


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


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='Название',
        required=True,
    )
    category = forms.ChoiceField(
        label='Рубрика',
        choices=Article.CATEGORY_CHOICES,
        required=True,
    )
    description = forms.CharField(
        label='Описание',
        required=True,
        widget=forms.Textarea,
    )
    text = forms.CharField(
        label='Основной текст',
        required=True,
        widget=forms.Textarea,
    )
    publication = forms.BooleanField(
        label='Статус публикации',
        required=False,
    )
    img = forms.ImageField(
        label='Превью',
        required=False,
        widget=forms.FileInput
    )

    class Meta:
        model = Article
        fields = ['title', 'category', 'description', 'text', 'publication', 'img']
