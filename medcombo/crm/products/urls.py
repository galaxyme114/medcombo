from django.conf.urls import url
from .views import ListProductCrm
from .views import CreateProductCrm
from .views import DetailProductCrm
from .views import UpdateProductCrm
from .views import DeleteProductCrm
from .views import DeleteCrmProduct

urlpatterns = [
               url(r'^ListProductCrm/$', ListProductCrm.as_view(), name='ListProductCrm'),
               url(r'^CreateProductCrm/$', CreateProductCrm.as_view(), name='CreateProductCrm'),               
               url(r'^DetailProductCrm/(?P<pk>[0-9]+)/$', DetailProductCrm.as_view(), name='DetailProductCrm'),
               url(r'^UpdateProductCrm/(?P<pk>[0-9]+)/$', UpdateProductCrm.as_view(), name='UpdateProductCrm'),
               url(r'^DeleteProductCrm/(?P<pk>[0-9]+)/$', DeleteProductCrm.as_view(), name='DeleteProductCrm'),
               url(r'^ProductDeleteCrm/$', DeleteCrmProduct, name='ProductDeleteCrm'),
]