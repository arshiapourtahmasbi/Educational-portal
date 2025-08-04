from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import User from local models

# Portal forms for user registration and login
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    is_teacher = forms.BooleanField(required=False, help_text='Check if you are a teacher.')
    is_admin = forms.BooleanField(required=False, help_text='Check if you are an administrator.')

# Meta class to specify the model and fields
    class Meta:
        model = User # Use the custom User model
        fields = ('username', 'email', 'password1', 'password2', 'is_teacher', 'is_admin') # Include is_teacher and is_admin in the form

# Login form for user authentication
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# Edit profile form for updating user information
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    is_teacher = forms.BooleanField(required=False, help_text='Check if you are a teacher.')
    is_admin = forms.BooleanField(required=False, help_text='Check if you are an administrator.')
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

# Meta class to specify the model and fields
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'is_teacher', 'is_admin')

# Validation to ensure passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

# Save method to handle user creation or update
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
                
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Set custom fields if they exist
        if hasattr(user, 'is_teacher'):
            user.is_teacher = self.cleaned_data['is_teacher']
        if hasattr(user, 'is_admin'):
            user.is_admin = self.cleaned_data['is_admin']
        if commit:
            user.save()
        return user
