from django import forms
from django.forms import inlineformset_factory
from .models import Course, Schedule

# Form for creating and editing courses
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'content', 'capacity', 'pre_requisites', 'price')
        labels = {
            'pre_requisites': 'Prerequisites',
        }
        # Customizing the form fields with CSS classes and placeholders
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Course Description'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed course content, syllabus, and materials'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum Capacity',
                'type': 'number'
            }),
            'pre_requisites': forms.Textarea(attrs={
                
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Prerequisites'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course Price',
                'min': '0',
                'step': '0.01'
            }),
        }

# Form for creating and editing course schedules
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['schedule_type', 'specific_date', 'weekday', 'time']
        widgets = {
            'id': forms.HiddenInput(),
            'schedule_type': forms.Select(attrs={
                'class': 'form-control schedule-type',
            }),
            'specific_date': forms.DateInput(attrs={
                'class': 'form-control specific-date',
                'type': 'date'
            }),
            'weekday': forms.Select(attrs={
                'class': 'form-control weekday'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }

# Inline formset for managing multiple schedules for a course
ScheduleFormSet = inlineformset_factory(
    Course, 
    Schedule,
    form=ScheduleForm,
    extra=1,
    can_delete=True
)

