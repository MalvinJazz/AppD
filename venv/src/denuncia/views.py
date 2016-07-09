# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core import serializers
from django.core.mail import EmailMessage
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
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

            municipio = denuncia.direccion.municipio
            departamento = municipio.departamento

            motivo = denuncia.motivo
            vIn = motivo.institucion
            vIn = Correo.objects.filter(institucion=vIn)
            print vIn


            #Envio de correo----------------------------------------------------

            text_content = 'Denuncia'
            html_content = '<!DOCTYPE html><html><body><h1>' + str(motivo) + '''</h1></br>
                                <h3> Nombre: ''' + str(denuncia.nombre) + '''<br>
                                DPI: ''' + str(denuncia.dpi) + '''<br>
                                Telefono: ''' + str(denuncia.telefono) + '''</h3></br>
                                <h4>Direccion: ''' + str(denuncia.direccion) + ''',
                                ''' + str(municipio) + ', ' + str(departamento) +'''.
                                <i>(Con referencia en: '''+str(denuncia.referencia)+''')</i> </h4>
                                </br> <h5> Denuncio: </h5></br> <p>
                                ''' + str(denuncia.denuncia) + '''</p></body>
                                <footer><i>Los archivos quedan a cargo de la
                                 entidad indicada.</i><br>
                                <i>Todos los datos de este correo son
                                 confidenciales y no deben ser difundidos
                                a nadie más que las entidades interesadas
                                 en ellos.</i></footer></html>'''

            from_email = '"Denuncia Movil" <denunciamovil@gmail.com>'
            to = vIn
            msg = EmailMultiAlternatives(motivo, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            if request.FILES:
                msg.attach(archivo.name,archivo.read(),archivo.content_type)
            msg.send()

            # connection = mail.get_connection()
            # connection.open()
            #
            # correo = EmailMessage(
            #     motivo,
            #     denuncia.denuncia,
            #     'denunciamovil@gmail.com',
            #     vIn,
            #     connection=connection,
            #     )
            #
            # if request.FILES:
            #     correo.attach(archivo.name,archivo.read(),archivo.content_type)
            #
            # print correo.subject, correo.from_email, correo.to
            #
            # correo.send(fail_silently = False)
            # connection.close()
            # print 'conexion cerrada'

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
        # 'instituciones': instituciones,
        'departamentos': departamentos,
        }

    return render(request,'denuncia.html',context)


def success(request):
    return render(request,'success.html',{})

def busquedaMo(request):
    vID = request.GET['id']
    mots = Motivo.objects.filter(institucion__tipo = vID)
    data = serializers.serialize('json', mots, fields = ('motivo'))

    return HttpResponse(data, content_type='application/json')

@login_required(login_url='inicio')
def denunciasList(request):
    zona = request.user.zona
    tipo = request.user.institucion.tipo

    if tipo == 'NG':
        denuncias = Denuncia.objects.filter(direccion=zona)
    else:
        denuncias = Denuncia.objects.filter(
            direccion=zona, motivo__institucion__tipo=tipo
        )

    context = {
        "denuncias": denuncias,
    }

    return render(request,'usuario/denuncias_list.html', context)

class DenunciaDetail(LoginRequiredMixin,DetailView):
    model = Denuncia
    login_url = 'inicio'
    template_name = 'usuario/denuncia_detail.html'

    def dispatch(self, request, *args, **kwargs):
        handler = super(DenunciaDetail, self).dispatch(request, *args, **kwargs)

        objeto = self.get_object(self.get_queryset())

        if objeto.direccion != request.user.zona:
            if objeto.direccion.municipio != request.user.zona.municipio:
                return HttpResponse('No puedes ver esto.')

        return handler

    def get_context_data(self, **kwargs):
        context = super(DenunciaDetail, self).get_context_data(**kwargs)

        objeto = self.get_object(self.get_queryset())
        geo = False
        if objeto.latitud is not None and objeto.longitud is not None:
            if objeto.latitud != 0 and objeto.longitud != 0:
                geo = True

        context.update({
            "geo": geo,
            "label": objeto.motivo.motivo[0]
        })


        return context
