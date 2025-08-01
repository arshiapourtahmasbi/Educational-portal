from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from portal.models import User
from .forms import AdminUserEditForm
from course.models import Course
from student.models import Enrollment
from django.db.models import Q

def is_admin(user):
    return user.is_admin

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_to_edit.username} updated successfully.')
            return redirect('manage_users')
    else:
        form = AdminUserEditForm(instance=user_to_edit)
    
    return render(request, 'admin/edit_user.html', {
        'form': form,
        'user_to_edit': user_to_edit
    })

@login_required
@user_passes_test(is_admin)
def toggle_teacher(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_teacher = not user.is_teacher
        user.save()
        messages.success(request, f'Teacher status updated for {user.username}')
    return redirect('manage_users')

@login_required
@user_passes_test(is_admin)
def toggle_admin(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_admin = not user.is_admin
        user.save()
        messages.success(request, f'Admin status updated for {user.username}')
    return redirect('manage_users')

@login_required
@user_passes_test(is_admin)
def toggle_active(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'Active status updated for {user.username}')
    return redirect('manage_users')

@login_required
@user_passes_test(is_admin)
def manage_course_enrollments(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Get enrolled students
    enrolled_students = Enrollment.objects.filter(
        course=course,
        status='enrolled'
    ).select_related('student')
    
    # Get available students (not enrolled in this course)
    enrolled_student_ids = enrolled_students.values_list('student_id', flat=True)
    available_students = User.objects.exclude(
        Q(id__in=enrolled_student_ids) | Q(is_teacher=True) | Q(is_admin=True)
    )
    
    return render(request, 'admin/manage_course_enrollments.html', {
        'course': course,
        'enrolled_students': enrolled_students,
        'available_students': available_students,
    })

@login_required
@user_passes_test(is_admin)
def admin_add_student(request, course_id, student_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(User, id=student_id)
        
        # Check if course has capacity
        if course.capacity <= 0:
            messages.error(request, 'Course is at maximum capacity')
            return redirect('manage_course_enrollments', course_id=course_id)
        
        # Try to get existing enrollment or create new one
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={'status': 'enrolled'}
        )
        
        # If enrollment existed but was dropped, update it
        if not created and enrollment.status == 'dropped':
            enrollment.status = 'enrolled'
            enrollment.save()
            
            # Update course capacity
            course.capacity -= 1
            course.save()
            
            messages.success(
                request, 
                f'Successfully re-enrolled {student.username} in {course.title}'
            )
        elif created:
            # Update course capacity for new enrollment
            course.capacity -= 1
            course.save()
            
            messages.success(
                request, 
                f'Successfully added {student.username} to {course.title}'
            )
        else:
            messages.warning(
                request,
                f'{student.username} is already enrolled in {course.title}'
            )
    
    return redirect('manage_course_enrollments', course_id=course_id)

@login_required
@user_passes_test(is_admin)
def admin_remove_student(request, course_id, student_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(User, id=student_id)
        
        # Update enrollment status
        enrollment = get_object_or_404(
            Enrollment,
            course=course,
            student=student,
            status='enrolled'
        )
        enrollment.status = 'dropped'
        enrollment.save()
        
        # Update course capacity
        course.capacity += 1
        course.save()
        
        messages.success(
            request, 
            f'Successfully removed {student.username} from {course.title}'
        )
    
    return redirect('manage_course_enrollments', course_id=course_id)

@login_required
@user_passes_test(is_admin)
def admin_manage_courses(request):
    courses = Course.objects.all().select_related('teacher')
    return render(request, 'admin/manage_courses.html', {
        'courses': courses
    })

@login_required
@user_passes_test(is_admin)
def admin_delete_account(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # Check if user is not a teacher or admin
        if user.is_teacher or user.is_admin:
            messages.error(request, 'Cannot delete a teacher or admin account.')
            return redirect('manage_users')
        
        # Delete the user account
        user.delete()
        messages.success(request, f'User {user.username} deleted successfully.')
    
    return redirect('manage_users')