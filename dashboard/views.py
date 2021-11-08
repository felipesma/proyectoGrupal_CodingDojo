from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from loginRegister.models import *
import bcrypt
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from twilio.rest import Client

# Create your views here.

def send_sms(numero_cliente):
    account_sid = 'ACf4078d6e201901c7ea7e3da29ef4bf85'
    auth_token = '51ddd9bee04517df8d0e71d20cccecc1'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Tu pedio realizado en ALMACEN está listo para ser retirado! Te esperamos en el negocio para que lo retires.",
                        from_='+15157173081',
                        to=numero_cliente
                    )
    print('SMS ENVIADO A CLIENTE', message.sid)


def send_email(email):
    usuario = Usuario.objects.get(email=email)
    context = {'usuario': usuario}
    template = get_template('confirmacion-pedido.html')
    content = template.render(context)
    email_send = EmailMultiAlternatives(
        'Tu compra esta lista para ser retirada!',
        'Alamecen ha preparado tu compra y se encuentra lista',
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_send.attach_alternative(content, 'text/html')
    email_send.send()

def dashboard(request):
    if request.session.get('email') == None:
        return redirect('/main/')
    else:
        usuario = Usuario.objects.get(email=request.session['email'])
        if usuario.nivel == 1:
            return redirect('/main/')
        elif usuario.nivel == 9:
            pedidos = Pedido.objects.all().order_by("-id")
            pedidos_en_proceso = Pedido.objects.filter(estado="1")
            total = 0
            for pedido in pedidos:
                total += pedido.total
            clientes = Usuario.objects.all()
            ultimos_clientes = Usuario.objects.all().order_by("-id")
            context = {
                'pedidos': pedidos,
                'clientes': clientes,
                'ultimos_clientes': ultimos_clientes,
                'en_proceso': pedidos_en_proceso,
                'total': total,
            }
            return render(request, 'dashboard.html', context=context)

def pedidos(request):
    if request.session.get('email') == None:
        return redirect('/main/')
    else:
        usuario = Usuario.objects.get(email=request.session['email'])
        if usuario.nivel == 1:
            return redirect('/main/')
        elif usuario.nivel == 9:
            pedidos = Pedido.objects.all().order_by("-id")
            context = {
                'pedidos': pedidos,
            }
            return render(request, 'pedidos.html', context=context)

def clientes(request):
    if request.session.get('email') == None:
        return redirect('/main/')
    else:
        usuario = Usuario.objects.get(email=request.session['email'])
        if usuario.nivel == 1:
            return redirect('/main/')
        elif usuario.nivel == 9:
            clientes = Usuario.objects.all()
            context = {
                'clientes': clientes,
            }
            return render(request, 'clientes.html', context=context)

def verPedido(request, id):
    pedido = Pedido.objects.get(id=id)
    context = {
        'pedido': pedido,
    }
    return render(request, 'vista-pedido.html', context=context)

def editarPedido(request, id):
    if request.method == 'POST':
        pedido = Pedido.objects.get(id=id)
        pedido.estado = request.POST['estado']
        pedido.pago = request.POST['pago']
        numero_cliente = pedido.cliente.telefono
        print(numero_cliente)
        pedido.save()
        if pedido.estado == '2':
            print('enviando mail')
            send_email(pedido.cliente.email)
            send_sms(numero_cliente)
        return redirect('/dashboard/pedidos/')
    else:
        return redirect('/dashboard/pedidos/')

def borrarPedido(request, id):
    if request.method == 'POST':
        Pedido.objects.get(id=id).delete()
        return redirect('/dashboard/pedidos/')
    else:
        return redirect('/dashboard/pedidos/')

def actualizarCliente(request, id):
    cliente = Usuario.objects.get(id=id)
    context = {
        'cliente': cliente,
    }
    return render(request, 'editar-usuario.html', context=context)

def editarCliente(request, id):
    if request.method == 'POST':
        cliente = Usuario.objects.get(id=id)
        cliente.nombre = request.POST['nombre']
        cliente.email = request.POST['email']
        cliente.direccion = request.POST['direccion']
        cliente.telefono = request.POST['telefono']
        cliente.nivel = request.POST['nivel']
        if request.POST['password'] != '':
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            cliente.password = password
        cliente.save()
        return redirect('/dashboard/clientes/')
    else:
        return redirect('/dashboard/clientes/')

def borrarCliente(request, id):
    if request.method == 'POST':
        Usuario.objects.get(id=id).delete()
        return redirect('/dashboard/clientes/')
    else:
        return redirect('/dashboard/clientes/')
    