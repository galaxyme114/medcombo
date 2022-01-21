from django.db import models
from cities_light.models import Country
from cities_light.models import City
from medcombo.configuration.location.models import InvoicingTitle
#from .validators import invoicing_first_name_validation
from django.core.validators import RegexValidator

def content_file_company(instance, filename):
    return 'company/{1}'.format(instance, filename)

def content_file_company_video(instance, filename):
    return 'company/video/{1}'.format(instance, filename)

def content_file_company_pdf(instance, filename):
    return 'company/pdf/{1}'.format(instance, filename)  

class Company(models.Model):
    name = models.CharField(max_length=500, blank=True)
    cif = models.CharField(max_length=500, blank=True)
    address = models.TextField(blank=True)
    city_company = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    country_company = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    code_postal = models.IntegerField(blank=True, null=True)
    telephone = models.CharField(max_length=250, blank=True, null=True)
    #type_company = models.BooleanField(default=False, blank=True)
    type_company = models.IntegerField(blank=True, null=True)
    another_type_company = models.BooleanField(default=False, blank=True)
    sector = models.ForeignKey('Sector', on_delete=models.SET_NULL, blank=True, null=True)
    web = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to=content_file_company, blank=True)
    policy_accept = models.BooleanField(default=False, blank=True)
    date_policy_accept = models.DateField(null=True, blank=True)
    ip_policy_accept = models.TextField(null=True, blank=True)
    certification_iso = models.FileField(upload_to=content_file_company_pdf,blank=True)
    approved = models.BooleanField(default=False, blank=True)
    invoicing_company_name = models.CharField(max_length=500, blank=True)
    invoicing_address = models.TextField(blank=True)
    invoicing_postal_code =models.IntegerField(blank=True, null=True)
    invoicing_telephone = models.CharField(max_length=250, blank=True, null=True)
    invoicing_fax = models.IntegerField(blank=True, null=True)
    invoicing_title = models.ForeignKey(InvoicingTitle, on_delete=models.SET_NULL, blank=True, null=True)
    invoicing_last_name = models.CharField(max_length=500, blank=True, validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Ingrese un apellido válido')])
    invoicing_first_name = models.CharField(max_length=500, blank=True, validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Ingrese un nombre válido')])
    invoicing_email = models.EmailField(max_length=250,blank=True)
    invoicing_vat_number = models.CharField(max_length=500, blank=True)
    #invoicing_language = models.ForeignKey('LanguageModel', null=True,blank=True,on_delete=True)
    invoicing_city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoicing_city')
    invoicing_country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoicing_country')
    notify = models.BooleanField(default=True, blank=True)
    createdate = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Sector(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name

class BoostingCompany(models.Model):
    company_boosting = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    certification_boosting = models.CharField(max_length=10, null=True, blank=True)
    manufacturer_boosting = models.CharField(max_length=10, null=True, blank=True)
    manufacturer_flag_boosting = models.BooleanField(default=False, blank=True)

class LanguageModel(models.Model):
    name_language = models.CharField(max_length=250)
    value_language = models.CharField(max_length=4)

    def __str__(self):
        return self.name_language

class DescriptionCompany(models.Model):
    title = models.CharField(max_length=1000, blank=True)
    paragraph = models.TextField(blank=True)
    video = models.FileField(upload_to=content_file_company_video, blank=True)
    company = models.ForeignKey('Company', related_name='descriptioncompany_relationship', on_delete=models.CASCADE, blank=True, null=True)
    language = models.ForeignKey('LanguageModel', on_delete=models.SET_NULL, blank=True, null=True) 


