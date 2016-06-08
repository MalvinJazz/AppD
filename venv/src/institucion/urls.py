from django.conf.urls import url
from .views import lista, InstitucionDetail

urlpatterns = [

    url(r'^$', lista, name = 'list'),
    url(r'^(?P<pk>\d+)$', InstitucionDetail.as_view(), name = 'detail'),

]
