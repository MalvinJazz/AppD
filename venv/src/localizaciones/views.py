from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

from .models import Departamento, Municipio, Direccion

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
