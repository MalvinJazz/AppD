from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import Serializer
from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.views.generic.detail import DetailView
#from django.utils.encoding import smart_text, is_protected_type

from .models import Departamento, Municipio, Direccion
from denuncia.models import Denuncia, Motivo

#--------------------------------------------------------
#Serializador de json------------------------------------

class MuniSerializer(Serializer):

    def get_dump_object(self, obj):
        dic = super(MuniSerializer, self).get_dump_object(obj)
        dic.update({
            'cant': obj.sumDirecciones(),
            'mots': obj.getDenuncias(),
        })
        return dic


    def end_object(self, obj):
        super(MuniSerializer, self).end_object(obj)

class DirSerializer(Serializer):

    def get_dump_object(self, obj):
        dic = super(DirSerializer, self).get_dump_object(obj)
        dic.update({
            'mots': obj.getDenuncias(),
        })
        return dic


    def end_object(self, obj):
        super(DirSerializer, self).end_object(obj)

#--------------------------------------------------------

def busquedaM(request):
    vID = request.GET['id']
    municipios = Municipio.objects.filter(departamento = vID)
    data = serializers.serialize('json', municipios, fields = ('nombre'))

    return HttpResponse(data, content_type='application/json')

def busquedaD(request):
    vID = request.GET['id']
    dirs = Direccion.objects.filter(municipio = vID)
    data = serializers.serialize('json', dirs, fields = ('direccion'))

    return HttpResponse(data, content_type='application/json')

def obtenerD(request):
    codigo = request.GET['code']
    dep = Departamento.objects.get(codigo=codigo)
    dens = Municipio.objects.filter(departamento=dep)

    serial = MuniSerializer()

    data = serial.serialize(dens)

    return HttpResponse(data, content_type='application/json')

def detalleZona(request):
    vZona = request.GET['zona']
    zona = Direccion.objects.filter(direccion=vZona)

    serial = DirSerializer()

    data = serial.serialize(zona)

    return HttpResponse(data, content_type='application/json')


def estadisticas(request):

    departamentos = Departamento.objects.all()
    total = Denuncia.objects.all()
    motivos = Motivo.objects.all()

    context = {
        'departamentos': departamentos,
        'total': len(total),
        'motivos': motivos,
    }

    return render(request,'estadisticas.html', context)

def mapa(request):
    denuncias = Denuncia.objects.exclude(longitud = None,latitud = None)

    context = {
        'denuncias': denuncias.exclude(longitud = 0, latitud = 0),
        'motivos': Motivo.objects.all(),
    }

    return render(request,'mapa.html',context)

def municipioDetail(request, dep, muni):
    splt = dep.split('_')
    splt1 = muni.split('_')

    tmp = splt[0]
    i = 1
    while i<len(splt):
        tmp = tmp + ' ' + splt[i]
        i += 1

    tmp1 = splt1[0]

    i = 1
    while i<len(splt1):
        tmp1 = tmp1 + ' ' + splt1[i]
        i += 1

    try:

        ms = Municipio.objects.filter(departamento__nombre=tmp)
        m = ms.get(nombre=tmp1)
        dirs = Direccion.objects.filter(municipio=m)
    except:
        raise Http404('Error')

    context = {
        'municipio': m,
        'motivos': Motivo.objects.all(),
        'dirs': dirs,
    }

    return render(request, 'municipio_detail.html', context)
