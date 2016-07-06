# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from denuncia.models import Denuncia, Motivo

# Create your models here.

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=6, blank = False, null = False)

    def __unicode__(self):
        return str(self.nombre)

    def sumMunicipios(self):
        denuncias = Municipio.objects.filter(departamento=self)
        suma = 0

        for dato in denuncias:
            suma = suma + dato.sumDirecciones()

        return suma

    def getMunicipios(self):
        return Municipio.objects.filter(departamento=self)

    class Meta:
        ordering = ["codigo"]

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    departamento = models.ForeignKey('Departamento')

    def __unicode__(self):
        return str(self.nombre)

    def sumDirecciones(self):
        denuncias = Direccion.objects.filter(municipio=self)
        suma = 0
        for dato in denuncias:
            suma = suma + dato.sumDenuncias()

        return suma

    def getDenuncias(self):
        direcciones = Direccion.objects.filter(municipio=self)

        motivos = Motivo.objects.all()

        dic = {}

        for mot in motivos:
            x = len(Denuncia.objects.filter(
                direccion__municipio=self,
                motivo = mot
                ))
            dic.update({
                mot.motivo: x,
            })

        return dic



class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)

    municipio = models.ForeignKey('Municipio')

    def __unicode__(self):
        return str(self.direccion)

    def sumDenuncias(self):
        denuncias = Denuncia.objects.filter(direccion=self)
        return len(denuncias)

    def getDenuncias(self):

        motivos = Motivo.objects.all()

        dic = {}

        for mot in motivos:
            x = len(Denuncia.objects.filter(
                direccion = self,
                motivo = mot
                ))
            dic.update({
                mot.motivo: x,
            })

        return dic
