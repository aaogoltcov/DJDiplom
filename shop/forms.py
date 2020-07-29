from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ReviewForm(forms.Form):
    person_name = forms.CharField(label='Ваше имя')
    description = forms.CharField(label='Отзыв')
    score = forms.CharField(label='Оценка')


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        label="Email",
        max_length=60,
        required=True,
        help_text=True,
    )
    password1 = forms.CharField(
        label="Придумайте пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=True,
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=True,
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )