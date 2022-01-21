from django.contrib import admin
from .models import Country
from .models import City
#from .models import Province
from import_export.admin import ImportExportModelAdmin


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    pass


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    pass

""" @admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    pass """

