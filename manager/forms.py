from django import forms
from .models import *
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())