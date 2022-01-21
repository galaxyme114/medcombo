from django.conf.urls import url
from .views import MywebProductAdminList
from .views import MywebProductCreate
from .views import MywebProductUpdate
from .views import MywebProductAdminDetail
from .views import SearchKeywords
from .views import MywebProductDelete
from .views import SendSuggestion
from .views import ProductDelete 
from .views import Proposalmethod, Unapprove_propo_ajax
from .views import getpdf, accept_proposal
from .views import MywebProductCreateJapones
from .views import MywebProductCreateItaliano
from .views import MywebProductCreatePortugues
from .views import MywebProductCreateAleman
from .views import MywebProductCreateFrances
from .views import MywebProductCreateChinoSimplificado
from .views import MywebProductCreateChinoTradicional
from .views import MywebProductCreateIngles
from .views import MywebProductUpdateIngles
from .views import MywebProductUpdateAleman
from .views import MywebProductUpdateFrances
from .views import MywebProductUpdateItaliano
from .views import MywebProductUpdateJapones
from .views import MywebProductUpdatePortugues, Ajax_administrar_keywords, ajax_category, ajax_subcategory, ajax_search_item
from .views import MywebProductUpdateChinoTradicional, MywebProductAdmininistrar, Ajax_administrar_product, Ajax_administrar_product_listado
from .views import MywebProductUpdateChinoSimplificado, Ajax_update_keywords_product, Ajax_asignar_keyword_product, Ajax_eliminar_keyword_product

urlpatterns = [
                url(r'^myweb/product/list/$', MywebProductAdminList.as_view(), name='MyWebProductAdminList'),
                url(r'^myweb/product/create/$', MywebProductCreate.as_view(), name='MywebProductCreate'),
                url(r'^myweb/product/detail/(?P<pk>[0-9]+)/$', MywebProductAdminDetail.as_view(), name='MywebProductAdminDetail'),                
                url(r'^myweb/product/update/es/(?P<pk>[0-9]+)/$', MywebProductUpdate.as_view(), name='MywebProductUpdate'),                
                url(r'^myweb/product/keywords$', SearchKeywords, name='SearchKeywords'),
                url(r'^myweb/product/delete/(?P<pk>[0-9]+)/$', MywebProductDelete.as_view(), name='MywebProductDelete'),
                url(r'^myweb/product/suggestions$', SendSuggestion, name='SendSuggestion'),
                url(r'^myweb/product/ajax_delete$', ProductDelete, name='ProductDelete'),
                url(r'^myweb/product/create/ja$', MywebProductCreateJapones.as_view(), name='MywebProductCreateJapones'),
                url(r'^myweb/product/create/it$', MywebProductCreateItaliano.as_view(), name='MywebProductCreateItaliano'),
                url(r'^myweb/product/create/hans$', MywebProductCreateChinoSimplificado.as_view(), name='MywebProductCreateChinoSimplificado'),
                url(r'^myweb/product/create/hant$', MywebProductCreateChinoTradicional.as_view(), name='MywebProductCreateChinoTradicional'),
                url(r'^myweb/product/create/pt$', MywebProductCreatePortugues.as_view(), name='MywebProductCreatePortugues'),
                url(r'^myweb/product/create/en$', MywebProductCreateIngles.as_view(), name='MywebProductCreateIngles'),
                url(r'^myweb/product/create/de$', MywebProductCreateAleman.as_view(), name='MywebProductCreateAleman'),
                url(r'^myweb/product/create/fr$', MywebProductCreateFrances.as_view(), name='MywebProductCreateFrances'),
                url(r'^myweb/product/update/en/(?P<pk>[0-9]+)/$', MywebProductUpdateIngles.as_view(), name='MywebProductUpdateIngles'),                
                url(r'^myweb/product/update/de/(?P<pk>[0-9]+)/$', MywebProductUpdateAleman.as_view(), name='MywebProductUpdateAleman'),                
                url(r'^myweb/product/update/fr/(?P<pk>[0-9]+)/$', MywebProductUpdateFrances.as_view(), name='MywebProductUpdateFrances'),                
                url(r'^myweb/product/update/it/(?P<pk>[0-9]+)/$', MywebProductUpdateItaliano.as_view(), name='MywebProductUpdateItaliano'),                
                url(r'^myweb/product/update/pt/(?P<pk>[0-9]+)/$', MywebProductUpdatePortugues.as_view(), name='MywebProductUpdatePortugues'),                
                url(r'^myweb/product/update/hans/(?P<pk>[0-9]+)/$', MywebProductUpdateChinoSimplificado.as_view(), name='MywebProductUpdateChinoSimplificado'),                
                url(r'^myweb/product/update/hant/(?P<pk>[0-9]+)/$', MywebProductUpdateChinoTradicional.as_view(), name='MywebProductUpdateChinoTradicional'),                
                url(r'^myweb/product/update/ja/(?P<pk>[0-9]+)/$', MywebProductUpdateJapones.as_view(), name='MywebProductUpdateJapones'),                
                url(r'^myweb/product/ajax_update_keywords_product$', Ajax_update_keywords_product, name='AjaxUpdateKeywordsProductMyweb'),
                url(r'^myweb/product/ajax_asignar_keyword_product$', Ajax_asignar_keyword_product, name='ajax_asignar_keyword_product'),
                url(r'^myweb/product/ajax_eliminar_keyword_product$', Ajax_eliminar_keyword_product, name='ajax_eliminar_keyword_product'),
                url(r'^myweb/product/Admin/$', MywebProductAdmininistrar, name='MywebProductAdmininistrar'),
                url(r'^myweb/product/ajax_productoadministrar$', Ajax_administrar_product, name='ajax_productoadministrar'),
                url(r'^myweb/product/ajax_productoadministrar/listado$', Ajax_administrar_product_listado, name='ajax_productoadministrar_listado'),
                url(r'^proposal/(?P<pk>[0-9]+)/$', Proposalmethod.as_view(), name='proposalmethod'),
                url(r'^pdf/(?P<value>\w+)/$', getpdf, name='pdfdownload'),
                url(r'^unapprove_propo_ajax/$', Unapprove_propo_ajax, name='unapprove_propo_ajax'),
                url(r'^accept_proposal$', accept_proposal, name='accept_proposal'),
                url(r'^myweb/product/ajax_keywordsadministrar$', Ajax_administrar_keywords, name='keywords_administrar'),
                url(r'^ajax_category$', ajax_category, name='ajax_category'),
                url(r'^ajax_subcategory$', ajax_subcategory, name='ajax_subcategory'),
                url(r'^ajax-search-item$', ajax_search_item, name='ajax_search_item'),

              ]   