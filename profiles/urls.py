from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),  
    path('profile/', views.profile, name='profile'),  
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('register/', views.register, name='register'), 
    path('login/', LoginView.as_view(template_name='profiles/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    ]
