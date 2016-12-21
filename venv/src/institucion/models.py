# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

"""

Atributo    Descripcion

id          Identificador de la institucion

nombre      Nombre de la institucion

tipo        Sección del total de denuncias a las que pertenece esta
            institucion, relacionado con el atributo TIPO_CHOICES.

"""
class Institucion(models.Model):
    CRIMINAL = 'CR'
    MUNICIPAL = 'MU'
    MEDIO_AMBIENTE = 'MA'
    DERECHOS_HUMANOS = 'DH'
    NINGUNO = 'NG'

    TIPO_CHOICES = (
        (CRIMINAL, 'Criminal'),
        (MUNICIPAL, 'Municipal'),
        (MEDIO_AMBIENTE, 'Medio Ambiente'),
        (DERECHOS_HUMANOS, 'Derechos Humanos'),
        (NINGUNO, 'Ninguno')
    )

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank = False)
    tipo = models.CharField(
                    max_length=2,
                    choices=TIPO_CHOICES,
                    default=CRIMINAL
                    )


    def __unicode__(self):
        return self.nombre

"""

Atributo    Descripcion

id          Identificador del correo

correo      Correo de la institucion relacionada y
            del municipio a donde pertenece esta.

institucion Institucion a la que pertenece este correo.

municipio   Municipio a donde pertenece el correo.

"""
#concejomunixelaof@gmail.com
class Correo(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField()

    institucion = models.ForeignKey('Institucion')
    municipio = models.ForeignKey('localizaciones.Municipio')

    def __unicode__(self):
        return self.correo

    def get_departamento(self):
        return self.municipio.departamento

    class Meta:
        ordering = ['-municipio']
