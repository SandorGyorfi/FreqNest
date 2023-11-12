from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_synths, name='all_synths'),  
    path('<product_id>/', views.synths_detail, name='synths_detail'),
]

