from django.db import models

class Country(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=150, blank=True)
    cc_fips = models.CharField(primary_key=True, unique=False, max_length=2)
    cc_iso = models.CharField(max_length=2, blank=True)
    tld = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.name

class City(models.Model):
    relationship = models.ForeignKey('Country', on_delete=models.DO_NOTHING, blank=True)
    name = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.name

class InvoicingTitle(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

""" class Province(models.Model):
    relationship = models.ForeignKey('Country', on_delete=models.DO_NOTHING, blank=True)
    name = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.name """