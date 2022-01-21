from django.db import models
from medcombo.configuration.company.models import Company

def content_file_banner_picture(instance, filename):
	return 'banner/{1}'.format(instance, filename)

def content_file_company_log_picture(instance, filename):
    return 'company_logo/{1}'.format(instance, filename)

def content_file_event_picture(instance, filename):
    return 'event/{1}'.format(instance, filename)

def content_file_banner_index_picture(instance, filename):
	return 'banner/index/{1}'.format(instance, filename)

def content_file_banner_user_picture(instance, filename):
	return 'banner/user/{1}'.format(instance, filename)

def content_file_banner_web_picture(instance, filename):
	return 'banner/web/{1}'.format(instance, filename)

def content_file_banner_video(instance, filename):
    	return 'banner/video/{1}'.format(instance, filename)

class LanguageCampaign(models.Model):
    name_language = models.CharField(max_length=250)
    value_language = models.CharField(max_length=15)

    def __str__(self):
        return self.name_language

class Campaign(models.Model):
    start_campaign = models.DateField(null=True, blank=True)
    end_campaign = models.DateField(null=True, blank=True)
    activate_campaign = models.BooleanField()
    position_campaign = models.IntegerField()

    class Meta: 
        permissions = (("read_campaign","Can read campaign"),)

class Banner(models.Model):
    banner_campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=True, null=True)
    language_campaign = models.ForeignKey('LanguageCampaign', on_delete=models.SET_NULL, blank=True, null=True) 
    url_campaign = models.CharField(max_length=250)
    picture_campaign = models.ImageField(upload_to=content_file_banner_picture, blank=True)

    def __str__(self):
        return self.url_campaign

class BannerIndex(models.Model): 
    language = models.ForeignKey('LanguageCampaign', on_delete=models.SET_NULL, blank=True, null=True) 
    url = models.CharField(max_length=500, blank=True)
    picture = models.ImageField(upload_to=content_file_banner_index_picture, blank=True)
    date = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=250, null=True, blank=True)
    order_created = models.IntegerField(default=0)
    description = models.TextField(blank=True,null=True)
    activate = models.BooleanField(default=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    video = models.FileField(upload_to=content_file_banner_video, blank=True)

    def __str__(self):
        return self.title

class CompanyLogo(models.Model): 
    url = models.CharField(max_length=250)
    picture = models.ImageField(upload_to=content_file_company_log_picture, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.url

class BannerUser(models.Model):
    language = models.ForeignKey('LanguageCampaign', on_delete=models.SET_NULL, blank=True, null=True) 
    picture = models.ImageField(upload_to=content_file_banner_user_picture, blank=True)

    def __str__(self):
        return str(self.language)

class Event(models.Model): 
    picture = models.ImageField(upload_to=content_file_event_picture, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    description_es = models.CharField(max_length=500, null=True, blank=True)
    description_en = models.CharField(max_length=500, null=True, blank=True)
    description_pt = models.CharField(max_length=500, null=True, blank=True)
    description_fr = models.CharField(max_length=500, null=True, blank=True)
    description_it = models.CharField(max_length=500, null=True, blank=True)
    description_de = models.CharField(max_length=500, null=True, blank=True)
    description_zh_hant = models.CharField(max_length=500, null=True, blank=True)
    description_zh_hans = models.CharField(max_length=500, null=True, blank=True)
    description_jp = models.CharField(max_length=500, null=True, blank=True)
    start_event = models.DateField(null=True, blank=True)
    end_event = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.title