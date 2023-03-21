from django import forms
from .models import *
from django.core.validators import RegexValidator
from django.forms import ModelForm

        
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

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'number', 'country_code', 'wayra_investment', 'investors', 'founders']
        """
        widgets = {
            'investors': TextInput(),
            'founders': TextInput()
        }
        """

class AddNewUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            # 'password': forms.PasswordInput(),
        }
        help_texts = { 'first_name': None, 'last_name': None, 'email': None}
    # username = forms.CharField(label="Email")
    password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [ # validates that the input matches the requirements
            RegexValidator(
                regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message = 'Password must contain an uppercase character, a lowercase character and a number'
            ),
        ]
    )
    password_confirmation = forms.CharField(label = 'Password Confirmation', widget = forms.PasswordInput())

    def clean(self): # checks if the password matches the confirm password
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirmatiuon = self.cleaned_data.get('password_confirmation')
        if password != password_confirmatiuon:
            self.add_error('password_confirmation', 'Confirmation password does not match the password.') # creates an erro

    def save(self): # creates a new user
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('email'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            password = self.cleaned_data.get('password'),
            user_type = 1
        )
        return

