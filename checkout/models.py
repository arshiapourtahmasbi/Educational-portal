from django.db import models
from django.conf import settings
from course.models import Course
from decimal import Decimal

# Cart model to manage user's shopping cart
class Cart(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    courses = models.ManyToManyField(Course)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Method to calculate total price of courses in the cart
    def total_price(self):
        return sum(course.price for course in self.courses.all())

# Payment model to manage payments for courses
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'), #First item is the value, second is the display name
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # ForeignKey to the user model
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # ForeignKey to the course model
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Amount for the payment
    payment_date = models.DateTimeField(auto_now_add=True) # Date when the payment was made
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending') # Status of the payment
    transaction_id = models.CharField(max_length=100, blank=True, null=True) # Transaction ID for the payment

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.status}"
