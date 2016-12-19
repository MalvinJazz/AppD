# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.db.models import Q

from denuncia.models import Denuncia, Motivo

"""
--------------------------------------------------------------------------------
|     VARIABLE     |       TIPO      |              DESCRIPCION                |
-------------------+-----------------+------------------------------------------
|        id        |       PK        |  Llave primaria de Departamento.        |
|                  |      (INT)      |                                         |
--------------------------------------------------------------------------------
|      nombre      |    CharField    |  Nombre del departamento.               |
--------------------------------------------------------------------------------
|      codigo      |    CharField    |  Cadena que identifica al departamento  |
|                  |                 |  por medio de su codigo ISO.            |
--------------------------------------------------------------------------------
|    __unicode__   |     funcion     |  Representación del obejto como una     |
|                  |                 |  cadena, en este caso, es el 'nombre'.  |
--------------------------------------------------------------------------------
|   sumMunicipios  |     funcion     |  Retorna el conteo de objetos de la     |
|                  |                 |  tabla Denuncia, relacionadas con este  |
|                  |                 |  departamento.                          |
--------------------------------------------------------------------------------
|   getMunicipios  |     funcion     |  Retorna la lista de Municipios del     |
|                  |                 |  Departamento.                          |
--------------------------------------------------------------------------------

Meta:
--------------------------------------------------------------------------------
|     ordering     |      array      |  Lista que indica por que parametros    |
|                  |                 |  se ordena la tabla del modelo. Se      |
|                  |                 |  ordena por cantidad.                   |
--------------------------------------------------------------------------------
"""

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=6, blank = False, null = False)

    def __unicode__(self):
        return self.nombre

    def sumMunicipios(self):
        return Denuncia.objects.filter(
                    direccion__municipio__departamento=self
                    ).count()

    def getMunicipios(self):
        return Municipio.objects.filter(departamento=self)

    class Meta:
        ordering = ["codigo"]

"""
--------------------------------------------------------------------------------
|     VARIABLE     |       TIPO      |              DESCRIPCION                |
-------------------+-----------------+------------------------------------------
|        id        |       PK        |  Llave primaria de Municipio.           |
|                  |      (INT)      |                                         |
--------------------------------------------------------------------------------
|      nombre      |    CharField    |  Nombre del municipio.                  |
--------------------------------------------------------------------------------
|   departamento   |       FK        |  Relacion del municipio con un dep.     |
--------------------------------------------------------------------------------
|    __unicode__   |     funcion     |  Representación del obejto como una     |
|                  |                 |  cadena, en este caso, es el 'nombre'.  |
--------------------------------------------------------------------------------
|  sumDirecciones  |     funcion     |  Retorna el conteo de objetos de la     |
|                  |                 |  tabla Denuncia, relacionadas con este  |
|                  |                 |  municipio.                             |
--------------------------------------------------------------------------------
|   getDenuncias   |     funcion     |  Retorna un diccionario con la cantidad |
|                  |                 |  de denuncias por motivo, filtrado por  |
|                  |                 |  municipio.                             |
--------------------------------------------------------------------------------
"""
class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    departamento = models.ForeignKey('Departamento')

    def __unicode__(self):
        return self.nombre

    def filtro_denuncias(self, tipo):
        return Denuncia.objects.filter(
            direccion__municipio=self,
            tipo=tipo
        ).count()

    def sumDirecciones(self):
        return Denuncia.objects.filter(direccion__municipio=self).count()

    def getDenuncias(self):
        #direcciones = Direccion.objects.filter(municipio=self)
        dic = {}

        for mot in Motivo.objects.all():
            dic.update({
                mot.motivo_hash(): Denuncia.objects.filter(
                    direccion__municipio=self,
                    motivo = mot
                    ).count(),
            })

        return dic

# @receiver(post_save, sender=Municipio)
# def zona_prov(sender, instance, created, **kwargs):
#     if not created:
#         i = 1
#         while i < 21:
#             zona = Direccion()
#             zona.direccion = 'Zona ' + str(i)
#             zona.municipio = instance
#             zona.save()
#             i+=1
"""
--------------------------------------------------------------------------------
|     VARIABLE     |       TIPO      |              DESCRIPCION                |
-------------------+-----------------+------------------------------------------
|        id        |       PK        |  Llave primaria de Direccion.           |
|                  |      (INT)      |                                         |
--------------------------------------------------------------------------------
|     direccion    |    CharField    |  Nombre de la zona.                     |
--------------------------------------------------------------------------------
|     municipio    |       FK        |  Relacion del objeto con un Municipio.  |
--------------------------------------------------------------------------------
|    __unicode__   |     funcion     |  Representación del obejto como una     |
|                  |                 |  cadena, en este caso, es la 'dir'.     |
--------------------------------------------------------------------------------
|   sumDenuncias   |     funcion     |  Conteo de objetos de la tabla Denuncia |
|                  |                 |  relacionadas con el objeto Direccion.  |
--------------------------------------------------------------------------------
|  denuncias_tipo  |     funcion     |  Retorna un diccionario con la cantidad |
|                  |                 |  de denuncias de la direccion por tipo. |
--------------------------------------------------------------------------------
|   getDenuncias   |     funcion     |  Retorna un diccionario con la cantidad |
|                  |                 |  de denuncias por de la dir. por motivo.|
--------------------------------------------------------------------------------

"""
class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=255)

    municipio = models.ForeignKey('Municipio')

    def __unicode__(self):
        return self.direccion

    def sumDenuncias(self):
        return Denuncia.objects.filter(direccion=self).count()
        #return len(denuncias)

    def denuncias_tipo(self):
        dic = {
            "CR": Denuncia.objects.filter(
                    direccion=self,
                    tipo="CR").count(),
            "MA": Denuncia.objects.filter(
                    direccion=self,
                    tipo="MA").count(),
            "MU": Denuncia.objects.filter(
                    direccion=self,
                    tipo="MU").count(),
            "DH": Denuncia.objects.filter(
                    direccion=self,
                    tipo="DH").count(),
        }

        return dic

    def getDenuncias(self):

        motivos = Motivo.objects.all()

        dic = {}

        for mot in motivos:
            x = Denuncia.objects.filter(
                direccion = self,
                motivo = mot
                ).count()
            dic.update({
                mot.motivo_hash(): x,
            })

        return dic
