from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=6)

    def __unicode__(self):
        return str(self.codigo)

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    departamento = models.ForeignKey('Departamento')

    def __unicode__(self):
        return str(self.nombre)

class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)

    municipio = models.ForeignKey('Municipio')

    def __unicode__(self):
        return str(self.direccion)
