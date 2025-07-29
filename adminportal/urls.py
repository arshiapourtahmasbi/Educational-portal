from django.urls import path
from . import views

urlpatterns = [
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('toggle-teacher/<int:user_id>/', views.toggle_teacher, name='toggle_teacher'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
    path('toggle-active/<int:user_id>/', views.toggle_active, name='toggle_active'),
]