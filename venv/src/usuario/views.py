from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, InicioForm
