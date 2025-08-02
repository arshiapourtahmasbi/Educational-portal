from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from course.models import Course
from .models import Payment, Cart
from student.models import Enrollment
from course.views import check_schedule_conflict
from decimal import Decimal
from course.models import Course


@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is already enrolled
    if Enrollment.objects.filter(student=request.user, course=course, status='enrolled').exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('my_courses')
    
    if course.capacity <= 0:
        messages.error(request, 'This course is full.')
        return redirect('course_list')
    
    # Check for schedule conflicts with enrolled courses
    if check_schedule_conflict(request.user, course):
        messages.error(request, f'Schedule conflict detected with your enrolled courses.')
        return redirect('course_list')
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(student=request.user)
    
    # Check for conflicts with courses already in cart
    for cart_course in cart.courses.all():
        for new_schedule in course.schedules.all(): # pyright: ignore[reportAttributeAccessIssue]
            for existing_schedule in cart_course.schedules.all():
                # Check date schedules
                if new_schedule.schedule_type == 'date' and existing_schedule.schedule_type == 'date':
                    if existing_schedule.specific_date == new_schedule.specific_date:
                        if abs(existing_schedule.time.hour - new_schedule.time.hour) < 1:
                            messages.error(request, f'Schedule conflict detected with {cart_course.title} in your cart.')
                            return redirect('view_cart')
                
                # Check weekday schedules
                elif new_schedule.schedule_type == 'weekday' and existing_schedule.schedule_type == 'weekday':
                    if existing_schedule.weekday == new_schedule.weekday:
                        if abs(existing_schedule.time.hour - new_schedule.time.hour) < 1:
                            messages.error(request, f'Schedule conflict detected with {cart_course.title} in your cart.')
                            return redirect('view_cart')
    
    cart.courses.add(course)
    messages.success(request, f'{course.title} added to cart.')
    return redirect('view_cart')

@login_required
def remove_from_cart(request, course_id):
    cart = Cart.objects.filter(student=request.user).first()
    if cart:
        course = get_object_or_404(Course, id=course_id)
        cart.courses.remove(course)
        messages.success(request, f'{course.title} removed from cart.')
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(student=request.user).first()
    context = {
        'cart': cart,
        'total_price': cart.total_price() if cart else Decimal('0.00')
    }
    return render(request, 'checkout/cart.html', context)

@login_required
def checkout(request):
    cart = Cart.objects.filter(student=request.user).first()
    if not cart or cart.courses.count() == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('course_list')
    
    # Check for schedule conflicts
    for course in cart.courses.all():
        if check_schedule_conflict(request.user, course):
            messages.error(request, f'Schedule conflict detected for {course.title}')
            return redirect('view_cart')
    
    context = {
        'cart': cart,
        'total_price': cart.total_price()
    }
    return render(request, 'checkout/checkout.html', context)

@login_required
def process_payment(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(student=request.user).first()
        if not cart or cart.courses.count() == 0:
            messages.error(request, 'Cart is empty')
            return redirect('course_list')
        
        # For debugging - simulate payment success/failure
        payment_status = request.POST.get('payment_status', 'failed')
        
        if payment_status == 'success':
            # Create enrollment for each course
            for course in cart.courses.all():
                # Check if enrollment exists and update it if needed
                enrollment, created = Enrollment.objects.get_or_create(
                    student=request.user,
                    course=course,
                    defaults={'status': 'enrolled'}
                )
                
                # If enrollment existed but was dropped, reactivate it
                if not created and enrollment.status == 'dropped':
                    enrollment.status = 'enrolled'
                    enrollment.save()
                
                # Only update capacity for new enrollments
                if created or enrollment.status == 'dropped':
                    # Update course capacity
                    course.capacity -= 1
                    course.save()
                
                # Create payment record
                Payment.objects.create(
                    student=request.user,
                    course=course,
                    amount=course.price,
                    status='completed'
                )
            
            # Clear cart
            cart.delete()
            messages.success(request, 'Payment successful! You are now enrolled in the selected courses.')
            return redirect('payment_success')
        else:
            messages.error(request, 'Payment failed. Please try again.')
            return redirect('payment_failed')
    
    return redirect('checkout')

@login_required
def payment_success(request):
    return render(request, 'checkout/payment_success.html')

@login_required
def payment_failed(request):
    return render(request, 'checkout/payment_failed.html')
