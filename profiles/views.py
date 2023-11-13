from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm  
from .models import Profile
from checkout.models import Order
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


@login_required
def profile(request):
    user = request.user
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            print("User form errors:", u_form.errors)
            print("Profile form errors:", p_form.errors)

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    orders = Order.objects.filter(user=user).order_by('-date')
    context = {'u_form': u_form, 'p_form': p_form, 'orders': orders}
    return render(request, 'profiles/profiles.html', context)


@login_required

def order_detail(request, order_id):

    """

    View function to display the details of a specific order using the profiles.html template.

    """

    order = get_object_or_404(Order, id=order_id)


    context = {'order': order}

    return render(request, 'profiles.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registered successfully.') 
            return redirect('profile')
        else:
            print("Form is not valid: ", form.errors)  
    else:
        form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'form': form})



def index(request):
    return render(request, 'profiles/profiles.html')


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})