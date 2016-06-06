from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Institucion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank = False)

    def __unicode__(self):
        return str(self.nombre)

class Sede(models.Model):
    id = models.AutoField(primary_key=True)

    direccion = models.ForeignKey('localizaciones.Direccion')
    institucion = models.ForeignKey('Institucion')

    def __unicode__(self):
        return str(self.institucion) + "--" + str(self.direccion)

#    class Meta:
        #verbose_name = 'Sedes'

class Correo(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField()

    institucion = models.ForeignKey('Institucion')

    def __unicode__(self):
        return str(self.correo)

class Telefono(models.Model):
    id = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=8)

    sede = models.ForeignKey('Sede')

    verbose_name = 'Telefonos'

    def __unicode__(self):
        return str(self.telefono)
