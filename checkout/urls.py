from django.urls import path
from . import views
from . import views as checkout_views


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/success/<str:order_number>/', views.checkout_success, name='checkout_success'),
    path('stripe-public-key/', checkout_views.stripe_public_key, name='stripe_public_key'),
]