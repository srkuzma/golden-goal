from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError


class Usercreationform(UserCreationForm):

    class Meta:
        model = User
        fields= ['username','password1' , 'password2']

