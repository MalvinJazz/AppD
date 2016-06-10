from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

from .forms import DenunciaForm
from institucion.models import Correo, Institucion
from localizaciones.models import Departamento, Municipio, Direccion

# Create your views here.

def denunciar(request):

    form = DenunciaForm(request.POST or None)
    instituciones = Institucion.objects.all()
    departamentos = Departamento.objects.all()

    context = {
        'form':form,
        'instituciones': instituciones,
        'departamentos': departamentos,
    }

    if form.is_valid():
        vForm = form.save()
        motivo = vForm.motivo
        vIn = motivo.institucion
        vIn = Correo.objects.filter(institucion = vIn)

        try:
            send_mail(
                motivo.motivo,
                vForm.descripcion,
                'prueba',
                vIn,
                )
        except gaierror:
            print "no funciono"

        #redirect('/denuncia')

    return render(request,'denuncia.html',context)

def success(request):
    render(request,'success.html',{})

#
# def home(request):
#
#     context = {
#         'titulo':'Inicio'
#     }
#     return render(request, 'inicio.html',context)
