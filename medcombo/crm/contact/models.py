from django.db import models
from medcombo.configuration.company.models import Company
from datetime import datetime

class PolityToken(models.Model):
    company =  models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_client', blank=False, null=True)
    token = models.CharField(max_length=60, blank=False)
    state = models.BooleanField(default=0, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.token
