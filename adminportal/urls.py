from django.urls import path
from . import views

urlpatterns = [
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('toggle-teacher/<int:user_id>/', views.toggle_teacher, name='toggle_teacher'),
    path('toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
    path('toggle-active/<int:user_id>/', views.toggle_active, name='toggle_active'),
    path('course/<int:course_id>/enrollments/', 
         views.manage_course_enrollments, 
         name='manage_course_enrollments'),
    path('course/<int:course_id>/add-student/<int:student_id>/',
         views.admin_add_student,
         name='admin_add_student'),
    path('course/<int:course_id>/remove-student/<int:student_id>/',
         views.admin_remove_student,
         name='admin_remove_student'),
    path('manage-courses/', views.admin_manage_courses, name='admin_manage_courses'),
    path('delete-account/<int:user_id>/',
         views.admin_delete_account, name='admin_delete_account')
]