from django.conf.urls import url
from .views import ListContacCrm
from .views import CreateContacCrm
from .views import DetailContacCrm
from .views import PrivacyPolicy
from .views import UpdateContacCrm
from .views import DeleteContacCrm
from .views import ListTaskCrm
from .views import CreateTaskCrm
from .views import ReadyTaskCrm
from .views import UpdateTaskCrm
from .views import DeleteTaskCrm
from .views import ListCallCrm
from .views import CreateCallCrm
from .views import DetailCallCrm
from .views import UpdateCallCrm
from .views import DeleteCallCrm
from .views import CreateOpportunityCrm
from .views import DetailOpportunityCrm
from .views import OpportunityList
from .views import add_state
from .views import LeadCrm
from .views import LeadSuccessCrm
from .views import ListProductCrm
from .views import CreateProductCrm
from .views import DetailProductCrm
from .views import UpdateProductCrm
from .views import AdminUserCrm
from .views import AdminProductCrm
from .views import AdminMywebCrm
from .views import AdminKeywordCrm
from .views import AdminUserConfirmGenerate
from .views import AdminUserConfirmRestablecer
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete

urlpatterns = [
               url(r'^ListContacCrm/$', ListContacCrm.as_view(), name='ListContacCrm'),
               url(r'^DetailContacCrm/(?P<pk>[0-9]+)/$', DetailContacCrm.as_view(), name='DetailContacCrm'),
               url(r'^CreateContacCrm/$', CreateContacCrm.as_view(), name='CreateContacCrm'),
               url(r'^PrivacyPolicy/$', PrivacyPolicy.as_view(), name='PrivacyPolicy'),
               url(r'^UpdateContacCrm/(?P<pk>[0-9]+)/$', UpdateContacCrm.as_view(), name='UpdateContacCrm'),
               url(r'^DeleteContacCrm/(?P<pk>[0-9]+)/$', DeleteContacCrm.as_view(), name='DeleteContacCrm'),
               url(r'^ListCallCrm/$', ListCallCrm.as_view(), name='ListCallCrm'),
               url(r'^DetailCallCrm/(?P<pk>[0-9]+)/$', DetailCallCrm.as_view(), name='DetailCallCrm'),
               url(r'^CreateCallCrm/$', CreateCallCrm.as_view(), name='CreateCallCrm'),
               url(r'^UpdateCallCrm/(?P<pk>[0-9]+)/$', UpdateCallCrm.as_view(), name='UpdateCallCrm'),
               url(r'^DeleteCallCrm/(?P<pk>[0-9]+)/$', DeleteCallCrm.as_view(), name='DeleteCallCrm'),
               url(r'^CreateTaskCrm/$', CreateTaskCrm.as_view(), name='CreateTaskCrm'),
               url(r'^ReadyTaskCrm/(?P<pk>[0-9]+)/$', ReadyTaskCrm.as_view(), name='ReadyTaskCrm'),
               url(r'^ListTaskCrm/$', ListTaskCrm.as_view(), name='ListTaskCrm'),
               url(r'^UpdateTaskCrm/(?P<pk>[0-9]+)/$', UpdateTaskCrm.as_view(), name='UpdateTaskCrm'),
               url(r'^DeleteTaskCrm/(?P<pk>[0-9]+)/$', DeleteTaskCrm.as_view(), name='DeleteTaskCrm'),
               url(r'^DetailOpportunityCrm/(?P<pk>[0-9]+)/$', DetailOpportunityCrm.as_view(), name='DetailOpportunityCrm'),
               url(r'^CreateOpportunityCrm/$', CreateOpportunityCrm.as_view(), name='CreateOpportunityCrm'),
               url(r'^OpportunityList/$', OpportunityList.as_view(), name='OpportunityList'),
               url(r'^ajax/load_state$', add_state, name='ajax_load_state'),
               url(r'^LeadCrm/$', LeadCrm.as_view(), name='LeadCrm'),
               url(r'^LeadSuccessCrm/$', LeadSuccessCrm.as_view(), name='LeadSuccessCrm'),
               # url(r'^AdminUserCrm/', AdminUserCrm.as_view(), name='AdminUserCrm'),
               # url(r'^AdminProductCrm/$', AdminProductCrm.as_view(), name='AdminProductCrm'),               
               # url(r'^AdminMywebCrm/$', AdminMywebCrm.as_view(), name='AdminMywebCrm'),
               # url(r'^AdminKeywordCrm/$', AdminKeywordCrm.as_view(), name='AdminKeywordCrm'),
               # url(r'Confirm/(?P<id_user>\d+)/', AdminUserConfirmGenerate, name='AdminUserConfirm'),
               # url(r'ConfirmRestablecer/(?P<id_user>\d+)/', AdminUserConfirmRestablecer, name='AdminUserConfirmRestablecer'),
               url(r'^resets/password_reset/', password_reset, {'template_name': 'crm/admin/password_reset_form.html', 'email_template_name':'crm/admin/password_reset_email.html'}, name='password_reset2'),
               url(r'^resets/password_reset_done/', password_reset_done, {'template_name': 'crm/admin/password_reset_done.html'}, name='password_reset_done2'),
               url(r'^resets/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name': 'crm/admin/password_reset_confirm.html'}, name='password_reset_confirm2'),
               url(r'^resets/done/$', password_reset_complete, {'template_name': 'crm/admin/password_reset_complete.html'}, name='password_reset_complete2'),
               url(r'^ListProductCrm/$', ListProductCrm.as_view(), name='ListProductCrm'),
               url(r'^CreateProductCrm/$', CreateProductCrm.as_view(), name='CreateProductCrm'),               
               url(r'^DetailProductCrm/(?P<pk>[0-9]+)/$', DetailProductCrm.as_view(), name='DetailProductCrm'),
               url(r'^UpdateProductCrm/(?P<pk>[0-9]+)/$', UpdateProductCrm.as_view(), name='UpdateProductCrm'),
]