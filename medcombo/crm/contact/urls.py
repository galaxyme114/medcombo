from django.conf.urls import url, include
from .views import ListContacCrm
from .views import CreateContacCrm
from .views import DetailContacCrm
from .views import PrivacyPolity
from .views import UpdateContacCrm
from .views import DeleteContacCrm
from .views import PrivacyPolitySend
from .views import PrivacyPolityConfirm
from .views import index
from .views import ContactDelete
from .views import AddUserLead
from medcombo.website.home.views import Home
from .views import CityAutocompleteContact, CityAutocompleteContactTwo
from .views import SendPrivacyPolity

urlpatterns = [
               url(r'^ListContacCrm/$', ListContacCrm.as_view(), name='ListContacCrm'),
               url(r'^DetailContacCrm/(?P<pk>[0-9]+)/$', DetailContacCrm.as_view(), name='DetailContacCrm'),
               url(r'^CreateContacCrm/$', CreateContacCrm.as_view(), name='CreateContacCrm'),
               url(r'^PrivacyPolity/(?P<token>\w{40,40})/$', PrivacyPolity.as_view(), name='PrivacyPolity'),
               url(r'^UpdateContacCrm/(?P<pk>[0-9]+)/$', UpdateContacCrm.as_view(), name='UpdateContacCrm'),
               url(r'^DeleteContacCrm/(?P<pk>[0-9]+)/$', DeleteContacCrm.as_view(), name='DeleteContacCrm'),
               url(r'^SendPrivacyPolityCrm/(?P<pk>[0-9]+)/$', PrivacyPolitySend.as_view(), name='SendPrivacyPolityCrm'),
               url(r'^ConfirmPrivacyPolityCrm/(?P<pk>[0-9]+)/$', PrivacyPolityConfirm.as_view(), name='ConfirmPrivacyPolityCrm'),
               url(r'^inicioejemplo$', index, name='index'),
               url(r'^$', Home.as_view(), name='Home'),
               url(r'^ContactDeleteCrm/$', ContactDelete, name='ContactDeleteCrm'),
               url(r'^city-autocomplete-contact/$', CityAutocompleteContact.as_view(create_field='name'), name='city-autocomplete-contact'),
               url(r'^city-autocomplete-contact-two/$', CityAutocompleteContactTwo.as_view(create_field='name'), name='city-autocomplete-contact-two'),
               url(r'^PrivacyPolitySend/$', SendPrivacyPolity, name='PrivacyPolitySend'),
               url(r'^AddUserLead/$', AddUserLead, name='add_user_lead'),
            ]