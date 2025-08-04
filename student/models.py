from django.db import models
from django.conf import settings
from course.models import Course 

# Enrollment model for students in courses
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Reference to the user model
        on_delete=models.CASCADE, # Deletes all enrollments if the user is deleted
        related_name='enrollments' # Allows access to a user's enrollments
    )
    # Foreign key to the Course model
    course = models.ForeignKey(
        Course, # Reference to the Course model
        on_delete=models.CASCADE, # Deletes all enrollments if the course is deleted
        related_name='enrollments'  # Allows access to a course's enrollments
    )
    # Enrollment date and status
    enrollment_date = models.DateTimeField(auto_now_add=True) # Automatically set to the current date/time when created
    status = models.CharField(
        max_length=20,
        choices=[
            ('enrolled', 'Enrolled'),
            ('completed', 'Completed'),
            ('dropped', 'Dropped'),
        ],
        default='enrolled'
    )

    # Meta options for the model
    # Ensures that a student can't enroll in the same course twice
    class Meta:
        unique_together = ['student', 'course']

    # String representation of the enrollment for easy debugging
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"