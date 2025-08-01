from django.urls import path
from . import views

urlpatterns = [
    path('grades/', views.student_grades, name='student_grades'),
    path('course/<int:course_id>/grades/', 
         views.teacher_course_grades, 
         name='teacher_course_grades'),
    path('adminpanel/course/<int:course_id>/grades/', 
         views.admin_course_grades, 
         name='admin_course_grades'),


]