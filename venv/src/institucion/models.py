from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Institucion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank = False)

    verbose_name = 'Instituciones'


class Sede(models.Model):
    id = models.AutoField(primary_key=True)

    direccion = models.ForeignKey('localizaciones.Direccion')
    institucion = models.ForeignKey('Institucion')

#    class Meta:
        #verbose_name = 'Sedes'

class Telefono(models.Model):
    id = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=8)

    sede = models.ForeignKey('Sede')

    verbose_name = 'Telefonos'
