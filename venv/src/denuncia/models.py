# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone

class Denuncia(models.Model):

    CRIMINAL = 'CR'
    MUNICIPAL = 'MU'
    MEDIO_AMBIENTE = 'MA'
    DERECHOS_HUMANOS = 'DH'

    TIPO_CHOICES = (
        (CRIMINAL, 'Criminal'),
        (MUNICIPAL, 'Municipal'),
        (MEDIO_AMBIENTE, 'Medio Ambiente'),
        (DERECHOS_HUMANOS, 'Derechos Humanos'),
    )

    id = models.AutoField(primary_key=True)
    # nombre = models.CharField(max_length=255, blank=False, default = 'Anonimo')
    # dpi = models.CharField(max_length=13, blank=False, default = 'Anonimo')
    # telefono = models.CharField(max_length=10, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    denuncia = models.TextField(blank=False)
    referencia = models.CharField(blank=True, max_length=140, default="")
    fecha = models.DateTimeField(auto_now=True, auto_now_add=False, blank = False)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default=CRIMINAL)

    motivo = models.ForeignKey('Motivo')
    direccion = models.ForeignKey('localizaciones.Direccion')

    verbose_name = 'Denuncias'

    def __unicode__(self):
        return str(self.denuncia)

    def getSprite(self):
        return self.motivo.sprite()


@receiver(post_delete, sender=Denuncia)
def denuncia_delete(sender, instance, **kwargs):
    instance.motivo.cantidad -= 1
    instance.motivo.save()

@receiver(post_save, sender=Denuncia)
def denuncia_save(sender, instance, **kwargs):
    instance.motivo.cantidad += 1
    instance.motivo.save()

class Motivo(models.Model):
    id = models.AutoField(primary_key=True)
    motivo = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)

    correos = models.ManyToManyField('institucion.Correo')
    # institucion = models.ForeignKey('institucion.Institucion')

    def __unicode__(self):
        return str(self.motivo)

    def sumTotal(self):
        denuncias = Denuncia.objects.filter(motivo=self)

        return len(denuncias)

    def sprite(self):
        return self.id * 36

    class Meta:
        verbose_name = 'Motivos'
        ordering =['-cantidad']
