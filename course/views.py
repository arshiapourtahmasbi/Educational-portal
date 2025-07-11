from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required 
def course_view(request):
    # Placeholder for course view logic
    return HttpResponse("Course view not implemented yet.")

@login_required
def course_management_view(request):
    # Placeholder for course management view logic
    return HttpResponse("Course management view not implemented yet.")