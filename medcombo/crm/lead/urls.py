from django.conf.urls import url
from .views import LeadCrm
from .views import LeadSuccessCrm

urlpatterns = [
               url(r'^LeadCrm/$', LeadCrm.as_view(), name='LeadCrm'),
               url(r'^LeadSuccessCrm/$', LeadSuccessCrm.as_view(), name='LeadSuccessCrm'),
            ]