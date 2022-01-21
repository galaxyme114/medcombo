from django.conf.urls import url
from .views import EconomicProposal
from .views import EconomicProposal_create
from .views import EconomicProposal_update
from .views import EconomicProposal_delete

urlpatterns = [
               url(r'^economic-proposal/$', EconomicProposal.as_view(), name='economic-proposal'),
               url(r'^economic-proposal-create/$', EconomicProposal_create.as_view(), name='economic-proposal-create'),
               url(r'^economic-proposal-update/(?P<pk>\d+)/$', EconomicProposal_update.as_view(), name='economic-proposal-update'),
               url(r'^Deleteproposal/$', EconomicProposal_delete, name='delete_proposal'),
                ]

