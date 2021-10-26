from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('main/', views.main),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
]