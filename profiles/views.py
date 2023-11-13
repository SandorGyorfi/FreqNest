from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Profile
from checkout.models import Order
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm

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

    orders = Order.objects.filter(user=request.user)

    context = {
        'form': form,
        'orders': orders  
    }
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  
    else:
        form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'form': form})

def index(request):
    return render(request, 'shop/index.html')