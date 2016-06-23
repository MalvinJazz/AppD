from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import Serializer
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_text, is_protected_type

from .models import Departamento, Municipio, Direccion
from denuncia.models import Denuncia, Motivo

#--------------------------------------------------------
#Serializador de json------------------------------------
class MuniSerializer(Serializer):

    def get_dump_object(self, obj):
        dic = super(MuniSerializer, self).get_dump_object(obj)
        dic.update({
            'cant': obj.sumDirecciones()
        })
        return dic


    def end_object(self, obj):
        super(MuniSerializer, self).end_object(obj)



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

    print data

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

    for dato in departamentos:
        print str(dato.codigo)+"--"+str(dato.sumMunicipios())

    return render(request,'estadisticas.html', context)

def mapa(request):
    denuncias = Denuncia.objects.exclude(longitud=None,latitud=None)
    print denuncias

    return render(request,'mapa.html',{'denuncias': denuncias})
