from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),  
    path('profile/', views.profile, name='profile'),  
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register/', views.register, name='register'), 
    path('login/', views.custom_login, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    ]
