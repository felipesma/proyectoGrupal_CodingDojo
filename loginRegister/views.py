from django.shortcuts import render, HttpResponse, redirect
from loginRegister.models import *
from django.contrib import messages
import bcrypt

# Create your views here.

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
        return redirect('/main/')

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
                messages.error(request, 'La contraseña no coincide con el usuario, intente nuevamente')
                return redirect('/main/')
        else:
            if 'registerError' in request.session:
                    del request.session['registerError']
            request.session['loginError'] = True
            print(request.session)
            messages.error(request, 'No existe usuario registrado con este correo electrónico.')
            return redirect('/main/')

def logout(request):
    if request.method == 'GET':
        if request.session.get('email') != None:
            request.session.flush()
            return redirect('/')