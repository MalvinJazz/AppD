from django.conf.urls import url

from .views import (
        busquedaM,
        busquedaD,
        obtenerD,
        estadisticas,
        municipioDetail,
        )

urlpatterns = [

    url(r'^busqM/',busquedaM, name='muni'),
    url(r'^busqD/', busquedaD, name = 'dirs'),
    url(r'^obtD/', obtenerD, name='dens'),
    url(r'^$',estadisticas, name="estadisticas"),
    url(r'^(?P<dep>\w+)/(?P<muni>\w+)$',municipioDetail,name='mDetail'),

]
