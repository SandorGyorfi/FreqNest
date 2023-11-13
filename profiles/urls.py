from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('profile/', views.profile, name='profile'),  
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register/', views.register, name='register'), 
]
