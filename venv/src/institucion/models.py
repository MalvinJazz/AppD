from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Institucion(models.Model):
    CRIMINAL = 'CR'
    MUNICIPAL = 'MU'
    MEDIO_AMBIENTE = 'MA'
    DERECHOS_HUMANOS = 'DH'

    TIPO_CHOICES = (
        (CRIMINAL, 'Criminal'),
        (MUNICIPAL, 'Municipal'),
        (MEDIO_AMBIENTE, 'Medio Ambiente'),
        (DERECHOS_HUMANOS, 'Derechos Humanos')
    )

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank = False)
    telefono = models.CharField(max_length=8, blank = False)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default=CRIMINAL)


    def __unicode__(self):
        return str(self.nombre)

# class Sede(models.Model):
#     id = models.AutoField(primary_key=True)
#
#     direccion = models.ForeignKey('localizaciones.Direccion')
#     institucion = models.ForeignKey('Institucion')
#
#     def __unicode__(self):
#         return str(self.institucion) + "--" + str(self.direccion)

#    class Meta:
        #verbose_name = 'Sedes'

class Correo(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField()

    institucion = models.ForeignKey('Institucion')

    def __unicode__(self):
        return str(self.correo)

# class Telefono(models.Model):
#     id = models.AutoField(primary_key=True)
#     telefono = models.CharField(max_length=8)
#
#     sede = models.ForeignKey('Sede')
#
#     verbose_name = 'Telefonos'
#
#     def __unicode__(self):
#         return str(self.telefono)
