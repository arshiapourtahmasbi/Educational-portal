from django.db import models
from django.conf import settings
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from student.models import Enrollment

# Define the Course model with necessary fields
class Schedule(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Saturday'),
        (1, 'Sunday'),
        (2, 'Monday'),
        (3, 'Tuesday'),
        (4, 'Wednesday'),
        (5, 'Thursday'),
        (6, 'Friday'),
        
    ]

# Define the schedule type choices
# first element is the value stored in the database, second is the human-readable name
    SCHEDULE_TYPE_CHOICES = [
        ('date', 'Specific Date'),
        ('weekday', 'Weekly Schedule'),
    ]

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='schedules') # ForeignKey to Course model
    # Schedule type field with choices
    schedule_type = models.CharField(
        max_length=7, # Length of 'weekday' is 7, 'date' is 4
        choices=SCHEDULE_TYPE_CHOICES, # Choices for schedule type
        default='date' # Default to 'date' type if not specified
    )
    specific_date = models.DateField(null=True, blank=True) 
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, null=True, blank=True) 
    time = models.TimeField()

# Define the string representation of the Schedule model
    def get_schedule_display(self):
        if self.schedule_type == 'date': 
            if self.specific_date:
                return f"On {self.specific_date.strftime('%Y-%m-%d')} at {self.time.strftime('%H:%M')}" # Format date and time
            return "Date not set"
        elif self.schedule_type == 'weekday':
            if self.weekday is not None:
                return f"Every {self.get_weekday_display()} at {self.time.strftime('%H:%M')}" # Format weekday and time
            return "Weekday not set"
        return "No schedule set"

    # Method to get the display name of the weekday
    def get_weekday_display(self):
        for value, display in self.WEEKDAY_CHOICES:
            if self.weekday == value:
                return display
        return "Unknown"

# Define the Course model
class Course(models.Model):
    title = models.CharField(max_length=200) 
    description = models.TextField()
    content = models.TextField(help_text="Detailed course content and materials")
    # ForeignKey to the User model with a limit to teachers only
    teacher = models.ForeignKey( 
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},
    )
    capacity = models.PositiveIntegerField() 
    pre_requisites = models.TextField(blank=True, null=True)  #allow pre-requisites to be empty
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        
    )

    def __str__(self):
        return self.title