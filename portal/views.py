from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import SignUpForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm



def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            if user.is_teacher:
                user.is_teacher = True
            else:
                user.is_teacher = False
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:   
                login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']
            if hasattr(user, 'is_teacher'):
                user.is_teacher = form.cleaned_data['is_teacher']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('profile')
    else:
        form = EditProfileForm()
    return render(request, 'profile.html', {'form': form})