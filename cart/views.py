from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from synths.models import Product

# View Cart
def view_cart(request):
    return render(request, 'cart/cart.html')

# Add to Cart
def add_to_cart(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url', reverse('view_cart'))  

    cart = request.session.get('cart', {})

    if item_id in cart:
        cart[item_id] += quantity
        messages.success(request, f'{product.name} Updated quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} Added to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)

# Adjust Cart
def adjust_cart(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    if item_id in cart:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} Updated quantity to {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(request, f'{product.name} Added to your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))

# Remove from Cart
def remove_from_cart(request, item_id):
    try:
        product = get_object_or_404(Product, pk=item_id)

        cart = request.session.get('cart', {})

        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart

            messages.success(request, f'{product.name} Removed from your cart')

        return redirect(reverse('view_cart'))  

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
