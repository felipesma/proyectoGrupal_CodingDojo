from django.urls import path
from . import views

urlpatterns = [
    path('', views.market),
    path('compra/', views.compra),
    path('success/', views.success),
]