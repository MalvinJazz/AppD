from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization
from tastypie import fields

from .models import Institucion, Correo

class InstitucionResource(ModelResource):
    class Meta:
        queryset = Institucion.objects.all()
        filtering = {
            'id': ALL,
        }
        resource_name = 'institucion'
        allowed_methods = ['get']

class CorreoResource(ModelResource):

    institucion = fields.ForeignKey(
                        InstitucionResource,
                        attribute='institucion',
                        null=True,
                        full=True
                        )

    class Meta:
        queryset = Correo.objects.all()
        resource_name = 'correo'
