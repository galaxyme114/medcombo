from django.contrib.sitemaps import Sitemap
from django.urls import reverse, reverse_lazy
from django.utils import translation

from medcombo.product.models import Area, Category, SubCategory

from medcombo.crm.dashboard_admin.models import Event, BannerIndex
from medcombo.configuration.company.models import Company
from medcombo.myweb.job.models import Job

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'
    i18n = False

    def items(self):
        return ['aboutme', 'privacy_policy', 'prices', 'FAQ', 'Contacto', 'list_news', 'list_events']

    def location(self, item):
        return reverse(item)

class Area_Sitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    i18n = False

    def items(self):
        return Area.objects.filter(active=True)

    def location(self, obj):
        return "/categories/" + str(obj.name) + "/"

class Category_Sitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    i18n = False

    def items(self):
        return Category.objects.filter(active=True)

    def location(self, obj):
        return "/subcategories/" + obj.relationship.name + "/" + str(obj.name) + "/"

class SubCategory_Sitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    i18n = False

    def items(self):
        return SubCategory.objects.filter(active=True)

    def location(self, obj):
        return "/keywords/" + obj.relationship.relationship.name + "/" + obj.relationship.name + "/" + str(obj.name) + "/"

class Event_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    i18n = False

    def items(self):
        return Event.objects.filter()

    def location(self, obj):
        return "/detail-event/" + str(obj.id) + "/"

class News_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    i18n = False

    def items(self):
        return BannerIndex.objects.filter(activate=True)

    def location(self, obj):
        return "/detail-news/" + str(obj.id) + "/"

class Company_Sitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    i18n = False

    def items(self):
        return Company.objects.filter(approved=True)

    def location(self, obj):
        return "/my_web_home/" + str(obj.id) + "/"

class Jobopening_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    i18n = False

    def items(self):
        return Job.objects.filter(active=True)

    def location(self, obj):
        return "/detail_front_offers/" + str(obj.id) + "/"