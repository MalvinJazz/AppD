#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import smart_str, smart_unicode
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone

from tastypie.resources import (
                        ModelResource,
                        ALL,
                        ALL_WITH_RELATIONS
                        )
from tastypie.authorization import Authorization
from tastypie import fields

from .models import Denuncia, Motivo
from institucion.models import Correo
from institucion.api import InstitucionResource
from localizaciones.api import (
    DepartamentoResource,
    MunicipioResource,
    DireccionResource
)

class MotivoResource(ModelResource):

    instituciones = fields.ToManyField(
        InstitucionResource,
        attribute='instituciones',
        full=True,
        )

    class Meta:
        queryset = Motivo.objects.all()
        filtering = {
            'id': ALL,
            'tipo': ALL,
            'instituciones': ALL_WITH_RELATIONS,
        }
        allowed_methods = ['get']
        resource_name = 'motivo'

class DenunciaResource(ModelResource):

    motivo = fields.ForeignKey(
        MotivoResource,
        attribute = 'motivo',
        full=True,
    )
    direccion = fields.ForeignKey(
        DireccionResource,
        attribute='direccion',
        full=True
    )

    def obj_create(self, bundle, **kwargs):


        imgData = bundle.data.get('file')

        print bundle.data.get('latitud')
        print bundle.data.get('longitud')

        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        objeto = self.save(bundle)

        denuncia = bundle.obj

        geo = False

        if denuncia.latitud != 0 and denuncia.longitud != 0:
            geo = True

        municipio = denuncia.direccion.municipio
        departamento = municipio.departamento

        motivo = denuncia.motivo
        vIn = motivo.instituciones.all()

        correos = Correo.objects.none()
        for institucion in vIn:
            if institucion.tipo == "MU":
                temp = Correo.objects.filter(
                            institucion = institucion,
                            municipio = municipio
                            )
            else:
                temp = Correo.objects.filter(
                            institucion = institucion,
                            municipio__departamento = departamento
                            )
            correos = correos | temp

        try:
            text_content = 'Denuncia'

            mail_html = get_template('correo.html')

            d = Context({
                    'motivo':motivo,
                    'denuncia': denuncia.denuncia,
                    'geo': geo,
                    'referencia': denuncia.referencia,
                    'latitud': denuncia.latitud,
                    'longitud': denuncia.longitud,
                    'label': motivo.motivo[0],
                    'fecha': timezone.localtime(denuncia.fecha).strftime('%d-%b-%Y %-I:%M %p %Z'),
                    'direccion': denuncia.direccion.direccion+", "+municipio.nombre+", "+departamento.nombre,
                    'tipo': motivo.tipo
                    })

            html_content = mail_html.render(d)

            from_email = '"DenunciApp Guatemala" <denuncias@denunciappguatemala.com>'
            to = correos
            msg = EmailMultiAlternatives(motivo, text_content, from_email, to)

            msg.attach_alternative(html_content, "text/html")

            try:
                if len(imgData)>0:

                    quitar = ""

                    quitar, imgData = imgData.split("data:", 1)
                    mime, imgData = imgData.split(";base64,")
                    quitar, tipo = mime.split('/')

                    missing_padding = 4 - len(imgData) % 4
                    if missing_padding:
                        imgData += b'='* missing_padding

                    msg.attach('denuncia.' + tipo ,imgData.decode('base64'), mime)

            except Exception, ex:
                print ex, '1'

            #msg.send()

        except Exception, ex:
            print ex, '2'

        return objeto

    class Meta:
        queryset = Denuncia.objects.all()
        filtering = {
            'id': ALL,
            'tipo': ALL,
            'motivo': ALL_WITH_RELATIONS,
            'direccion': ALL_WITH_RELATIONS
        }
        allowed_methods = ['post']
        resource_name = 'denuncia'
        authorization = Authorization()
