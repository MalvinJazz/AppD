from django.contrib import admin

from .models import Institucion,Sede,Telefono,Correo

# Register your models here.
admin.site.register(Institucion)
admin.site.register(Sede)
admin.site.register(Telefono)
admin.site.register(Correo)
