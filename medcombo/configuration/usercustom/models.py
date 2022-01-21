from django.db import models
from django.contrib.auth.models import AbstractUser 
from medcombo.configuration.company.models import Company
from cities_light.models import Country
from cities_light.models import City
from medcombo.crm.dashboard_admin.models import LanguageCampaign


def content_file_user(instance, filename):
    return 'usercustom/{1}'.format(instance, filename)

class User(AbstractUser):
    picture = models.ImageField(upload_to=content_file_user, blank=True)
    telephone = models.CharField(max_length=250, blank=True, null=True)
    work = models.ForeignKey('Work', on_delete=models.SET_NULL, blank=True, null=True)    
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)    
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    lead = models.BooleanField(default=False) 
    company = models.ForeignKey(Company, related_name='user_relationship',on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    policy = models.BooleanField(default=True)
    movil = models.CharField(max_length=30, blank=True, null=True)
    wechat = models.CharField(max_length=100, blank=True, null=True)
    tracing = models.ManyToManyField('User',related_name="tracing_users", blank=True)
    indicated = models.BooleanField(default=True)
    extra_surename = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    com_approve_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username

    class Meta:
        permissions = (("marketing_user","Can use modules marketing"),("sales_user","Can use modules sales"),("system_user","Can use modules system"),("management_user","Can use modules management"),("optional_user","Can use modules optional"),("optional2_user","Can use modules optional2"),("optional3_user","Can use modules optional3"),("optional4_user","Can use modules optional4"))

class GetIP(models.Model):
    user_ip = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ipaddress = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ipaddress

class Work(models.Model):
    name = models.CharField(max_length=150)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

class UserScore(models.Model):
    user_score = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    value_score = models.CharField(max_length=10, null=True, blank=True)

class UserOnline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Userrunning_system(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(auto_now_add=True, blank=True)
