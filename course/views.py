from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import Course, Schedule
from .forms import CourseForm, ScheduleFormSet
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from student.models import Enrollment  
from django.contrib import messages

# Course views for managing courses, schedules, and enrollments
# ListView to display all courses
class CourseListView(ListView):
    model = Course
    context_object_name = 'courses' # Name of the context variable to hold the list of courses
    template_name = 'courses/course_list.html'

# ListView to display all courses ordered by creation date
    def get_queryset(self):
        return Course.objects.order_by('-created_at')

# ListView to display courses created by the logged-in user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context (django provides)
        context['user'] = self.request.user  # Add the logged-in user to the context
        return context  # Return the updated context


# CreateView for creating a new course
@method_decorator(login_required, name='dispatch') # Ensure that only logged-in users can access this view. dispatch is a method that handles the request and returns a response.
class CreateCourseView(CreateView):
    model = Course # The model to use for this view
    form_class = CourseForm # The form class to use for creating a new course
    template_name = 'courses/create_course.html' # The template to use for rendering the view
    

    def get_context_data(self, **kwargs): # Get the context data for the view
        context = super().get_context_data(**kwargs) # Get the default context (django provides)
        if self.request.POST:
            context['schedule_formset'] = ScheduleFormSet(self.request.POST) # If the request is a POST request, create a ScheduleFormSet with the POST data
        else:
            context['schedule_formset'] = ScheduleFormSet() # If the request is a GET request, create an empty ScheduleFormSet

        return context

    def form_valid(self, form): # Method to handle the form submission when the form is valid
        context = self.get_context_data() 
        schedule_formset = context['schedule_formset'] # Get the ScheduleFormSet from the context
        if schedule_formset.is_valid(): # Check if the ScheduleFormSet is valid
            self.object = form.save(commit=False)
            self.object.teacher = self.request.user
            self.object.save()
            schedule_formset.instance = self.object
            schedule_formset.save()
            return redirect('course_list')
        return self.render_to_response(self.get_context_data(form=form)) # If the form is not valid, render the form again with the errors

# View to remove a course
@login_required
def remove_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id) # get the course by id
        if request.user == course.teacher or request.user.is_admin:
            course.delete()
            if request.user.is_admin:
                return redirect('admin_manage_courses')
            return redirect('course_list')
        else:
            return render(request, 'courses/error.html', {'message': 'You do not have permission to delete this course.'})
    except Course.DoesNotExist:
        return render(request, 'courses/error.html', {'message': 'Course not found.'})

# View to enroll in a course
@login_required
def enrolled_students(request, course_id):
    # Get course and verify teacher permission
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.teacher:
        return render(request, 'courses/error.html', 
                     {'message': 'You do not have permission to view this course\'s enrollments.'})
    
    # Get all active enrollments for the course
    enrollments = course.enrollments.filter(    # type: ignore 
        status='enrolled'
    ).select_related('student')
    
    return render(request, 'courses/enrolled_students.html', {
        'course': course,
        'enrollments': enrollments
    })

# check if a new course schedule conflicts with existing enrollments
def check_schedule_conflict(user, new_course):
    existing_enrollments = Enrollment.objects.filter(
        student=user,
        status='enrolled'
    ).select_related('course')
    
    for enrollment in existing_enrollments:
        existing_course = enrollment.course
        
        for new_schedule in new_course.schedules.all():
            for existing_schedule in existing_course.schedules.all():  # type: ignore
                if new_schedule.schedule_type == 'date' and existing_schedule.schedule_type == 'date': 
                    if existing_schedule.specific_date == new_schedule.specific_date: # Check if the specific dates are the same
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1:    # Check if the time difference is less than 1 hour
                            return True
                
                elif new_schedule.schedule_type == 'weekday' and existing_schedule.schedule_type == 'weekday':
                    if existing_schedule.weekday == new_schedule.weekday:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1: # Check if the time difference is less than 1 hour
                            return True
                
                elif new_schedule.schedule_type == 'weekday' and existing_schedule.schedule_type == 'date':
                    if existing_schedule.specific_date and existing_schedule.specific_date.weekday() == new_schedule.weekday:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1: # Check if the time difference is less than 1 hour
                            return True
                
                elif new_schedule.schedule_type == 'date' and existing_schedule.schedule_type == 'weekday':
                    if new_schedule.specific_date.weekday() == existing_schedule.weekday:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1: # Check if the time difference is less than 1 hour
                            return True
    
    return False

# View to edit a course
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.teacher and not request.user.is_admin: # Check if the user is the teacher of the course or an admin
        messages.error(request, 'You do not have permission to edit this course.')
        return redirect('course_list')
        
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course) # Create a form instance with POST data and the course instance
        schedule_formset = ScheduleFormSet(request.POST, instance=course) # Create a schedule formset instance with POST data and the course instance   
        
        if form.is_valid() and schedule_formset.is_valid():
            form.save()
            schedule_formset.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course) 
        schedule_formset = ScheduleFormSet(instance=course)
    
    return render(request, 'courses/edit_course.html', {
        'form': form,
        'schedule_formset': schedule_formset,
        'course': course
    })

# View to display details of a course
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id) # Get the course by id or return 404 if not found
    is_enrolled = False # Default to not enrolled
    if request.user.is_authenticated: # Check if the user is authenticated
        # Check if the user is enrolled in the course
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course,
            status='enrolled'
        ).exists()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })


# View to display courses created by the logged-in user
@login_required
def view_created_courses(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'courses/created_courses.html', {
        'courses': courses
    })