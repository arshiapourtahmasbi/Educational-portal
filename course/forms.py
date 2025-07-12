from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'date', 'time', 'capacity', 'pre_requisites')  
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Course Description'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Capacity', 'type': 'number'}),
            'pre_requisites': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prerequisites', 'type': 'text'}),
        }
