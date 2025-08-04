from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from adminportal.views import is_admin
from .models import Grade
from .forms import GradeForm
from course.models import Course
from student.models import Enrollment


# View to display grades for a student's enrolled courses
@login_required
def student_grades(request):
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status='enrolled'
    ).select_related('course').prefetch_related('grades')  # Prefetch related grades for efficiency
    return render(request, 'grades/student_grades.html', {'enrollments': enrollments}) 

# View to manage grades for a course by the teacher
@login_required
def teacher_course_grades(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollments = Enrollment.objects.filter(
        course=course,
        status='enrolled'
    ).select_related('student').prefetch_related('grades')
    
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        form = GradeForm(request.POST)  # Create a form instance with POST data

        if form.is_valid():
            grade, created = Grade.objects.update_or_create(
                enrollment=enrollment,
                defaults={
                    'grade': form.cleaned_data['grade'],
                    'comment': form.cleaned_data['comment']
                }
            )
            messages.success(request, 'Grade updated successfully')
            return redirect('teacher_course_grades', course_id=course_id)
    
    return render(request, 'grades/teacher_course_grades.html', {
        'course': course,
        'enrollments': enrollments,
        'form': GradeForm()
    })

# Admin view to manage grades for a course
@login_required
@user_passes_test(is_admin)
def admin_course_grades(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(
        course=course,
        status='enrolled'
    ).select_related('student').prefetch_related('grades')
    
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        form = GradeForm(request.POST)
        
        if form.is_valid():
            grade, created = Grade.objects.update_or_create(
                enrollment=enrollment,
                defaults={
                    'grade': form.cleaned_data['grade'],
                    'comment': form.cleaned_data['comment']
                }
            )
            messages.success(request, 'Grade updated successfully')
            return redirect('admin_course_grades', course_id=course_id)
    
    return render(request, 'grades/admin_course_grades.html', {
        'course': course,
        'enrollments': enrollments,
        'form': GradeForm()
    })

