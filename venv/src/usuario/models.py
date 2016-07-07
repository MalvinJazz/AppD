from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

class UsuarioManager(BaseUserManager):

    def create_user(self, username, correo, nombre, apellidos, password=None):

        if not username:
            raise ValueError('Ingrese un nombre de usuario valido.')
        if not correo:
            raise ValueError('Ingrese una direccion de correo valida.')
        if not nombre:
            raise ValueError('Ingrese uno o mas nombres.')
        if not apellidos:
            raise ValueError('Ingrese sus apellidos.')

        usuario = self.model(
            username = username,
            correo = self.normalize_email(correo),
            nombre = nombre,
            apellidos = apellidos
        )

        usuario.set_password(password)
        usuario.save()

        return usuario

    def create_superuser(self, username, correo, nombre, apellidos, password=None):

        usuario = self.create_user(username, correo, nombre, apellidos, password)
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.save()

        return usuario

class Tipo_Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=45)

class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=55)
    apellidos = models.CharField(max_length=55)
    username = models.CharField(max_length=25, unique=True)
    correo = models.EmailField(unique=True)
    ultima_conexion = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    tipo = models.ForeignKey('Tipo_Usuario', default=1)
    institucion = models.ForeignKey('institucion.Institucion', default = 1)
    zona = models.ForeignKey('localizaciones.Direccion', default = 1)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'correo']

    def get_full_name(self):
        return self.nombre + " " + self.apellidos

    def get_short_name(self):
        return self.nombre

    def __unicode__(self):
        return self.username

    def has_module_perms(self, perm_list):
        return True

    def has_perm(self, perm):
        return True
