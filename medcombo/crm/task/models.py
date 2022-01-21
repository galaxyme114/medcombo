from django.db import models
from datetime import datetime
from medcombo.crm.opportunity.models import Opportunity
from medcombo.configuration.usercustom.models import User
from django.utils import formats, translation
from medcombo.crm.dashboard_admin.models import LanguageCampaign


class Priority(models.Model):
    name = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.name

class CallTask(models.Model):
    name = models.CharField(max_length=100, blank=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

class Task(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, blank=True, null=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, limit_choices_to={'employee': 1}, blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    priority = models.ForeignKey('Priority', on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True)
    call = models.ForeignKey('CallTask', on_delete=models.SET_NULL, blank=True, null=True)
    language = models.ForeignKey(LanguageCampaign, null=True,blank=True,on_delete=models.SET_NULL)
    done = models.BooleanField(default=True)

    def __str__(self):
        return self.opportunity.title
