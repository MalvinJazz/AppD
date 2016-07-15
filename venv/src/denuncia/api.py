# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives

from tastypie.resources import (
                        ModelResource,
                        ALL,
                        ALL_WITH_RELATIONS
                        )
from tastypie.authorization import Authorization
from tastypie import fields

from .models import Denuncia, Motivo
from institucion.api import InstitucionResource
from localizaciones.api import (
    DepartamentoResource,
    MunicipioResource,
    DireccionResource
)

class MotivoResource(ModelResource):

    institucion = fields.ForeignKey(
        InstitucionResource,
        attribute='institucion',
        full=True,
        )

    class Meta:
        queryset = Motivo.objects.all()
        filtering = {
            'id': ALL,
            'institucion': ALL_WITH_RELATIONS,
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

        print type(bundle.data.get('file'))

        # text_content = 'Denuncia'
        # html_content = '<!DOCTYPE html><html><body><h1>' + str(motivo) + '''</h1></br>
        #                     <h3> Nombre: ''' + str(denuncia.nombre) + '''<br>
        #                     DPI: ''' + str(denuncia.dpi) + '''<br>
        #                     Telefono: ''' + str(denuncia.telefono) + '''</h3></br>
        #                     <h4>Direccion: ''' + str(denuncia.direccion) + ''',
        #                     ''' + str(municipio) + ', ' + str(departamento) +'''.
        #                     <i>(Con referencia en: '''+str(denuncia.referencia)+''')</i> </h4>
        #                     </br> <h5> Denuncio: </h5></br> <p>
        #                     ''' + str(denuncia.denuncia) + '''</p></body>
        #                     <footer><i>Los archivos quedan a cargo de la
        #                      entidad indicada.</i><br>
        #                     <i>Todos los datos de este correo son
        #                      confidenciales y no deben ser difundidos
        #                     a nadie más que las entidades interesadas
        #                      en ellos.</i></footer></html>'''
        #
        # from_email = '"Denuncia Movil" <denunciamovil@gmail.com>'
        # to = vIn
        # msg = EmailMultiAlternatives(motivo, text_content, from_email, to)
        # msg.attach_alternative(html_content, "text/html")
        # if request.FILES:
        #     msg.attach(archivo.name,archivo.read(),archivo.content_type)
        # msg.send()

        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        return self.save(bundle)

    class Meta:
        queryset = Denuncia.objects.all()
        filtering = {
            'id': ALL,
            'tipo': ALL,
            'motivo': ALL_WITH_RELATIONS,
            'direccion': ALL_WITH_RELATIONS
        }
        allowed_methods = ['get', 'post']
        resource_name = 'denuncia'
        authorization = Authorization()
