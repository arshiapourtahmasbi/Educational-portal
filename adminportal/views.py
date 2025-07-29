from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from portal.models import User
from .forms import AdminUserEditForm

def is_admin(user):
    return user.is_admin

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_to_edit.username} updated successfully.')
            return redirect('manage_users')
    else:
        form = AdminUserEditForm(instance=user_to_edit)
    
    return render(request, 'admin/edit_user.html', {
        'form': form,
        'user_to_edit': user_to_edit
    })

@login_required
@user_passes_test(is_admin)
def toggle_teacher(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_teacher = not user.is_teacher
        user.save()
        messages.success(request, f'Teacher status updated for {user.username}')
    return redirect('manage_users')

@login_required
@user_passes_test(is_admin)
def toggle_admin(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_admin = not user.is_admin
        user.save()
        messages.success(request, f'Admin status updated for {user.username}')
    return redirect('manage_users')

@login_required
@user_passes_test(is_admin)
def toggle_active(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'Active status updated for {user.username}')
    return redirect('manage_users')