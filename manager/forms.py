from django import forms
from .models import *
from django.core.validators import RegexValidator

        
class LoginForm(forms.Form):
    
    username_attrs = {
        'id':'username',
        'name': 'username',
        'class': 'form-control',
        'id':'username',
        'placeholder':"Username"
    }
    
    password_attrs = {
        'id':'password',
        'name':'password',
        'class':'form-control',
        'id':'password',
        'placeholder':"************"
    }
        
    username = forms.CharField(label='', widget=forms.TextInput(attrs=username_attrs))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs=password_attrs))
        
class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['upload']

