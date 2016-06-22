from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

from .models import Departamento, Municipio, Direccion
from denuncia.models import Denuncia, Motivo

# Create your views here.
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
    print dep
    dens = Municipio.objects.filter(departamento=dep)
    data = serializers.serialize('json', dens)

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
