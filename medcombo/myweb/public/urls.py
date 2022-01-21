from django.conf.urls import url
from .views import MywebHomeDetail
from .views import MywebContact
from .views import MywebProductList
from .views import MywebCatalogueList
from .views import MywebNewsList, DetailPost
 
urlpatterns = [
                url(r'^my_web_home/(?P<pk>[0-9]+)/$', MywebHomeDetail, name='my_web_home'),          
                url(r'^my_web_product/(?P<pk>[0-9]+)/$', MywebProductList.as_view(), name='MyWebProductList'),
                url(r'^my_web_catalogue/(?P<pk>[0-9]+)/$', MywebCatalogueList.as_view(), name='MyWebCatalogueList'),
                url(r'^my_web_contact/(?P<pk>[0-9]+)/$', MywebContact.as_view(), name='my_web_contact'),
                url(r'^my_web_news/(?P<pk>[0-9]+)/$', MywebNewsList.as_view(), name='MyWebNewsList'),
                url(r'^my_web/post/detail/(?P<idcompany>[0-9]+)/(?P<pk>[0-9]+)$', DetailPost.as_view(), name='detail_post'),
              ]
