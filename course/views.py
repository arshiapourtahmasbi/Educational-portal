from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from .models import Course, Schedule
from .forms import CourseForm, ScheduleFormSet
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['schedule_formset'] = ScheduleFormSet(self.request.POST)
        else:
            context['schedule_formset'] = ScheduleFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        schedule_formset = context['schedule_formset']
        if schedule_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.teacher = self.request.user
            self.object.save()
            schedule_formset.instance = self.object
            schedule_formset.save()
            return redirect('course_list')
        return self.render_to_response(self.get_context_data(form=form))

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
        
        for new_schedule in new_course.schedules.all():
            for existing_schedule in existing_course.schedules.all():
                if new_schedule.schedule_type == 'date' and existing_schedule.schedule_type == 'date':
                    if existing_schedule.specific_date == new_schedule.specific_date:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1:
                            return True
                
                elif new_schedule.schedule_type == 'weekday' and existing_schedule.schedule_type == 'weekday':
                    if existing_schedule.weekday == new_schedule.weekday:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1:
                            return True
                
                elif new_schedule.schedule_type == 'weekday' and existing_schedule.schedule_type == 'date':
                    if existing_schedule.specific_date and existing_schedule.specific_date.weekday() == new_schedule.weekday:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1:
                            return True
                
                elif new_schedule.schedule_type == 'date' and existing_schedule.schedule_type == 'weekday':
                    if new_schedule.specific_date.weekday() == existing_schedule.weekday:
                        if abs((existing_schedule.time.hour - new_schedule.time.hour)) < 1:
                            return True
    
    return False

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.teacher:
        return render(request, 'courses/error.html', 
                     {'message': 'You do not have permission to edit this course.'})
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        schedule_formset = ScheduleFormSet(request.POST, instance=course)
        
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

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course,
            status='enrolled'
        ).exists()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })


