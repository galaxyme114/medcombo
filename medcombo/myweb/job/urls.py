from django.conf.urls import url
from .views import CreateJob
from .views import ListJob
from .views import UpdateJob
from .views import DetailJob
from .views import DeleteJob
from .views import ActiveJob
from .views import RegistrationJob
from .views import ListFrontJob
from .views import DetailFrontJob
from .views import ListResume
from .views import DetailResume
from .views import ProcessResume
from .views import DiscardResume
from .views import DeleteResume
from .views import SearchOffer
from .views import SearchParticipant

urlpatterns = [
               url(r'^create_offer/$', CreateJob.as_view(), name='create_offer'),
               url(r'^update_offer/(?P<pk>[0-9]+)/$', UpdateJob.as_view(), name='update_offer'),
               url(r'^list_offers/$', ListJob.as_view(), name='list_offers'),
               url(r'^job_offers/(?P<pk>[0-9]+)/$', DetailJob.as_view(), name='detail_offers'),
               url(r'^delete_offers/$', DeleteJob, name='delete_offers'),
               url(r'^active_offers/$', ActiveJob, name='active_offers'),
               url(r'^registration_offers/(?P<pk>[0-9]+)/$', RegistrationJob.as_view(), name='registration_offers'),
               url(r'^list-front-offers/$', ListFrontJob.as_view(), name='list-front-offers'),
               url(r'^detail_front_offers/(?P<pk>[0-9]+)/$', DetailFrontJob.as_view(), name='detail_front_offers'),
               url(r'^list_participants/(?P<pk>[0-9]+)/$', ListResume.as_view(), name='list_participants'),
               url(r'^job_participant/(?P<pk>[0-9]+)/$', DetailResume.as_view(), name='detail_participant'),
               url(r'^process_participant/$', ProcessResume, name='process_participant'),
               url(r'^discard_participant/$', DiscardResume, name='discard_participant'),
               url(r'^delete_participant/$', DeleteResume, name='delete_participant'),
               url(r'^search_offers/$', SearchOffer, name='search_offers'),
               url(r'^search_participant/$', SearchParticipant, name='search_participant'),
              ]