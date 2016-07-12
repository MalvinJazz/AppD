from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields

from .models import Departamento, Municipio, Direccion

class DepartamentoResource(ModelResource):
    class Meta:
        queryset = Departamento.objects.all()
        resource_name = 'departamento'
        allowed_methods = ['get']

class MunicipioResource(ModelResource):

    departemento = fields.ForeignKey(
                    DepartamentoResource,
                    attribute='departamento',
                    null=True,
                    full=True
                    )

    class Meta:
        queryset = Municipio.objects.all()
        resource_name = 'municipio'
        allowed_methods = ['get']

class DireccionResource(ModelResource):

    municipio = fields.ForeignKey(
        MunicipioResource,
        attribute='municipio',
        null=True,
        full=True
    )

    class Meta:
        queryset = Direccion.objects.all()
        resource_name = 'direccion'
        allowed_methods = ['get']
