from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'content', 'schedule_type', 
                 'specific_date', 'weekday', 'time', 'capacity', 
                 'pre_requisites')
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
            'schedule_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'schedule-type'
            }),
            'specific_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'specific-date'
            }),
            'weekday': forms.Select(attrs={
                'class': 'form-control',
                'id': 'weekday'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
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
        }
