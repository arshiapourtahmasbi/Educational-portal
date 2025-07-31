from django.urls import path
from . import views

urlpatterns = [
    path('course/', views.CourseListView.as_view(), name='course'),
    path('create/', views.CreateCourseView.as_view(), name='create_course'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
    path('remove/<int:course_id>/', views.remove_course, name='remove_course'),
    path('enrolled-students/<int:course_id>/', views.enrolled_students, name='enrolled_students'), 
    path('edit/<int:course_id>/', views.edit_course, name='edit_course'),
]