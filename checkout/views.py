from django.contrib.auth.decorators import login_required  
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import os
import json
from .models import Order, OrderLineItem, Product
from .forms import OrderForm
from cart.contexts import cart_contents




@login_required  
def checkout(request):
    """
    Handles the checkout process. If the request method is POST, it processes the order form and saves the order.
    If the request method is GET, it displays the checkout page.
    """
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item_id, quantity in cart.items():
                product = Product.objects.get(id=item_id)
                OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                ).save()

            del request.session['cart']
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error processing your order. Please try again.")

    cart = request.session.get('cart', {})
    if not cart:
        return redirect(reverse('products'))

    current_cart = cart_contents(request)
    total = current_cart['grand_total']

    order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'total': total,  
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handles the checkout success page. It retrieves the order and displays the success page.
    """
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
    }
    return render(request, 'checkout/checkout_success.html', context)


@csrf_exempt  
def save_order(request):
    """
    Handles the saving of an order. If the request method is POST, it processes the order data and saves the order.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('orderData'))
            items = data['items']
            total_price = data['totalPrice']

            order = Order(total=total_price) 
            order.save()

            for item_name in items:
                product, created = Product.objects.get_or_create(name=item_name) 
                OrderLineItem.objects.create(order=order, product=product)  

            return JsonResponse({'status': 'success', 'message': 'Order saved successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error processing order: {str(e)}'}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def stripe_public_key(request):
    """
    Returns the Stripe public key.
    """
    public_key = os.environ.get('STRIPE_PUBLIC_KEY', '')  
    return JsonResponse({'publicKey': public_key})
