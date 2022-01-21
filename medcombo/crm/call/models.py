from django.db import models
from datetime import datetime
from medcombo.configuration.usercustom.models import User

class Call(models.Model):
    client =  models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'lead': 1}, related_name='user_client_call', blank=False, null=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, limit_choices_to={'employee': 1}, blank=False, null=True)
    telephone = models.CharField(max_length=16, blank=False)
    date = models.DateField(null=True, blank=True)
    hour = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.client

class HistoryCall(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='call_client', blank=False, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    result = models.CharField(max_length=100, blank=False)
    notes = models.TextField(blank=True)