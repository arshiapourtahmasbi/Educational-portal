from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    """
    Model to store teacher information.
    Links to the built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Course(models.Model):
    """
    Model for courses offered in the portal.
    """
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

class Student(models.Model):
    """
    Model to store student information.
    Links to the built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    enrolled_courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Enrollment(models.Model):
    """
    Through model to connect Students and Courses.
    This allows for storing extra information about the enrollment itself.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course') # Ensures a student can only enroll in a course once.

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"