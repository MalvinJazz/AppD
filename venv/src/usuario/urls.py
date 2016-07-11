from django.conf.urls import url

from .views import (
                    privado,
                    registro,
                    usuarioList,
                    UsuarioDetail,
                    UsuarioEdit
                    )
from denuncia.views import denunciasList, DenunciaDetail

urlpatterns = [
    url(r'^$', privado, name='privado'),
    url(r'^denuncias/$', denunciasList, name='lista'),
    url(r'^denuncias/(?P<pk>\d+)/detalles/', DenunciaDetail.as_view(), name='detalles'),
    url(r'^usuarios/crear/$', registro, name="registro"),
    url(r'^usuarios/$', usuarioList, name="lista_u"),
    url(r'^usuarios/(?P<pk>\d+)/detalles/$', UsuarioDetail.as_view(), name="detalles_u"),
    url(r'^usuarios/(?P<pk>\d+)/editar/$', UsuarioEdit.as_view(), name="editar_u"),

]
