from django.contrib import admin

from .models import Departamento,Municipio,Direccion

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Direccion)
