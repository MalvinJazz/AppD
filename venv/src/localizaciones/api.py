from tastypie.resources import (
                        ModelResource,
                        ALL,
                        ALL_WITH_RELATIONS
                        )
from tastypie.authorization import Authorization
from tastypie import fields

from .models import Departamento, Municipio, Direccion

class DepartamentoResource(ModelResource):
    class Meta:
        queryset = Departamento.objects.all()
        resource_name = 'departamento'
        filtering = {
            'id': ALL,
        }
        allowed_methods = ['get']

class MunicipioResource(ModelResource):

    departamento = fields.ForeignKey(
                    DepartamentoResource,
                    attribute='departamento',
                    full=True,
                    )
    # departamento = fields.CharField(attribute='departamento')

    class Meta:
        queryset = Municipio.objects.all()
        resource_name = 'municipio'
        filtering = {
            'departamento': ALL_WITH_RELATIONS,
            'id': ALL,
        }
        allowed_methods = ['get']

class DireccionResource(ModelResource):

    municipio = fields.ForeignKey(
        MunicipioResource,
        attribute='municipio',
        full=True
    )

    # municipio = fields.CharField(attribute='municipio')

    class Meta:
        queryset = Direccion.objects.all()
        resource_name = 'direccion'
        filtering = {
            'municipio': ALL_WITH_RELATIONS,
        }
        allowed_methods = ['get']
