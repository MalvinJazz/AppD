# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import UserCreationForm, InicioForm
from .models import Usuario
from localizaciones.models import Departamento


@login_required(login_url="inicio")
def registro(request):

    form = UserCreationForm(request.POST or None)

    context = {
        "form": form,
        "departamentos": Departamento.objects.all()
    }

    if form.is_valid():
        form.save()

        return HttpResponseRedirect('/')

    return render(request, 'usuario/registro.html', context)


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

@login_required(login_url='inicio')
def privado(request):
    return render(request, 'usuario/privado.html', {})

@login_required(login_url='inicio')
def usuarioList(request):

    if not request.user.is_staff:
        return render(request, 'error/permisos.html', {})

    context = {
        'usuarios': Usuario.objects.exclude(id=request.user.id)
    }

    return render(request, 'usuario/usuarios_list.html', context)

class UsuarioDetail(LoginRequiredMixin, DetailView):
    model = Usuario
    login_url = 'inicio'
    template_name = 'usuario/usuario_detail.html'
    slug_field = 'username'

    def dispatch(self, request, *args, **kwargs):
        handler = super(UsuarioDetail, self).dispatch(request, *args, **kwargs)

        if not request.user.is_staff:
            return render(request, 'error/permisos.html', {})

        if self.get_object(self.queryset) == request.user:
            return redirect('usuario:privado')

        return handler


class UsuarioEdit(LoginRequiredMixin, UpdateView):
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
        'is_active',
        'tipo',
        'institucion',
        'zona'
    ]

    def dispatch(self, request, *args, **kwargs):

        handler = super(UsuarioEdit, self).dispatch(request, *args, **kwargs)

        if not request.user.is_staff:
            return render(request, 'error/permisos.html', {})

        if self.get_object(self.queryset) == request.user:
            return redirect('usuario:privado')

        return handler

    def get_context_data(self, **kwargs):

    	context = super(UsuarioEdit, self).get_context_data(**kwargs)
    	Departamentos = Departamento.objects.all()

    	context.update({
    		"departamentos":Departamentos,
    		})

    	return context
