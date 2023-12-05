from django.urls import path
from .views import all_synths  # Import your view
from . import views

urlpatterns = [
    path('', views.all_synths, name='all_synths'),  
    path('synths/', all_synths, name='synths'),  
    path('<product_id>/', views.synths_detail, name='synths_detail'),
]

