from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from loginRegister.models import *
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def send_email(email_user, id_pedido):
    usuario = Usuario.objects.get(email=email_user)
    administradores = Usuario.objects.filter(nivel=9)
    admin_email = []
    for admin in administradores:
        admin_email.append(admin.email)
    print(admin_email)
    context = {
        'usuario': usuario,
        'id_pedido': id_pedido,
    }
    template = get_template('email-order.html')
    content = template.render(context)
    email_send = EmailMultiAlternatives(
        'Compra Realizada',
        'Se ha realizado una compra',
        settings.EMAIL_HOST_USER,
        admin_email
    )
    email_send.attach_alternative(content, 'text/html')
    email_send.send()

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
        print(pedido.id)
        send_email(request.session['email'], pedido.id)
        context = {
            'usuario': nombre_usuario,
        }
        return render(request, 'success.html', context=context)
    else:
        return redirect('/inicio/compra/')