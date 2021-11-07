from django.db import models
from django.core.validators import validate_email
import re

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['password'] != postData['password_confirmation']:
            errors['password_match'] = "Las constraseñas no coinciden, favor reintente."
        if len(postData['password']) < 8:
            errors['len_password'] = "La contraseña debe tener al menos 8 carácteres."
        if len(postData['nombre']) < 1:
             errors["nombre"] = "Nombre no puede estar en blanco"            
        if len(postData['direccion']) < 1 :
            errors["direccion"] = "Direccion no puede estar en blanco"
        if len(postData['telefono']) < 1 :
            errors["telefono"] = "Telefono no puede estar en blanco"
        if len(postData['email']) < 1 :
            errors["email"] = "Email no puede estar en blanco"
        user = self.filter(email=postData['email'])
        if user:
            errors["email"] = "ya existe el email"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # probar si un campo coincide con el patrón        
            errors['email'] = "Formato de correo incorrecto!"
        return errors

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    objects = UserManager()
    nivel = models.IntegerField(default=1)

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

class Producto(models.Model):
    producto = models.CharField(max_length=50)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, related_name="productos", on_delete=models.CASCADE)

class Pedido(models.Model):
    cliente = models.ForeignKey(Usuario, related_name="pedidos", on_delete=models.CASCADE)
    productos = models.TextField(default='null')
    total = models.IntegerField(default=0)
    estado = models.IntegerField(default=1)
    pago = models.IntegerField(default=1)