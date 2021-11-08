from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('main/', views.main),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/<int:id>', views.profile, name= 'profile'),
    path('update_profile/<int:id>', views.update_profile, name= 'update_profile'),
]