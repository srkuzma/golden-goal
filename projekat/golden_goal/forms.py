# autori:
# Dejan Kovacevic 0167/2019
# Kosta Mladenovic 0283/2019
# Joze Vodnik 0125/2019

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.models import ModelForm


# Klasa koja predstavlja formu za registraciju korisnika
class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Klasa koja predstavlja formu za logovanje korisnika
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


# Klasa koja predstavlja formu dodavanje nove vesti
class AddNewsForm(ModelForm):

    class Meta:
        model = News
        fields = ['title', 'summary', 'content']


# Klasa koja predstavlja formu za azuriranje vesti
class UpdateNewsForm(ModelForm):

    class Meta:
        model = News
        fields = ['title', 'summary', 'content']


# Klasa koja predstavlja formu za pretragu vesti
class SearchNewsForm(forms.Form):
    keyword = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': "form-control",
        'style': 'width: 100%'
    }))


# Klasa koja predstavlja formu za dodavanje komentara
class CommentNews(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
