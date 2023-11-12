from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Profile

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.user.order_set.all()  
    return render(request, 'profiles/profile.html', {'form': form, 'orders': orders})