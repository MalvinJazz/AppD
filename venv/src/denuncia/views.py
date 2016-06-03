from django.shortcuts import render

from .forms import DenunciaForm

# Create your views here.

def denunciar(request):

    form = DenunciaForm

    context = {
        'form':form
    }

    return render(request,'denuncia.html',context)
