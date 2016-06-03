from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.nombre)

    #class Meta:
        #verbose_name = 'Departamentos'

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    departamento = models.ForeignKey('Departamento')

    verbose_name = 'Municipios'

    def __unicode__(self):
        return str(self.nombre)

class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)

    municipio = models.ForeignKey('Municipio')

    verbose_name = 'Direcciones'

    def __unicode__(self):
        return str(self.direccion)
