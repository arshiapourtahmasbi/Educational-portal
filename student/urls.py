from django.urls import path
from . import views

urlpatterns = [
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('drop/<int:course_id>/', views.drop_course, name='drop_course'),
    path('course-content/<int:course_id>/', views.view_course_content, name='view_course_content'),
]