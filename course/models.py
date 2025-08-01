from django.db import models
from django.conf import settings
from decimal import Decimal

class Schedule(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    SCHEDULE_TYPE_CHOICES = [
        ('date', 'Specific Date'),
        ('weekday', 'Weekly Schedule'),
    ]

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='schedules')
    schedule_type = models.CharField(
        max_length=7,
        choices=SCHEDULE_TYPE_CHOICES,
        default='date'
    )
    specific_date = models.DateField(null=True, blank=True)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, null=True, blank=True)
    time = models.TimeField()

    def get_schedule_display(self):
        if self.schedule_type == 'date':
            if self.specific_date:
                return f"On {self.specific_date.strftime('%Y-%m-%d')} at {self.time.strftime('%H:%M')}"
            return "Date not set"
        elif self.schedule_type == 'weekday':
            if self.weekday is not None:
                return f"Every {self.get_weekday_display()} at {self.time.strftime('%H:%M')}"
            return "Weekday not set"
        return "No schedule set"

    def get_weekday_display(self):
        for value, display in self.WEEKDAY_CHOICES:
            if self.weekday == value:
                return display
        return "Unknown"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField(help_text="Detailed course content and materials")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},
    )
    capacity = models.PositiveIntegerField()
    pre_requisites = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Course price in USD"
    )

    def __str__(self):
        return self.title