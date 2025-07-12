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

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    is_teacher = forms.BooleanField(required=False, help_text='Check if you are a teacher.')
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('email', 'is_teacher', 'first_name', 'last_name', 'username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Handle is_teacher if it's a field on User or related profile
        if hasattr(user, 'is_teacher'):
            user.is_teacher = self.cleaned_data['is_teacher']
        if commit:
            user.save()
        return user
