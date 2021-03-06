from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from loginRegister.models import *
from django.contrib import messages
import bcrypt
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def send_email(email):
    usuario = Usuario.objects.get(email=email)
    context = {'usuario': usuario}
    template = get_template('register-mail.html')
    content = template.render(context)
    email_send = EmailMultiAlternatives(
        'Bienvenido a la App Almacen',
        'Tu usuario ha sido registrado exitosamente',
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_send.attach_alternative(content, 'text/html')
    email_send.send()

    
def index(request):
    if request.session.get('email') != None:
        logued = Usuario.objects.get(email=request.session['email'])
        nivel_logued = logued.nivel
        if nivel_logued == 1:
            return redirect('/inicio/')
        else:
            return redirect('/dashboard/')
    else:
        return redirect('main/')

def main(request):
    return render(request, 'signin-register.html')

def register(request):
    errors = Usuario.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        if 'loginError' in request.session:
            del request.session['loginError'] 
        request.session['registerError'] = True 
        return redirect('/inicio')
    else: 
        if request.method == 'POST':
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            length_users = Usuario.objects.all()
            if 'loginError' in request.session:
                del request.session['loginError']
            if 'registerError' in request.session:
                del request.session['registerError']
            if len(length_users) == 0:
                Usuario.objects.create(nombre=request.POST['nombre'], email=request.POST['email'], direccion=request.POST['direccion'], telefono=request.POST['telefono'],password=password, nivel=9)
            else:
                Usuario.objects.create(nombre=request.POST['nombre'], email=request.POST['email'], direccion=request.POST['direccion'], telefono=request.POST['telefono'],password=password, nivel=1)  
            request.session['email']=request.POST['email']
            send_email(request.session['email'])
            return redirect('/inicio/')
        else:
            return redirect('/main/')

def login(request):
    if request.method == 'POST':
        usuario = Usuario.objects.filter(email=request.POST['email'])
        if len(usuario) == 1:
            if bcrypt.checkpw(request.POST['password'].encode(), usuario[0].password.encode()):
                request.session['email'] = request.POST["email"]
                logued = Usuario.objects.get(email=request.session['email'])
                nivel_logued = logued.nivel
                if 'loginError' in request.session:
                    del request.session['loginError']
                if nivel_logued == 1:
                    return redirect('/inicio/')
                else:
                    return redirect('/dashboard/')
            else:
                if 'registerError' in request.session:
                    del request.session['registerError']
                request.session['loginError'] = True
                print(request.session)
                messages.error(request, 'La contrase??a no coincide con el usuario, intente nuevamente')
                return redirect('/main/')
        else:
            if 'registerError' in request.session:
                    del request.session['registerError']
            request.session['loginError'] = True
            print(request.session)
            messages.error(request, 'No existe usuario registrado con este correo electr??nico.')
            return redirect('/main/')

def logout(request):
    if request.method == 'GET':
        if request.session.get('email') != None:
            request.session.flush()
            return redirect('/')


def profile(request, id):
    user = Usuario.objects.get(id= id)
    context={
        'user': user
    }
    return render(request, 'profile.html', context)

def update_profile(request, id):
    user = Usuario.objects.get(id= id)
    errors = Usuario.objects.basic_validator2(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/profile/{user.id}')
    else:  
        if request.method == 'POST':
            user.nombre = request.POST['nombre']
            user.direccion = request.POST['direccion']
            user.telefono = request.POST['telefono']
            if request.POST['password'] != "":
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
                user.password = pw_hash
            user.email = request.POST['email']
            user.save()
            messages.success(request, 'Informaci??n actualizada con ??xito')
            context= {'icon': 'success'}
            return redirect(f'/profile/{user.id}', context)
      
