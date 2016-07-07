from django.conf.urls import url

from .views import privado

urlpatterns = [
    url(r'^$', privado, name='privado')
]
