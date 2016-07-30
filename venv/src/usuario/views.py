# -*- coding: utf-8 -*-

# import collections
# import time
import calendar

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import UserCreationForm, InicioForm, CambioPassForm
from .models import Usuario
from localizaciones.models import Departamento
from denuncia.models import Denuncia


@login_required(login_url="inicio")
def registro(request):

    if request.user.is_staff:

        form = UserCreationForm(request.POST or None)

        context = {
            "form": form,
            "departamentos": Departamento.objects.all()
        }

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')

        return render(request, 'usuario/registro.html', context)

    return render(request, 'error/permisos.html', {})


def inicio(request):
    if request.user.is_authenticated():

        return HttpResponseRedirect('/usuario')

    if request.POST:

        form = InicioForm(request.POST)

        if form.is_valid():

            username = request.POST['username']
            password = request.POST['password']

            usuario = authenticate(username = username, password = password)

            if usuario is not None:
                if usuario.is_active:
                    login(request, usuario)

                    context = {
                        "form": form
                    }

                    if request.GET:
                        if request.GET['next'] != '/logout':
                            return HttpResponseRedirect(request.GET['next'])

                    return redirect('usuario:privado')

                else:
                    messages.error(request, 'Usuario inactivo, comunicate con tu administrador.')
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'La contraseña o el usuario no coinciden.')
                return HttpResponseRedirect('/')

        else:
            messages.error(request, 'Datos invalidos.')

    else:

        form = InicioForm()

        context = {
            "form": form
        }

        return render(request, 'usuario/inicio.html', context)

@login_required(login_url='inicio')
def cerrar(request):
    request.user.ultima_conexion = timezone.now()
    request.user.save()

    logout(request)
    return redirect('inicio')

def getDenuncias():
    dias = timezone.now().day

    i=1
    # denuncias = collections.OrderedDict()
    denuncias = []
    while i<=dias:
        denuncias.append((
            str(i), len(Denuncia.objects.filter(
                fecha__year = timezone.now().year
            ).filter(
                fecha__month = timezone.now().month
            ).filter(
                fecha__day = i
            )), len(Denuncia.objects.filter(
                fecha__year = timezone.now().year
            ).filter(
                fecha__month = timezone.now().month - 1
            ).filter(
                fecha__day = i
            )), len(Denuncia.objects.filter(
                fecha__year = timezone.now().year
            ).filter(
                fecha__month = timezone.now().month - 2
            ).filter(
                fecha__day = i))))
        i += 1

    return denuncias

@login_required(login_url='inicio')
def privado(request):

    context = {
        'denuncias': getDenuncias(),
        'tiempo1': timezone.now().strftime('%B'),
        'tiempo2': calendar.month_name[timezone.now().month - 1],
        'tiempo3': calendar.month_name[timezone.now().month - 2]
    }

    return render(request, 'usuario/privado.html', context)


@login_required(login_url='inicio')
def usuarioList(request):

    if not request.user.is_staff:
        return render(request, 'error/permisos.html', {})

    usuarios = Usuario.objects.exclude(id=request.user.id)

    if request.GET:
        if request.GET['institucion']:
            usuarios = usuarios.filter(
                        institucion__nombre=request.GET['institucion']
                        )


    context = {
        'usuarios': usuarios
    }

    return render(request, 'usuario/usuarios_list.html', context)

class UsuarioDetail(DetailView):
    model = Usuario
    login_url = 'inicio'
    template_name = 'usuario/usuario_detail.html'
    slug_field = 'username'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        handler = super(UsuarioDetail, self).dispatch(request, *args, **kwargs)

        if self.get_object(self.queryset) == request.user:
            return redirect('usuario:privado')

        if not request.user.is_staff:
            return render(request, 'error/permisos.html', {})

        return handler


class UsuarioEdit(UpdateView):
    model = Usuario
    login_url = 'inicio'
    template_name = 'usuario/usuario_edit.html'
    slug_field = 'username'
    success_url = reverse_lazy('usuario:lista_u')

    fields = [
        'nombre',
        'apellidos',
        'correo',
        'is_staff',
        'is_admin',
        'is_res',
        'is_active',
        'institucion',
        'zona'
    ]

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        handler = super(UsuarioEdit, self).dispatch(request, *args, **kwargs)

        if self.get_object(self.queryset) == request.user:
            return redirect('usuario:privado')

        if not request.user.is_staff:
            return render(request, 'error/permisos.html', {})

        return handler

    def get_context_data(self, **kwargs):

    	context = super(UsuarioEdit, self).get_context_data(**kwargs)
    	Departamentos = Departamento.objects.all()

    	context.update({
    		"departamentos":Departamentos,
    		})

    	return context

@login_required(login_url='inicio')
def cambiarPass(request):
    if request.method == 'POST':
        form = CambioPassForm(request.POST)

        if form.is_valid():

            actual_pass = request.POST['actual']
            if request.user.check_password(actual_pass):
                nuevo_pass = request.POST['password1']

                if not request.user.check_password(nuevo_pass):

                    request.user.set_password(nuevo_pass)
                    request.user.save()

                    logout(request)
                    messages.info(request, 'Inicia sesión de nuevo porfavor.')
                    return redirect('inicio')
                else:
                    messages.error(request, 'No puedes usar tu actual contraseña.')

            else:
                messages.error(request, 'Primero ingresa tu contraseña actual.')
    else:
        form = CambioPassForm()

    return render(request, 'cambio_pass.html', {'form':form})
