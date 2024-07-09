from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш E-mail'})
    )
    password1 = forms.CharField(
        label='Пароль',
        required=True,
        help_text='Пароль не должен быть коротким (не менее 8 символов)',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите ваш пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if any(char in username for char in '@/_'):
            raise forms.ValidationError('Нельзя вводить символы: @, /, _')
        if len(username.split()) > 1:
            raise forms.ValidationError('Имя пользователя не должно содержать более одного слова')
        return username


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя пользователся',
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш E-mail'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if any(char in username for char in '@/_'):
            raise forms.ValidationError('Нельзя вводить символы: @, /, _')
        if len(username.split()) > 1:
            raise forms.ValidationError('Имя пользователя не должно содержать более одного слова')
        return username


class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Загрузить фото',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-img-control'})
    )

    class Meta:
        model = User
        fields = ['img']

