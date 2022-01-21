from django.db import models
from medcombo.configuration.usercustom.models import User
from cities_light.models import Country
from cities_light.models import City
from medcombo.crm.dashboard_admin.models import LanguageCampaign


def resume_file(instance, filename):
    return 'resume/pdf/{1}'.format(instance, filename)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500)
    places = models.IntegerField(default=0)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    assignment = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    advantages = models.TextField(blank=True)
    type_contract = models.ForeignKey('Contract', on_delete=models.SET_NULL, blank=True, null=True)
    work_day = models.ForeignKey('Workday', on_delete=models.SET_NULL, blank=True, null=True)
    show = models.BooleanField(default=False)
    salary_minimum = models.IntegerField(default=0)
    salary_maximum = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    pending = models.IntegerField(default=0)
    processing = models.IntegerField(default=0)
    selecting = models.IntegerField(default=0)
    discarding = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Contract(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

class Workday(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

class Salary(models.Model):
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.value

class Resume(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    offer = models.ForeignKey('Job', on_delete=models.CASCADE, blank=True, null=True)
    age = models.IntegerField(default=18)
    phone = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    languages = models.TextField(blank=True)
    computer = models.TextField(blank=True)
    another = models.TextField(blank=True)
    condition = models.CharField(max_length=50, default="Pending")
    pdf = models.FileField(upload_to=resume_file, blank=True, null=True)

    def __str__(self):
        return self.participant