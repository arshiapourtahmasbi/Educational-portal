from django.contrib.auth.models import AbstractUser
from django.db import models

#custom user model for the portal application
#This model extends the AbstractUser to include additional fields
class User(AbstractUser):
    is_teacher = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False) 

# Groups and permissions fields are inherited from AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='portal_user_set', # to avoid conflicts with other apps
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

# User permissions field is also inherited from AbstractUser
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='portal_user_set', # to avoid conflicts with other apps
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

