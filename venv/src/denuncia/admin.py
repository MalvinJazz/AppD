from django.contrib import admin

from .models import Denuncia, Motivo


class DenunciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'dpi', 'telefono', 'motivo', 'denuncia','direccion', 'fecha']

class MotivoAdmin(admin.ModelAdmin):
    list_display = ['motivo','institucion']

admin.site.register(Denuncia, DenunciaAdmin)
admin.site.register(Motivo, MotivoAdmin)

# Register your models here.
