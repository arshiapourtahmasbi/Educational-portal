from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from student.models import Enrollment  
from django.contrib import messages

class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'courses/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

@method_decorator(login_required, name='dispatch')
class CreateCourseView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create_course.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.teacher = self.request.user
        course.save()
        return redirect('course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
@login_required
def remove_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        if request.user == course.teacher:
            course.delete()
            return redirect('course_list')
        else:
            return render(request, 'courses/error.html', {'message': 'You do not have permission to delete this course.'})
    except Course.DoesNotExist:
        return render(request, 'courses/error.html', {'message': 'Course not found.'})

@login_required
def enrolled_students(request, course_id):
    # Get course and verify teacher permission
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.teacher:
        return render(request, 'courses/error.html', 
                     {'message': 'You do not have permission to view this course\'s enrollments.'})
    
    # Get all active enrollments for the course
    enrollments = course.enrollments.filter(   # type: ignore
        status='enrolled'
    ).select_related('student')
    
    return render(request, 'courses/enrolled_students.html', {
        'course': course,
        'enrollments': enrollments
    })

def check_schedule_conflict(user, new_course):
    existing_enrollments = Enrollment.objects.filter(
        student=user,
        status='enrolled'
    ).select_related('course')
    
    for enrollment in existing_enrollments:
        existing_course = enrollment.course
        
        if new_course.schedule_type == 'date' and existing_course.schedule_type == 'date':
            # Check date conflict
            if existing_course.specific_date == new_course.specific_date:
                if abs((existing_course.time.hour - new_course.time.hour)) < 1:
                    return True
        
        elif new_course.schedule_type == 'weekday' and existing_course.schedule_type == 'weekday':
            # Check weekday conflict
            if existing_course.weekday == new_course.weekday:
                if abs((existing_course.time.hour - new_course.time.hour)) < 1:
                    return True
        
        elif new_course.schedule_type == 'weekday' and existing_course.schedule_type == 'date':
            # Check if the specific date falls on the same weekday
            if existing_course.specific_date is not None and existing_course.specific_date.weekday() == new_course.weekday:
                if abs((existing_course.time.hour - new_course.time.hour)) < 1:
                    return True
        
        elif new_course.schedule_type == 'date' and existing_course.schedule_type == 'weekday':
            # Check if the specific date falls on the same weekday
            if new_course.specific_date.weekday() == existing_course.weekday:
                if abs((existing_course.time.hour - new_course.time.hour)) < 1:
                    return True
    
    return False

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is the course teacher
    if request.user != course.teacher:
        return render(request, 'courses/error.html', 
                     {'message': 'You do not have permission to edit this course.'})
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {
        'form': form,
        'course': course
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {
        'course': course
    })


