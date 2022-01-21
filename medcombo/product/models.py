from django.db import models
from datetime import datetime
from medcombo.configuration.usercustom.models import User
from medcombo.configuration.location.models import Country
from medcombo.configuration.location.models import City
from medcombo.configuration.company.models import Company
from medcombo.crm.dashboard_admin.models import LanguageCampaign
from datetime import datetime

def content_file_products_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'product/{1}'.format(instance, file_save_name)

def content_file_areas_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'area/{1}'.format(instance, file_save_name)

def content_file_areas_icono_picture(instance, filename):
    return 'area/icono/{1}'.format(instance, filename)

def content_file_categories_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'category/{1}'.format(instance, file_save_name)

def content_file_subcategories_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'subcategory/{1}'.format(instance, file_save_name)

def content_file_product_video(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'product/video/{1}'.format(instance, file_save_name)

def content_file_keywords_picture(instance, filename):
    file_save_name = instance.name +"."+ filename.split('.')[-1]
    return 'keyword/{1}'.format(instance, file_save_name)

def content_file_banner_web_picture(instance, filename):
    return 'banner/web/{1}'.format(instance, filename)

def content_file_banner_web_picture_search(instance, filename):
    return 'banner/websearch/{1}'.format(instance, filename)

def csv_file(instance, filename):
    return 'csv/file/{1}'.format(instance, filename)

class Product(models.Model):
    product_ID = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=100, default='0', decimal_places=2, blank=True)
    name = models.CharField(max_length=150)
    picture = models.ImageField(upload_to=content_file_products_picture, blank=True)
    picture2 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    picture3 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    picture4 = models.ImageField(upload_to=content_file_products_picture, blank=True)
    description = models.TextField( blank=True)
    notes = models.TextField(max_length=400, blank=True)
    company = models.ForeignKey(Company, related_name='product_relationship',on_delete=models.CASCADE, blank=True, null=True)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, blank=True, null=True)
    video = models.FileField(upload_to=content_file_product_video, blank=True)
    algorithmic_value = models.IntegerField(default=1000)
    rating_average = models.DecimalField(max_digits=100, default=0, decimal_places=1, blank=True)
    approved = models.BooleanField(default=False, blank=True)
    keyword = models.ManyToManyField('Keyword',related_name="keywords", blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    notify = models.BooleanField(default=True, blank=True)
    order = models.DecimalField(max_digits=100, default='0', decimal_places=2, blank=True)
    compare = models.BooleanField(default=False, blank=True)
    request_date  = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name 

    class Meta:
        permissions = (("read_product","Can read product"),("boosting_product","Can use boosting"),)

class Area(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to=content_file_areas_picture, blank=True)
    description = models.TextField(max_length=400, blank=True)
    active = models.BooleanField(default=True, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    has_keyword = models.BooleanField(default=True, blank=True)
    posicion = models.IntegerField(null=True, blank=True, default=10000)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    h_tag = models.CharField(max_length=500, null=True, blank=True)
 
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['posicion', '-date', 'id']

class Category(models.Model):
    relationship = models.ForeignKey('Area', related_name='category', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to=content_file_categories_picture, blank=True)
    description = models.TextField(max_length=400, blank=True)
    active = models.BooleanField(default=True, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    posicion = models.IntegerField(null=True, blank=True, default=10000)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    h_tag = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['posicion', '-date', 'id']

class SubCategory(models.Model):
    relationship = models.ForeignKey('Category', related_name='subcategory', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to=content_file_subcategories_picture, blank=True)
    description = models.TextField(max_length=400, blank=True)
    active = models.BooleanField(default=True, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    posicion = models.IntegerField(null=True, blank=True, default=10000)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)
    h_tag = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['posicion', '-date', 'id']

class RatingProduct(models.Model):
    user_rating = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product_rating = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    value_rating = models.IntegerField(null=True, blank=True, default=0)

class BoostingProduct(models.Model):
    product_boosting = models.ForeignKey('Product',on_delete=models.CASCADE, blank=True, null=True)
    rating_boosting = models.CharField(max_length=10, null=True, blank=True)
    keyword_boosting = models.CharField(max_length=10, null=True, blank=True)
    iso_boosting = models.CharField(max_length=10, null=True, blank=True)
    manufacturer_boosting = models.CharField(max_length=10, null=True, blank=True)

class Keyword(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    area = models.ForeignKey('Area', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, blank=True, null=True, )
    description = models.TextField(max_length=400, blank=True)
    image = models.ImageField(upload_to=content_file_keywords_picture, blank=True)
    posicion = models.IntegerField(null=True, blank=True, default=10000)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['posicion', 'id']

class SuggestionKeyword(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    notify = models.BooleanField(default=True, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)


class BoostingKeyword(models.Model):
    company = models.ForeignKey(Company,null=True,blank=True,on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword,null=True,blank=True,on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    flag = models.IntegerField(default=0)

class Sponsor(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, unique=True)
    active = models.BooleanField(default=True)
    lateral = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company.name)

class FavoriteProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class AdminProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE, blank=True, null=True)

class CsvArchivo(models.Model):
    name = models.CharField(max_length=155, null=True, blank=True)
    file = models.FileField(upload_to=csv_file, blank=True, null=True) 

class PolicyPrivacyModel(models.Model):
    description = models.TextField(blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)

class Searchkey_static(models.Model):
    searchkey_name = models.CharField(max_length=155, null=True, blank=True)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, blank=True, null=True, )
    search_date = models.DateField(null=True, auto_now_add=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True,blank=True,on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=155, null=True, blank=True)

class Click_static(models.Model):
    product_name = models.CharField(max_length=155, null=True, blank=True)
    click_date = models.DateField(null=True, auto_now_add=True) 

class BannerWeb(models.Model):
    banner_company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    language_campaign = models.ForeignKey(LanguageCampaign, on_delete=models.SET_NULL, blank=True, null=True) 
    url_campaign = models.CharField(max_length=250, blank=True, null=True)
    picture_campaign = models.ImageField(upload_to=content_file_banner_web_picture, blank=True, null=True)
    picture_campaign_search = models.ImageField(upload_to=content_file_banner_web_picture_search, blank=True, null=True)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, blank=True, null=True)
    keyword = models.ManyToManyField('Keyword',related_name="key", blank=True)
    start_banner = models.DateField(null=True, blank=True)
    end_banner = models.DateField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.banner_company)

class SynonymKeyword(models.Model):
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500, null=True, blank=True)
