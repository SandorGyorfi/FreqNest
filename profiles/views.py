from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.db.models import Prefetch
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm  
from .models import Profile
from checkout.models import Order, OrderLineItem
from checkout.signals import update_on_save, update_on_delete
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Profile view
@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            logger.error(f"User form errors: {u_form.errors}")
            logger.error(f"Profile form errors: {p_form.errors}")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    order_lineitems_prefetch = Prefetch('lineitems', queryset=OrderLineItem.objects.all())
    orders = Order.objects.filter(user=user).prefetch_related(order_lineitems_prefetch).order_by('-date')

    context = {'u_form': u_form, 'p_form': p_form, 'orders': orders}
    return render(request, 'profiles/profiles.html', context)

# Order detail view
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'profiles.html', context)

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Registered successfully.') 
                return redirect('profile')
            else:
                messages.error(request, 'Authentication failed after registration.')
                logger.error(f"Authentication failed for user: {username}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            logger.error(f"Registration form errors: {form.errors}")
    else:
        form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'form': form})

# Index view
def index(request):
    return render(request, 'profiles/profiles.html')

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Now logged in.')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
                logger.error(f"Failed login attempt for username: {username}")  
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})

# Custom logout view
class CustomLogoutView(RedirectView):
    url = reverse_lazy('login')  
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Successfully logged out.')
        return super().get(request, *args, **kwargs)    

# Delete account view
@login_required
def delete_account(request):
    user = request.user

    post_save.disconnect(update_on_save, sender=OrderLineItem)
    post_delete.disconnect(update_on_delete, sender=OrderLineItem)

    with transaction.atomic():
        orders = Order.objects.filter(user=user)
        for order in orders:
            order.delete()  

        user.delete()
        messages.success(request, 'Your account has been deleted.')

    post_save.connect(update_on_save, sender=OrderLineItem)
    post_delete.connect(update_on_delete, sender=OrderLineItem)

    logout(request)
    return redirect('login')
