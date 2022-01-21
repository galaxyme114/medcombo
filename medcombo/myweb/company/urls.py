from django.conf.urls import url
from .views import MywebCompanyDetail, MywebConfirmForm, MywebCompanyDetailFacturacion
from .views import MywebCompanyCreate
from .views import MywebCompanyUpdate, MywebCompanyUpdateFacturacion, MywebCompanyCreateDescription, MywebCompanyUpdateDescription
from .views import DeleteLogoCompany, MywebCompanyCopyUpdateFacturacion

urlpatterns = [
                url(r'^myweb/company/detail/(?P<pk>[0-9]+)/$', MywebCompanyDetail.as_view(), name='detail_company'),
                url(r'^myweb/company/create/$', MywebCompanyCreate.as_view(), name='create_company'),
                url(r'^myweb/company/update/(?P<pk>[0-9]+)/$', MywebCompanyUpdate.as_view(), name='update_company'),
                url(r'^myweb/company/confirm/$', MywebConfirmForm.as_view(), name='confirm_form'),
                url(r'^myweb/company/facturacion/(?P<pk>[0-9]+)/$', MywebCompanyDetailFacturacion.as_view(), name='detail_company_facturacion'),
                url(r'^myweb/company/change/facturacion/(?P<pk>[0-9]+)/$', MywebCompanyUpdateFacturacion.as_view(), name='update_company_facturacion'),
                url(r'^myweb/company/create/description/(?P<pk>[0-9]+)/$', MywebCompanyCreateDescription.as_view(), name='CreateDescriptionCompany'),
                url(r'^myweb/company/update/description/(?P<pk>[0-9]+)/$', MywebCompanyUpdateDescription.as_view(), name='UpdateDescriptionCompany'),
                url(r'^delete_logo_company/$', DeleteLogoCompany, name='delete_logo_company'),
                url(r'^myweb/company/changecopy/facturacion/(?P<pk>[0-9]+)/$', MywebCompanyCopyUpdateFacturacion, name='update_copy_company_facturacion'),

              ]