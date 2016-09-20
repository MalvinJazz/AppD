# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Denuncia, Motivo


class DenunciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'motivo', 'tipo', 'denuncia','direccion','referencia', 'fecha']

class MotivoAdmin(admin.ModelAdmin):
    list_display = ['id', 'motivo' ,'cantidad', 'get_instituciones']

    # def get_instituciones(self, obj):
    #     return ", ".join([m.nombre for m in obj.instituciones.all()])

admin.site.register(Denuncia, DenunciaAdmin)
admin.site.register(Motivo, MotivoAdmin)

# Register your models here.
