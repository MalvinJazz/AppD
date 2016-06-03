from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Institucion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank = False)

    direccion = models.ForeignKey('localizaciones.Direccion')

class Telefono(models.Model):
    id = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=8)

    institucion = models.ForeignKey('Institucion')
