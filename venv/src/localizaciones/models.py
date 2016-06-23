from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from denuncia.models import Denuncia

# Create your models here.

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=6, blank = False, null = False)

    def __unicode__(self):
        return str(self.codigo)

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
    cantidad = models.IntegerField(default=0)

    departamento = models.ForeignKey('Departamento')

    def __unicode__(self):
        return str(self.nombre)

    def sumDirecciones(self):
        denuncias = Direccion.objects.filter(municipio=self)
        suma = 0
        for dato in denuncias:
            suma = suma + dato.sumDenuncias()

        return suma

    # def getDenuncias(self):
    #     direcciones = Direccion.objects.filter(municipio=self)
    #
    #     denuncias = []
    #
    #     for dato in direcciones:
    #         tmp = list(Denuncia.objects.filter(direccion=dato).order_by('motivo'))
    #         denuncias.extend(tmp)
    #
    #     return denuncias


class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)

    municipio = models.ForeignKey('Municipio')

    def __unicode__(self):
        return str(self.direccion)+"--"+str(self.municipio.departamento)

    def sumDenuncias(self):
        denuncias = Denuncia.objects.filter(direccion=self)
        return len(denuncias)
