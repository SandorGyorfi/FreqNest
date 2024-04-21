from django.shortcuts import render


# Index view
def index(request):
    return render(request, 'shop/index.html')

# Contact view
def contact(request):
    return render(request, 'shop/contact.html')
