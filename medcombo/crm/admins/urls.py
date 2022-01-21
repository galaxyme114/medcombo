from django.conf.urls import url
from .views import AdminUserCrm
from .views import AdminProductCrm
from .views import AdminMywebCrm
from .views import AdminKeywordCrm
from .views import CategoriesCrmDelete
from .views import KeywordsCrmDelete
from .views import AdminUserConfirmGenerate
from .views import AdminUserConfirmRestablecer
from .views import KeywordDelete
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from .views import load_products_admin, load_keywords, keywords_ajax, subcategories_ajax, categories_ajax, approve_product_ajax
from .views import ApproveMyWebCrm, add_synonym, delete_synonym, Order_categories_admin, Order_subcategories_admin, Order_areas_admin
from .views import AdminCategoryCrm, PrivacyPolicyCrm, CreatePrivacyPolicyCrm, UpdatePrivacyPolicyCrm, Order_keywords_admin
from .views import ListAdminCategoryKeywordCrm, UpdateAdminCategoryKeywordCrm,dismiss_product_ajax, SeeProductCrm
from .views import load_myweb_admin, category_keywords_ajax, area_keywords_ajax, delete_myweb_admin, Crear_Keyword_Ajax, DeleteKeywordCrm, UpdateKeywordCrm, DeleteCategoryCrm, DeleteSubCategoryCrm, DeleteAreaCrm
from .views import loadKeys, Get_keywords

urlpatterns = [
               url(r'^AdminUserCrm/$', AdminUserCrm.as_view(), name='AdminUserCrm'),
               url(r'^AdminProductCrm/$', AdminProductCrm, name='AdminProductCrm'),               
               url(r'^AdminMywebCrm/$', AdminMywebCrm, name='AdminMywebCrm'),
               url(r'^AdminKeywordCrm/$', AdminKeywordCrm.as_view(), name='AdminKeywordCrm'),
               url(r'Confirm/(?P<id_user>\d+)/', AdminUserConfirmGenerate, name='AdminUserConfirm'),
               url(r'ConfirmRestablecer/(?P<id_user>\d+)/', AdminUserConfirmRestablecer, name='AdminUserConfirmRestablecer'),
               url(r'^resets/password_reset/(?P<id_user>\d+)/$', PasswordResetView.as_view(template_name='configuration/usercustom/password_reset_form.html', email_template_name='configuration/usercustom/password_reset_email.html'), name='password_reset2'),
               url(r'^resets/password_reset_done/', PasswordResetDoneView, {'template_name': 'crm/admin/password_reset_done.html'}, name='password_reset_done2'),
               url(r'^resets/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView, {'template_name': 'crm/admin/password_reset_confirm.html'}, name='password_reset_confirm2'),
               url(r'^resets/done/$', PasswordResetCompleteView, {'template_name': 'crm/admin/password_reset_complete.html'}, name='password_reset_complete2'),
               url(r'^ajax/load/products/admin', load_products_admin, name='ajax_load_products_admin'),
               url(r'^ajax/load/keyword/(?P<pk>[0-9]+)/(?P<lang>[0-9]+)$', load_keywords.as_view(), name='ajax_load_keyword'),
               url(r'^ajax/load/myweb/admin', load_myweb_admin, name='ajax_load_myweb_admin'), 
               url(r'^ajax/delete/myweb/admin', delete_myweb_admin, name='ajax_delete_myweb_admin'),
               url(r'^ApproveMyWebCrm/(?P<pk>[0-9]+)/$', ApproveMyWebCrm.as_view(), name='ApproveMyWebCrm'),
               url(r'^SeeProductCrm/(?P<pk>[0-9]+)/$', SeeProductCrm.as_view(), name='SeeProductCrm'),
               url(r'^AdminCategoryCrm/$', AdminCategoryCrm.as_view(), name='AdminCategoryCrm'),
               url(r'^AdminCategoryKeywordCrm/(?P<language>[0-9]+)/$', ListAdminCategoryKeywordCrm, name='AdminCategoryKeywordCrm'),
               url(r'^UpdateAdminCategoryKeywordCrm/(?P<area>[0-9]+)/(?P<category>[0-9]+)/(?P<subcategory>[0-9]+)/$', UpdateAdminCategoryKeywordCrm, name='UpdateAdminCategoryKeywordCrm'),
               url(r'^keywords/ajax', keywords_ajax, name='keywords_ajax'),
               url(r'^ajax/order/keywords/admin', Order_keywords_admin, name='ajax_order_keywords_admin'),
               url(r'^area/keywords/ajax', area_keywords_ajax, name='area_keywords_ajax'),
               url(r'^category/keywords/ajax', category_keywords_ajax, name='category_keywords_ajax'),
               url(r'^subcategories/ajax', subcategories_ajax, name='subcategory_ajax'),
               url(r'^categories/ajax', categories_ajax, name='category_ajax'),
               url(r'^gestion/keywords/ajax', Crear_Keyword_Ajax, name='crear_keyword_ajax'),
               url(r'^Delete/keywordCrm/(?P<pk>[0-9]+)/$', DeleteKeywordCrm.as_view(), name='DeleteKeywordCrm'),
               url(r'^Update/keywordCrm/(?P<pk>[0-9]+)/$', UpdateKeywordCrm.as_view(), name='UpdateKeywordCrm'),
               url(r'^Delete/categoryCrm/(?P<pk>[0-9]+)/$', DeleteCategoryCrm.as_view(), name='DeleteCategoryCrm'),
               url(r'^Delete/subcategoryCrm/(?P<pk>[0-9]+)/$', DeleteSubCategoryCrm.as_view(), name='DeleteSubCategoryCrm'),
               url(r'^Delete/areaCrm/(?P<pk>[0-9]+)/$', DeleteAreaCrm.as_view(), name='DeleteAreaCrm'),
               url(r'^KeywordDelete/$', KeywordDelete, name='KeywordDelete'),
               url(r'^PrivacyPolicyCrm/$', PrivacyPolicyCrm.as_view(), name='PrivacyPolicyCrm'),
               url(r'^CreatePrivacyPolicyCrm/$', CreatePrivacyPolicyCrm.as_view(), name='CreatePrivacyPolicyCrm'),
               url(r'^UpdatePrivacyPolicyCrm/(?P<pk>[0-9]+)/$', UpdatePrivacyPolicyCrm.as_view(), name='UpdatePrivacyPolicyCrm'),
               url(r'^DeleteCategoriesCrm', CategoriesCrmDelete, name='DeleteCategoriesCrm'),
               url(r'^DeleteKeywordsCrm', KeywordsCrmDelete, name='DeleteKeywordsCrm'),
               url(r'^ajax/order/categories/admin', Order_categories_admin, name='ajax_order_categories_admin'),
               url(r'^ajax/order/subcategories/admin', Order_subcategories_admin, name='ajax_order_subcategories_admin'),
               url(r'^ajax/order/areas/admin', Order_areas_admin, name='ajax_order_areas_admin'),
               url(r'^approve/product/ajax', approve_product_ajax, name='approve_product_ajax'),
               url(r'^dismiss/product/ajax', dismiss_product_ajax, name='dismiss_product_ajax'),
               url(r'^ajax/add/synonym', add_synonym, name='ajax_add_synonym'),
               url(r'^ajax/delete/synonym', delete_synonym, name='ajax_delete_synonym'),
               url(r'^ajax/loadingkeys', loadKeys, name='loadingkeys'),
               url(r'^ajax/load/key', Get_keywords, name='ajax_load_key'),

               
]