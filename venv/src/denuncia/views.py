from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core import mail
from django.core import serializers
from django.core.mail import EmailMessage
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect

from .forms import DenunciaForm
from institucion.models import Correo, Institucion
from localizaciones.models import Departamento, Municipio, Direccion
from .models import Motivo, Denuncia

def denunciar(request):

    instituciones = Institucion.objects.all()
    departamentos = Departamento.objects.all()
    if request.method == 'POST':
        form = DenunciaForm(request.POST or None, request.FILES or None)
        Post = True

        if form.is_valid():
            clean = form.cleaned_data

            is_valid = True

            denuncia = Denuncia()

            print clean
            print request.FILES
            print request.POST

            denuncia.nombre = clean['nombre']
            denuncia.dpi = clean['dpi']
            denuncia.telefono = clean['telefono']
            denuncia.direccion = clean['direccion']
            denuncia.referencia = clean['referencia']
            denuncia.denuncia = clean['denuncia']
            denuncia.latitud = request.POST['lat']
            denuncia.longitud = request.POST['lon']

            if request.FILES:
                archivo = request.FILES['file']

            denuncia.motivo = clean['motivo']

            denuncia.save()

            motivo = denuncia.motivo
            vIn = motivo.institucion
            vIn = Correo.objects.filter(institucion=vIn)
            print vIn


            #Envio de correo----------------------------------------------------
            connection = mail.get_connection()
            connection.open()

            correo = EmailMessage(
                motivo,
                denuncia.denuncia,
                'denunciamovil@gmail.com',
                vIn,
                connection=connection,
                )

            if request.FILES:
                correo.attach(archivo.name,archivo.read(),archivo.content_type)

            print correo.subject, correo.from_email, correo.to

            correo.send(fail_silently = False)
            connection.close()
            print 'conexion cerrada'
            #Cierre de conexion-------------------------------------------------

            #Trigger de sumatoria a motivo--------------------------------------
            motivo.cantidad = len(Denuncia.objects.filter(motivo=motivo))
            motivo.save()

            return redirect('success')

        else:
            print "no funciona"

    else:
        form = DenunciaForm()
        Post = False
        is_valid = False

    context = {
        'form':form,
        'instituciones': instituciones,
        'departamentos': departamentos,
        }

    return render(request,'denuncia.html',context)

# class DenunciaCreate(CreateView):
#     model = Denuncia
#     template_name = 'denuncia.html'
#     # succes_url = 'institucion:list'
#     fields = [
#         'nombre',
#         'dpi',
#         'direccion',
#         'denuncia',
#         'archivo',
#         'motivo',
#     ]
#
#     def get_context_data(self, **kwargs):
#         context = super(DenunciaCreate,self).get_context_data(**kwargs)
#         departamentos = Departamento.objects.all()
#         instituciones = Institucion.objects.all()
#
#         context.update({
#
#             "departamentos": departamentos,
#             "instituciones": instituciones,
#
#             })
#
#         return context
#
#     def form_valid(self, form):
#         self.object = form.save()

def success(request):
    return render(request,'success.html',{})

def busquedaMo(request):
    vID = request.GET['id']
    mots = Motivo.objects.filter(institucion = vID)
    data = serializers.serialize('json', mots, fields = ('motivo'))

    return HttpResponse(data, content_type='application/json')
