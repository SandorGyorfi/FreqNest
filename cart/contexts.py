from django.conf import settings
from django.shortcuts import get_object_or_404
from synths.models import Product


# Define a function to get the contents of the cart
def cart_contents(request):
    # Initialize variables
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    # Iterate over items in the cart
    for item_id, item_data in cart.items():
        # If the item_data is an integer, it means it's a quantity
        if isinstance(item_data, int):
            # Get the product with the given id
            product = get_object_or_404(Product, pk=item_id)
            # Update the total price
            total += item_data * product.price
            # Update the product count
            product_count += item_data
            # Add the item to the cart_items list
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })

    # The grand total is the same as the total in this case
    grand_total = total

    # Prepare the context to be returned
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    # Return the context
    return context
