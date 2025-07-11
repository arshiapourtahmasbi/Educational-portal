from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Student

def home_view(request):
    """
    Redirects authenticated users to their dashboard.
    Redirects unauthenticated users to the login page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def dashboard_view(request):
    """
    Displays the main dashboard for a logged-in user.
    For students, it shows their enrolled courses.
    """
    # Check if the logged-in user is a student
    try:
        student = request.user.student
        enrolled_courses = student.enrolled_courses.all()
        context = {
            'student': student,
            'courses': enrolled_courses
        }
        return render(request, 'portal/dashboard.html', context)
    except Student.DoesNotExist:
        # Handle cases where the user is not a student (e.g., a teacher or admin)
        # For now, we'll just render a simple message.
        return render(request, 'portal/dashboard_non_student.html')


class CourseListView(LoginRequiredMixin, ListView):
    """
    A class-based view to display a list of all available courses.
    """
    model = Course
    template_name = 'portal/course_list.html'
    context_object_name = 'courses'