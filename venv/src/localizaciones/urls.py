from django.conf.urls import url

from .views import busquedaM, busquedaD, obtenerD

urlpatterns = [

    url(r'^busqM/',busquedaM, name='muni'),
    url(r'^busqD/', busquedaD, name = 'dirs'),
    url(r'^obtD/', obtenerD, name='dens'),

]
