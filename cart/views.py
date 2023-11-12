from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from synths.models import Product



def view_cart(request):


    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):


    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart', {})

    if item_id in cart:
        cart[item_id] += quantity
        messages.success(request, f'{product.name} Updated quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} Added to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)