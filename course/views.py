from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    

