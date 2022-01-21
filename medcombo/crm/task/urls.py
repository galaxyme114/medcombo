from django.conf.urls import url
from .views import ListTaskCrm
from .views import CreateTaskCrm
from .views import ReadyTaskCrm
from .views import UpdateTaskCrm
from .views import DeleteTaskCrm
from .views import AppointmentBook
from .views import TaskDelete, AppointmentBookDetail

urlpatterns = [
               url(r'^CreateTaskCrm/$', CreateTaskCrm.as_view(), name='CreateTaskCrm'),
               url(r'^ReadyTaskCrm/(?P<pk>[0-9]+)/$', ReadyTaskCrm.as_view(), name='ReadyTaskCrm'),
               url(r'^ListTaskCrm/$', ListTaskCrm.as_view(), name='ListTaskCrm'),
               url(r'^UpdateTaskCrm/(?P<pk>[0-9]+)/$', UpdateTaskCrm.as_view(), name='UpdateTaskCrm'),
               url(r'^DeleteTaskCrm/(?P<pk>[0-9]+)/$', DeleteTaskCrm.as_view(), name='DeleteTaskCrm'),
               #url(r'^AppointmentBookCrm/(?P<pk>[0-9]+)/$', AppointmentBook.as_view(), name='AppointmentBookCrm'),
               url(r'^TaskDeleteCrm/$', TaskDelete, name='TaskDeleteCrm'),
               url(r'^AppointmentBookCrm/(?P<pk_empleado>[0-9]+)/$', AppointmentBook, name='AppointmentBookCrm'),
               url(r'^AppointmentBookCrm/detail/(?P<pk>[0-9]+)/$', AppointmentBookDetail.as_view(), name='detail_appointment'),
                ]