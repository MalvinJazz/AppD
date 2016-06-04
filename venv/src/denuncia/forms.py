from django import forms

from .models import Denuncia, Motivo

class DenunciaForm(forms.ModelForm):

    class Meta:
        model = Denuncia

        fields = [
            'nombre',
            'dpi',
            'direccion',
            'descripcion',
            'solicitud',
            'archivo',
            'motivo',
        ]
