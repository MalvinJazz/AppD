from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Denuncia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, default = 'Anonimo')
    dpi = models.CharField(max_length=13, blank=True)
    direccion = models.CharField(max_length=255, blank=False)
    coordenadas = models.CharField(max_length=255,blank=True)
    descripcion = models.TextField(blank=False)
    solicitud = models.TextField(blank=True)
    archivo = models.FileField(blank=True)
    fecha = models.DateTimeField(auto_now=True,auto_now_add=False)

    motivo = models.ForeignKey('Motivo')

    verbose_name = 'Denuncias'

    def __unicode__(self):
        return str(self.nombre)

class Motivo(models.Model):
    id = models.AutoField(primary_key=True)
    motivo = models.CharField(max_length=100)

    verbose_name = 'Motivos'

    institucion = models.ForeignKey('institucion.Institucion')
