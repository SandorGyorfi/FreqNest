from django.shortcuts import render

def index(request):
    """Index view"""
    return render(request, 'shop/index.html')


def contact(request):
    return render(request, 'shop/contact.html')

