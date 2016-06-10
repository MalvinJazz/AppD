from django.shortcuts import render

from .models import Departamento, Municipio, Direccion

# Create your views here.
def busquedaM(request):
    vID = request.GET['id']
    municipios = Municipio.objects.filter(departamento = vID)
    data = serializers.serialize('json', municipios, fields = ('nombre'))

    return HttpResponse(data, content_type='application/json')
