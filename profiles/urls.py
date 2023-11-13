from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register/', register, name='register'),
    path('', views.index, name='index'),
]