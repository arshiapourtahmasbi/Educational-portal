from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from student.models import Enrollment

class Grade(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, 
        on_delete=models.CASCADE,
        related_name='grades'
    )
    grade = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, message="Grade cannot be less than 0"),
            MaxValueValidator(20.00, message="Grade cannot be more than 20")
        ],
        help_text="Grade must be between 0 and 20"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.enrollment.course.title} - {self.grade}"

    class Meta:
        unique_together = ['enrollment']
