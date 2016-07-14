from django.conf.urls import url, include
from tastypie.api import Api

from .api import MotivoResource, DenunciaResource

denuncia_api = Api(api_name='d1')
denuncia_api.register(MotivoResource())
denuncia_api.register(DenunciaResource())

urlpatterns = [
    url(r'^api/', include(denuncia_api.urls)),
]
