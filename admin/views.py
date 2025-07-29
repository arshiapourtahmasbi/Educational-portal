from django.shortcuts import render

# Create your views here.
def manage_users(request):
    # Logic to manage users will go here
    return render(request, 'admin/manage_users.html')