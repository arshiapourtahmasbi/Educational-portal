
from django.urls import path
from . import views

urlpatterns = [
    # The root path of the app, e.g., http://127.0.0.1:8000/
    path('', views.home_view, name='home'),

    # The student's main dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # A page to view all available courses
    path('courses/', views.CourseListView.as_view(), name='course-list'),
]