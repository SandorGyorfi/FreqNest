from django.urls import path
from . import views
from .views import contact

urlpatterns = [
    path('', views.index, name='shop'),
    path('contact/', contact, name='contact'),
]