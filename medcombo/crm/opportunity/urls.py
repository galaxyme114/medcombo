from django.conf.urls import url
from .views import CreateOpportunityCrm
from .views import DetailOpportunityCrm
from .views import OpportunityList
from .views import add_state
from .views import OpportunitySummary
from .views import OpportunitySummaryDetail
from .views import OpportunityChangePercent
from .views import UpdateOpportunityCrm
from .views import DeleteOpportunity

urlpatterns = [
               url(r'^DetailOpportunityCrm/(?P<pk>[0-9]+)/$', DetailOpportunityCrm.as_view(), name='DetailOpportunityCrm'),
               url(r'^CreateOpportunityCrm/$', CreateOpportunityCrm.as_view(), name='CreateOpportunityCrm'),
               url(r'^UpdateOpportunityCrm/(?P<pk>[0-9]+)/$', UpdateOpportunityCrm.as_view(), name='UpdateOpportunityCrm'),
               url(r'^OpportunityList/$', OpportunityList.as_view(), name='OpportunityList'),
               url(r'^ajax/load_state$', add_state, name='ajax_load_state'),
               url(r'^OpportunitySummary/$', OpportunitySummary.as_view(), name='OpportunitySummary'),
               url(r'^OpportunitySummaryDetail/(?P<pk>[0-9]+)/$', OpportunitySummaryDetail.as_view(), name='OpportunitySummaryDetail'),
               url(r'^opportunitychangepercent$',OpportunityChangePercent, name='opportunitychangepercent'),
               url(r'^delete_opportunity$',DeleteOpportunity, name='delete_opportunity'),
            ]