from loginRegister.models import *
from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def send_email(email_user, id_pedido):
    usuario = Usuario.objects.get(email=email_user)
    administradores = Usuario.objects.filter(nivel=9)
    admin_email = []
    for admin in administradores:
        admin_email.append(admin.email)
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

def paymentIndex(request):
    return render(request, 'payment.html')

def paymentSucces(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(email=request.session['email'])
        nombre_usuario = usuario.nombre
        pedido = Pedido.objects.create(cliente=usuario, productos=request.session['compra'], total=int(request.session['total']))
        send_email(request.session['email'], pedido.id)
        context = {
            'usuario': nombre_usuario,
        }
        return render(request, 'success.html', context=context)
