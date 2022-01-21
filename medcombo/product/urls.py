from django.conf.urls import url
from .views import ListProduct
from .views import SearchProduct
from .views import searcharea
from .views import searchcategory
from .views import searchsubcategory
from .views import DetailProduct, DetailProductFavorite
from .views import CreateCategories
from .views import ListCategories
from .views import CategoryAutocomplete
from .views import SubCategoryAutocomplete
from .views import ProductsSearchData
from .views import NewSearchProduct, MywebDetailProduct, MywebProductDetailMenu, MywebPostDetailMenu
from .views import ProductCountry
from .views import ListFavorites
from .views import BannerWebCreate
from .views import BannerWebUpdate
from .views import DeleteNewbanner
from .views import ProductCountryTwo, ProductCompare

urlpatterns = [
               url(r'^product/list$', ListProduct.as_view(), name='product'),
               url(r'^product/search$', SearchProduct, name='SearchProduct'),
               url(r'^(?P<lang>[^/]+)/(?P<country>[^/]+)/(?P<product>[^/]+)/(?P<area>[^/]+)/(?P<category>[^/]+)/(?P<subcategory>[^/]+)/(?P<keyword>[^/]+)/$', NewSearchProduct, name='NewSearchProduct'),
               url(r'^product/searcharea/(?P<pk>[0-9]+)/$', searcharea, name='searcharea'),
               url(r'^product/searchcategory/(?P<pk>[0-9]+)/$', searchcategory, name='searchcategory'),               
               url(r'^product/searchsubcategory/(?P<pk>[0-9]+)/$', searchsubcategory, name='searchsubcategory'),
               url(r'^product/detail/(?P<pk>[0-9]+)/$', DetailProduct.as_view(), name='detail_product'),
               url(r'^product/category/create$', CreateCategories.as_view(), name='CreateCategories'),
               url(r'^product/category/list/$', ListCategories.as_view(), name='ListCategories'),
               url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(create_field='name'), name='category-autocomplete'),
               url(r'^subcategory-autocomplete/$', SubCategoryAutocomplete.as_view(create_field='name'), name='subcategory-autocomplete'),
               url(r'^products-autocomplete/$', ProductsSearchData.as_view(), name='products-autocomplete'),
               url(r'^my_web/product/detail/(?P<pk>[0-9]+)/$', MywebDetailProduct.as_view(), name='myweb_detail_product'),
               url(r'^my_web_product_detailmenu/(?P<idcompany>[0-9]+)/(?P<pk>[0-9]+)$', MywebProductDetailMenu.as_view(), name='my_web_product_menu'), 
               url(r'^my_web_post_menu/(?P<idcompany>[0-9]+)/(?P<pk>[0-9]+)$', MywebPostDetailMenu.as_view(), name='my_web_post_menu'),
               url(r'^product/country$', ProductCountry, name='product_country'),
               url(r'^product/country/searchengine$', ProductCountryTwo, name='product_country_searchengine'),
               url(r'^favorites/$', ListFavorites.as_view(), name='list_favorites'),
               url(r'^BannerCompany/$', BannerWebCreate.as_view(), name='BannerCompany'),
               url(r'^BannerWebUpdate/(?P<pk>\d+)/$', BannerWebUpdate.as_view(), name='BannerWebUpdate'),
               url(r'^product/detail/favorite/(?P<pk>[0-9]+)/$', DetailProductFavorite.as_view(), name='detail_product_favorite'),
               url(r'^Delete_newbanner/$', DeleteNewbanner, name='delete_newbanner'),
               url(r'^ProductCompare/$', ProductCompare, name='ProductCompare'),

]