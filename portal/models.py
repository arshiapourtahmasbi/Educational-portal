
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model to differentiate between students and teachers.
    """
    is_teacher = models.BooleanField('teacher status', default=False)