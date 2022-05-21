from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, News
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.models import ModelForm


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserSignInForm(AuthenticationForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise ValidationError("Fail login")

        return self.cleaned_data


class AddNewsForm(ModelForm):

    class Meta:
        model = News
        fields = ['title', 'summary', 'content']
