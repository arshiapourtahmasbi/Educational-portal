from django import forms
from .models import Grade

# GradeForm for creating and updating grades
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade', 'comment']
        widgets = {
            'grade': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'min': '0',
                'max': '20',
                'placeholder': 'Enter grade (0-20)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add comments about the grade'
            })
        }

# Validation for the grade field to ensure it is within the range of 0 to 20
    def clean_grade(self):
        grade = self.cleaned_data.get('grade') # Get the grade from cleaned data
        if grade is not None:
            if grade < 0:
                raise forms.ValidationError("Grade cannot be less than 0")
            if grade > 20:
                raise forms.ValidationError("Grade cannot be more than 20")
        return grade