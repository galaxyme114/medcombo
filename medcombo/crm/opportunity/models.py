from django.db import models
from datetime import datetime
from medcombo.configuration.usercustom.models import User
from medcombo.product.models import Product

class Opportunity(models.Model):
    title = models.CharField(max_length=70, blank=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_client', blank=False, null=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, limit_choices_to={'employee': 1}, related_name='user_responsible', blank=False, null=True)
    probability = models.IntegerField(default=20, blank=False, null=True)
    state = models.ForeignKey('StateOpportunity', on_delete=models.SET_NULL, default=1, blank=True, null=True)
    contacted_by = models.ForeignKey('ContactedBy', on_delete=models.SET_NULL, blank=False, null=True)
    automatic_percent = models.BooleanField(default=True)
    expected_revenue = models.FloatField(default=0.00)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

class StateOpportunity(models.Model):
    name = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.name

class ContactedBy(models.Model):
    name = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.name

class HistoryOpportunity(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    notes = models.TextField(blank=True)

