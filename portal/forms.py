from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    is_teacher = forms.BooleanField(required=False, help_text='Check if you are a teacher.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_teacher')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)