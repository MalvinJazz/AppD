from django.shortcuts import render

from .forms import DenunciaForm

# Create your views here.

def denunciar(request):

    form = DenunciaForm(request.POST or None)

    context = {
        'form':form
    }

    if form.is_valid():
        form.save()

    return render(request,'denuncia.html',context)
