from django.urls import path
from . import views

urlpatterns = [
    path('', views.paymentIndex),
    path('process/', views.paymentSucces),  
]