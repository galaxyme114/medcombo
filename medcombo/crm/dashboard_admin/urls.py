from django.conf.urls import url
from .views import DashboardAdmin
from .views import BannerList
from .views import BannerCreate
from .views import BannerUpdate
from .views import Boosting
from .views import BannerPicture
from .views import Stats
from .views import SearchBoosting
from .views import SendBoosting
from .views import autocompleteModelBoosting
from .views import ListCategories
from .views import SponsorList
from .views import SponsorCreate
from .views import SponsorCompany
from .views import SponsorTable
from .views import SponsorSearchTable
from .views import SponsorAjaxIcon
from .views import SponsorUpdate
from .views import BannerIndexList
from .views import BannerIndexUpdate
from .views import BannerIndexCreate
from .views import ActiveBannerIndex
#from .views import BannerCompany
from .views import ImportCSV
from .views import DeleteCampaign
from .views import Sponsor_delete
from .views import DeleteMedMagazine

from .views import CompanyLogoList
from .views import CompanyLogoCreate
from .views import CompanyLogoUpdate
from .views import CompanyLogoDelete

from .views import EventList
from .views import EventCreate
from .views import EventUpdate
from .views import EventDelete
urlpatterns = [
               url(r'^dashboard_admin/$', DashboardAdmin.as_view(), name='dashboard_admin'),
               url(r'^es/products/(?P<area>[^/]+)/(?P<category>[^/]+)/(?P<subcategory>[^/]+)/(?P<keyword>[^/]+)/$', SearchBoosting, name='SearchBoosting'),
               url(r'^Boosting/list_categories$', ListCategories, name='list_categories'),
               url(r'^Boosting/send$', SendBoosting, name='SendBoosting'),
               url(r'^BannerList/$', BannerList.as_view(), name='BannerList'), 
               url(r'^BannerCreate/$', BannerCreate.as_view(), name='BannerCreate'),
               url(r'^BannerUpdate/(?P<pk>\d+)/$', BannerUpdate.as_view(), name='BannerUpdate'),
               url(r'^BannerPicture/(?P<pk>\d+)/$', BannerPicture.as_view(), name='BannerPicture'),
               url(r'^Boosting/$', Boosting.as_view(), name='Boosting'),
               url(r'^Sponsor_List/$', SponsorList.as_view(), name='Sponsor_List'),
               url(r'^Sponsor_Create/$', SponsorCreate.as_view(), name='Sponsor_Create'),
               url(r'^Stats/$', Stats.as_view(), name='Stats'),    
               url(r'^ajax_calls/search/', autocompleteModelBoosting),
               url(r'^ajax_sponsor_company/$', SponsorCompany, name='ajax_sponsor_company'),
               url(r'^sponsor_company_product/$', SponsorTable, name='sponsor_company_product'),
               url(r'^sponsor_search_product/$', SponsorSearchTable, name='sponsor_search_product'),
               url(r'^sponsor_ajax_icon/$', SponsorAjaxIcon, name='sponsor_ajax_icon'),
               url(r'^Sponsor_Update/(?P<pk>\d+)/$', SponsorUpdate.as_view(), name='Sponsor_Update'),
               url(r'^BannerIndexList/(?P<lang>[^/]+)/$', BannerIndexList.as_view(), name='BannerIndexList'),
               url(r'^BannerIndexUpdate/(?P<pk>\d+)/$', BannerIndexUpdate.as_view(), name='BannerIndexUpdate'),
               url(r'^BannerIndexCreate/$', BannerIndexCreate.as_view(), name='BannerIndexCreate'), 
               url(r'^ActiveBannerIndex/$', ActiveBannerIndex, name='ActiveBannerIndex'), 
               #url(r'^BannerCompany/$', BannerCompany.as_view(), name='BannerCompany'),
               url(r'^Import_CSV/$', ImportCSV.as_view(), name='Import_CSV'),
               url(r'^delete_campaign/$', DeleteCampaign, name='delete_campaign'),
               url(r'^Deletesponsor/$', Sponsor_delete, name='delete_sponsor'),
               url(r'^Delete_MedMagazine/$', DeleteMedMagazine, name='delete_MedMagazine'),

               url(r'^CompanyLogoList/$', CompanyLogoList.as_view(), name='CompanyLogoList'), 
               url(r'^CompanyLogoCreate/$', CompanyLogoCreate.as_view(), name='CompanyLogoCreate'),
               url(r'^CompanyLogoUpdate/(?P<pk>\d+)/$', CompanyLogoUpdate.as_view(), name='CompanyLogoUpdate'),
               url(r'^CompanyLogoDelete/$', CompanyLogoDelete, name='delete_companylogo'),
               
               url(r'^EventList/$', EventList.as_view(), name='EventList'), 
               url(r'^EventCreate/$', EventCreate.as_view(), name='EventCreate'),
               url(r'^EventUpdate/(?P<pk>\d+)/$', EventUpdate.as_view(), name='EventUpdate'),
               url(r'^EventDelete/$', EventDelete, name='delete_event'),
              ]