from django.urls import path
from . import views
urlpatterns = [
    path('course/', views.course_view, name='course'),
    path('course/manage/', views.course_management_view, name='course_management'),
]