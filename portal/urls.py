from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Add more paths for other views as needed
    path('signup/', views.signup, name='signup'),
    # This will handle the signup view
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),


    path('logout/', views.logout_view, name='logout'),


]