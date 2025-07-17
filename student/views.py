from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from course.models import Course
from .models import Enrollment
from django.db.models import Q

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if student is already enrolled
    if Enrollment.objects.filter(
        student=request.user, 
        course=course, 
        status='enrolled'
    ).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('my_courses')
    
    # Check for time conflicts with existing enrollments
    existing_enrollments = Enrollment.objects.filter(
        student=request.user,
        status='enrolled'
    ).select_related('course')
    
    for enrollment in existing_enrollments:
        if enrollment.course.date == course.date:  # If same day
            existing_start = enrollment.course.time
            new_start = course.time
            
            # Assuming each course is 1 hour long
            if abs((existing_start.hour - new_start.hour)) < 1:
                messages.error(
                    request,
                    f'Time conflict with your enrolled course: {enrollment.course.title}'
                )
                return redirect('course_list')
    
    # If student previously dropped the course, update the existing record
    previous_enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status='dropped'
    ).first()
    
    if previous_enrollment:
        previous_enrollment.status = 'enrolled'
        previous_enrollment.save()
    else:
        # Create new enrollment if no previous record exists
        Enrollment.objects.create(student=request.user, course=course)
    
    # Update course capacity
    course.capacity -= 1
    course.save()
    
    messages.success(request, f'Successfully enrolled in {course.title}')
    return redirect('my_courses')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status='enrolled'
    ).select_related('course')
    return render(request, 'student/my_courses.html', {'enrollments': enrollments})

@login_required
def drop_course(request, course_id):
    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course_id=course_id,
        status='enrolled'
    )
    enrollment.status = 'dropped'
    enrollment.save()
    
    # Increase course capacity when student drops
    course = enrollment.course
    course.capacity += 1
    course.save()
    
    messages.success(request, f'Successfully dropped {enrollment.course.title}')
    return redirect('my_courses')