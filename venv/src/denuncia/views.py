# -*- coding: utf-8 -*-
from datetime import datetime, date, time, timedelta

from django.shortcuts import render, redirect
from django.utils.encoding import smart_str, smart_unicode
from django.core.mail import send_mail
from django.core.serializers.json import Serializer
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core import mail
from django.core import serializers
from django.core.mail import EmailMessage
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import DenunciaForm
from institucion.models import Correo, Institucion
from localizaciones.models import Departamento, Municipio, Direccion
from .models import Motivo, Denuncia

#------------------------------------------------

class DenunciaSerializer(Serializer):

    def get_dump_object(self, obj):
        fecha = timezone.localtime(obj.fecha)

        dic = {
            "sprite": obj.getSprite(),
            "motivo": obj.motivo.motivo,
            "fecha": fecha.strftime('%d-%b-%Y %-I:%M %p %Z'),
            "latitud": obj.latitud,
            "longitud": obj.longitud,
        }

        return dic


def getDenuncias(request):

    denuncias = Denuncia.objects.exclude(longitud = 0, latitud = 0)
    denuncias = denuncias.exclude(longitud = None, latitud = None)

    # print timezone.now()-timedelta(days=11)

    fecha_desde = timezone.now()-timedelta(hours=24)
    denuncias = denuncias.filter(
        fecha__range = (
            fecha_desde,
            timezone.now()
        )
    )

    data = DenunciaSerializer().serialize(denuncias)

    return HttpResponse(data, content_type='application/json')

#------------------------------------------------

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
            html_content = '<!DOCTYPE html><html><body><h1>' + smart_str(motivo) + '''</h1></br>
                                <h3> Nombre: ''' + smart_str(denuncia.nombre) + '''<br>
                                DPI: ''' + smart_str(denuncia.dpi) + '''<br>
                                Telefono: ''' + smart_str(denuncia.telefono) + '''</h3></br>
                                <h4>Direccion: ''' + smart_str(denuncia.direccion) + ''',
                                ''' + smart_str(municipio) + ', ' + smart_str(departamento) +'''.
                                <i>(Con referencia en: '''+smart_str(denuncia.referencia)+''')</i> </h4>
                                </br> <h5> Denuncio: </h5></br> <p>
                                ''' + smart_str(denuncia.denuncia) + '''</p></body>
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

            return redirect('success')

        else:
            messages.error(request, 'Ingresa correctamente los datos.')

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

    try:
        if request.GET['tipo']:
            mots = Motivo.objects.filter(institucion__id=vID)

    except:
        mots = Motivo.objects.filter(institucion__tipo = vID)

    data = serializers.serialize('json', mots, fields = ('motivo'))

    return HttpResponse(data, content_type='application/json')

@login_required(login_url='inicio')
def denunciasList(request):
    zona = request.user.zona
    tipo = request.user.institucion.tipo
    institucion = request.user.institucion

    motivos = Motivo.objects.all()

    if request.user.is_staff:
        denuncias = Denuncia.objects.all().order_by('-fecha')
    else:
        if tipo == 'NG':
            denuncias = Denuncia.objects.filter(direccion=zona).order_by('-fecha')
        else:
            denuncias = Denuncia.objects.filter(
                # direccion=zona,
                motivo__institucion=institucion
                ).order_by('-fecha')

            motivos = motivos.filter(institucion=request.user.institucion)

            if request.user.is_res:
                fecha_hasta = timezone.now()+timedelta(days=1)
                fecha_desde = timezone.now()-timedelta(days=8)
                print fecha_desde
                print fecha_hasta
                denuncias = denuncias.filter(
                        fecha__range=(
                            fecha_desde,
                            fecha_hasta)
                            )

    # errores = []

    if request.GET:
        try:
            denuncias = denuncias.filter(fecha__year=request.GET['año'])
            # errores.append('Año:' + str(request.GET['año']))
        except:
            pass

        try:
            denuncias = denuncias.filter(fecha__month=request.GET['mes'])
            # errores.append('Mes:' + str(request.GET['mes']))
        except:
            pass

        try:
            denuncias = denuncias.filter(fecha__day=request.GET['dia'])
            # errores.append('Dia:' + str(request.GET['dia']))
        except:
            pass

        try:
            denuncias = denuncias.filter(nombre__icontains=request.GET['nombre'])
            # denuncias = denuncias.filter(nombre__iexact=request.GET['nombre'])
            # errores.append('Nombre:' + str(request.GET['nombre']))
        except:
            pass

        try:
            denuncias = denuncias.filter(motivo__id=request.GET['motivo'])
            # errores.append('Motivo:' + str(
            #                         Motivo.objects.get(request.GET['motivo'])))
        except:
            pass
        try:
            if request.user.is_staff or tipo == 'NG':
                denuncias = denuncias.filter(motivo__institucion=request.GET['institucion'])
            else:
                denuncias = denuncias.filter(motivo__institucion=request.user.institucion)
            # errores.append('Institucion:' + str(
            #                         Institucion.objects.get(request.GET['motivo'])))
        except:
            pass

    if len(denuncias) == 0:
        messages.error(request, 'No existen coincidencias con esos parametros.')
        # for error in errores:
        #     messages.error(request, error)

    context = {
        "denuncias": denuncias,
        "motivos": motivos
    }

    if request.user.is_staff or tipo == 'NG':
        context.update({
            "instituciones": Institucion.objects.all()
        })


    return render(request,'usuario/denuncias_list.html', context)

class DenunciaDetail(DetailView):
    model = Denuncia
    login_url = 'inicio'
    template_name = 'usuario/denuncia_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        handler = super(DenunciaDetail, self).dispatch(request, *args, **kwargs)

        user = request.user
        objeto = self.get_object(self.get_queryset())

        if not user.is_staff:
            if user.is_admin and user.institucion.tipo == 'NG':
                if objeto.direccion != user.zona:
                    if objeto.direccion.municipio != user.zona.municipio:
                        return render(request, 'error/permisos.html', {})
            else:
                if objeto.motivo.institucion != user.institucion:
                    return render(request, 'error/permisos.html', {})

                fecha_limite = timezone.now().replace(day=timezone.now().day-8)
                if user.is_res and objeto.fecha < fecha_limite:
                    return render(request, 'error/permisos.html', {})

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
