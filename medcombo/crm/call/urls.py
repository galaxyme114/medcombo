from django.conf.urls import url
from .views import ListCallCrm
from .views import CreateCallCrm
from .views import DetailCallCrm
from .views import UpdateCallCrm
from .views import DeleteCallCrm

urlpatterns = [
               url(r'^ListCallCrm/$', ListCallCrm.as_view(), name='ListCallCrm'),
               url(r'^DetailCallCrm/(?P<pk>[0-9]+)/$', DetailCallCrm.as_view(), name='DetailCallCrm'),
               url(r'^CreateCallCrm/$', CreateCallCrm.as_view(), name='CreateCallCrm'),
               url(r'^UpdateCallCrm/(?P<pk>[0-9]+)/$', UpdateCallCrm.as_view(), name='UpdateCallCrm'),
               url(r'^DeleteCallCrm/(?P<pk>[0-9]+)/$', DeleteCallCrm.as_view(), name='DeleteCallCrm'),
            ]