from django.db import models
from django.db import models
from datetime import datetime
from django.utils import formats, translation
from medcombo.configuration.usercustom.models import User
from medcombo.crm.opportunity.models import Opportunity
from medcombo.product.models import Product
from django.utils import formats, translation

# Create your models here.

class Proposal_Commercial(models.Model):
    title = models.CharField(max_length=100, blank=True)
    commercial = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.CharField(max_length=100, blank=True)
    edit_date = models.DateField(null=True, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    validata = models.CharField(max_length=100, blank=True)
    flag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

class Proposal_Product(models.Model):
    commercial_prod = models.ForeignKey(Proposal_Commercial, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True)
    discount = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.commercial_prod

class Proposal_Opportunity(models.Model):
    commercial_oppor = models.ForeignKey(Proposal_Commercial, on_delete=models.CASCADE, blank=True, null=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.commercial_oppor