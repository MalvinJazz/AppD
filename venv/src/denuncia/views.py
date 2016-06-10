from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core import serializers
from django.core.mail import EmailMessage
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect

#from .forms import DenunciaForm
from institucion.models import Correo, Institucion
from localizaciones.models import Departamento, Municipio, Direccion
from .models import Motivo, Denuncia
# Create your views here.

# def denunciar(request):
#
#     instituciones = Institucion.objects.all()
#     departamentos = Departamento.objects.all()
#     if request.method == 'POST':
#         form = DenunciaForm(request.POST, request.FILES)
#         Post = True
#
#         if form.is_valid():
#             is_valid = True
#
#             # vForm = form.save(commit = False)
#             vForm = form.save()
#             motivo = vForm.motivo
#             vIn = motivo.institucion
#             # foto = request.FILES['archivo']
#             foto = vForm.archivo
#
#             print foto
#
#             # vForm.archivo = foto
#
#             # vForm.save()
#
#             vIn = Correo.objects.filter(institucion = vIn)
#
#             # email = EmailMessage(
#             #     motivo,
#             #     vForm.denuncia,
#             #     vIn
#                 # )
#
#             # email.attach_file(vForm.archivo.path)
#
#             # email.send(fail_silently = False)
#
#     else:
#         form = DenunciaForm()
#         Post = False
#         is_valid = False
#
#     context = {
#         'form':form,
#         'instituciones': instituciones,
#         'departamentos': departamentos,
#         }
#
#     return render(request,'denuncia.html',context)
class DenunciaCreate(CreateView):
    model = Denuncia
    template_name = 'denuncia.html'
    # succes_url = 'institucion:list'
    fields = [
        'nombre',
        'dpi',
        'direccion',
        'denuncia',
        'archivo',
        'motivo',
    ]

    def get_context_data(self, **kwargs):
        context = super(DenunciaCreate,self).get_context_data(**kwargs)
        departamentos = Departamento.objects.all()
        instituciones = Institucion.objects.all()

        context.update({

            "departamentos": departamentos,
            "instituciones": instituciones,

            })

        return context

def success(request):
    return render(request,'success.html',{})

def busquedaMo(request):
    vID = request.GET['id']
    mots = Motivo.objects.filter(institucion = vID)
    data = serializers.serialize('json', mots, fields = ('motivo'))

    return HttpResponse(data, content_type='application/json')
