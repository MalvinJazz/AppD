from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Denuncia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, default = 'Anonimo')
    dpi = models.CharField(max_length=13, blank=True)
    #Departamento = models.CharField()
    #Municipio = models.CharField()
    direccion = models.CharField(max_length=255, blank=False)
    coordenadas = models.CharField(blank=True)
    descripcion = models.TextField(blank=False)
    solicitud = models.TextField(blank=True)
    archivo = models.FileField(blank=True)
    fecha = models.DateTimeField(auto_now=True,auto_now_add=False)

    verbose_name = 'Denuncias'

    def __unicode__(self):
        return str(nombre)

class Institucion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank = False)
    direccion = 
