from django.shortcuts import render, redirect, reverse, get_object_or_404
from synths.models import Product, Category
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower



def all_synths(request):
    synths = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                synths = synths.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            synths = synths.order_by(sortkey)
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            synths = synths.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('synths'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            synths = synths.filter(queries)            
    current_sorting = f'{sort}_{direction}'
    context = {
        'synths': synths,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'synths/synths.html', context)

def synths_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'synths/synths_detail.html', context)

