# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone

from .forms import UserCreationForm, InicioForm
from .models import Usuario
from localizaciones.models import Departamento

def registro(request):
    if not reques.user.is_authenticated():

        form = UserCreationForm(request.POST or None)

        context = {
            "form": form,
            "departamentos": Departamento.objects.all()
        }

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/inicio')

        return render(request, 'usuario/registro.html', context)

    return HttpResponseRedirect('/')

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
                    return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')

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
    return HttpResponseRedirect('/')

@login_required(login_url='inicio')
def privado(request):
    return render(request, 'usuario/privado.html', {})
