from django.conf.urls import url
from .views import ListGroups
from .views import DetailGroups
from .views import CreateGroups
from .views import DeleteGroups
from .views import UpdateGroups
from .views import DeleteGroupActive

urlpatterns = [
               url(r'^List_Groups$', ListGroups.as_view(), name='list_groups'),
               url(r'^Groups/Create/$', CreateGroups.as_view(), name='create_groups'),
               url(r'^List_Groups/Detail/(?P<pk>[0-9]+)/$', DetailGroups.as_view(), name='detail_groups'),
               url(r'^Groups/Update/(?P<pk>[0-9]+)/$', UpdateGroups.as_view(), name='update_groups'),
               url(r'^Groups/Delete/(?P<pk>[0-9]+)/$', DeleteGroups.as_view(), name='delete_groups'),
               url(r'^DeleteGroup/$', DeleteGroupActive, name='DeleteGroup'),
              ]