from django.conf.urls import url
from .views import Home, About, CategoriesArea, KeywordSubCategoryNew, SubcategoriesCategoryNew, PrivacyPolicy, FAQ, Contacto, ListNews, DetailNews
from .views import ListEvents, DetailEvent
from .views import Prices
from .views import ContactoPrice
from .views import Sitemap

from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from .sitemaps import Static_Sitemap
from .sitemaps import Area_Sitemap
from .sitemaps import Category_Sitemap
from .sitemaps import SubCategory_Sitemap
from .sitemaps import Event_Sitemap
from .sitemaps import News_Sitemap
from .sitemaps import Company_Sitemap
from .sitemaps import Jobopening_Sitemap

sitemaps = {
    'static': Static_Sitemap(),
    'area': Area_Sitemap(),
    'category': Category_Sitemap(),
    'subcategory': SubCategory_Sitemap(),
    'events': Event_Sitemap(),
    'news': News_Sitemap(),
    'company': Company_Sitemap(),
    'job': Jobopening_Sitemap(),
}

urlpatterns = [
                url(r'^$', Home.as_view(), name='home'),
                url(r'^about-us/$', About.as_view(), name='aboutme'),
                url(r'^privacy/$', PrivacyPolicy.as_view(), name='privacy_policy'),
                url(r'^prices/$', Prices.as_view(), name='prices'),
                url(r'^FAQ/$', FAQ.as_view(), name='FAQ'),
                url(r'^Contact/$', Contacto.as_view(), name='Contacto'),
                url(r'^news/$', ListNews.as_view(), name='list_news'),
                url(r'^detail-news/(?P<pk>[0-9]+)/$', DetailNews.as_view(), name='detail_news'),
                url(r'^categories/(?P<my_category_area>.+)$', CategoriesArea, name='CategoriesArea'),
                url(r'^keywords/(?P<my_area_keyword>.+)/(?P<my_category_keyword>.+)/(?P<my_subcategory_keyword>.+)$', KeywordSubCategoryNew, name='KeywordsSubCategoryNew'),
                url(r'^subcategories/(?P<my_area_subcategory>.+)/(?P<my_category_subcategory>.+)$', SubcategoriesCategoryNew, name='SubcategoriesCategoryNew'),
                
                url(r'^events/$', ListEvents.as_view(), name='list_events'),
                url(r'^detail-event/(?P<pk>[0-9]+)/$', DetailEvent.as_view(), name='detail_event'),
                url(r'^Contact-Price/(?P<pk>[0-9]+)/$', ContactoPrice.as_view(), name='ContactoPrice'),

                url(r'^sitemap/$', Sitemap.as_view(), name='sitemap'),
                url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
            ]
              