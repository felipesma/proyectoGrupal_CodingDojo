from django.shortcuts import render, HttpResponse, redirect
from loginRegister.models import *

# Create your views here.

def market(request):
    if request.session.get('email') == None:
        return redirect('/main/')
    else:
        usuario = Usuario.objects.get(email=request.session['email'])
        print(usuario)
        categorias = []
        for categoria in Categoria.objects.all():
            categorias.append(categoria)
        context = {
            'categorias': categorias,
            'usuario': usuario,
        }
        return render(request, 'index.html', context=context)

def compra(request):
    if request.method == 'POST':
        compra = request.POST['compraTotal']
        total = request.POST['pagoTotal']
        request.session['compra'] = compra
        request.session['total'] = total
        context = {
            'compra': compra,
            'total': total,
        }
        return render(request, 'order-confirmation.html', context=context)
    else:
        return redirect('/inicio')

def success(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(email=request.session['email'])
        nombre_usuario = usuario.nombre
        pedido = Pedido.objects.create(cliente=usuario, productos=request.session['compra'], total=int(request.session['total']))
        print(pedido)
        context = {
            'usuario': nombre_usuario,
        }
        return render(request, 'success.html', context=context)
    else:
        return redirect('/inicio/compra/')

