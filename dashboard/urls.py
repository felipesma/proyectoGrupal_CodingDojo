from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('pedidos/', views.pedidos),
    path('clientes/', views.clientes),
    path('pedidos/<int:id>/', views.verPedido),
    path('pedidos/<int:id>/editar/', views.editarPedido),
    path('pedidos/<int:id>/borrar/', views.borrarPedido),
    path('clientes/<int:id>/', views.actualizarCliente),
    path('clientes/<int:id>/editar/', views.editarCliente),
    path('clientes/<int:id>/borrar/', views.borrarCliente),
]