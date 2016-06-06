from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .forms import DenunciaForm
from institucion.models import Correo

# Create your views here.

def denunciar(request):

    form = DenunciaForm(request.POST or None)

    context = {
        'form':form
    }

    if form.is_valid():
        vForm = form.save()
        motivo = vForm.motivo
        vIn = motivo.institucion
        vIn = Correo.objects.filter(institucion = vIn)

        print vIn

        send_mail(
            motivo.motivo,
            vForm.descripcion,
            'prueba',
            vIn,
        )

        #redirect('/denuncia')

    return render(request,'denuncia.html',context)

def home(request):

    context = {
        'titulo':'Inicio'
    }
    return render(request, 'inicio.html',context)
