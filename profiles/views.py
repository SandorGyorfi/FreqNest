from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Profile

@login_required
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None
        messages.info(request, "Profile not found. Please create a profile.")

    if request.method == 'POST' and user_profile:
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            print("Form errors:", form.errors) 
    else:
        form = UserProfileForm(instance=user_profile) if user_profile else UserProfileForm()

    context = {
        'form': form
    }

    if user_profile:
        orders = user_profile.user.order_set.all()
        print("Orders:", orders)  
        context['orders'] = orders
    else:
        context['orders'] = []

    return render(request, 'profiles/profiles.html', context)
