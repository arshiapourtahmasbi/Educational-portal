from datetime import date
from django.db import models
from django.conf import settings


# Create your models here.

class Course(models.Model):
    """
    Represents a course created by a teacher.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()  
    time = models.TimeField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title