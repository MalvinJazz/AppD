from django.conf.urls import url

from .views import privado, registro
from denuncia.views import denunciasList, DenunciaDetail

urlpatterns = [
    url(r'^$', privado, name='privado'),
    url(r'^denuncias/$', denunciasList, name='lista'),
    url(r'^denuncias/(?P<pk>\d+)/detalles/', DenunciaDetail.as_view(), name='detalles'),
    url(r'^crear/usuario/$', registro, name="registro"),
]
