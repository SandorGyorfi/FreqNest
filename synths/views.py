from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from synths.models import Product, Category


# Function to display all synths
def all_synths(request):
    # Get all synths from the database
    synths = Product.objects.all()

    # Check if there are any GET parameters
    if request.GET:
        # Sorting functionality
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'name':
                sortkey = 'lower_name'
                synths = synths.annotate(lower_name=Lower('name'))
            elif sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET and request.GET['direction'] == 'desc':
                sortkey = f'-{sortkey}'

            synths = synths.order_by(sortkey)

        # Category filtering functionality
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            synths = synths.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Search functionality
        if 'q' in request.GET:
            query = request.GET['q'].strip()
            if not query:
                messages.error(request, "[Search] You didn't enter any search criteria!")
                return redirect(reverse('synths'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            synths = synths.filter(queries)

    # Check if there are no synths and a search term was entered
    if not synths and 'q' in request.GET and request.GET['q'].strip():
        messages.error(request, "[Search] No results found for your search criteria.")

    # Prepare context for the template
    context = {
        'synths': synths,
        'search_term': request.GET.get('q', '').strip(),
        'current_categories': request.GET.get('category', '').split(','),
        'current_sorting': f"{request.GET.get('sort', '')}_{request.GET.get('direction', '')}",
    }

    # Render the template with the context
    return render(request, 'synths/synths.html', context)

# Function to display details of a specific synth
def synths_detail(request, product_id):
    # Get the specific product or return 404 if not found
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    # Render the template with the context
    return render(request, 'synths/synths_detail.html', context)
