from cities_light.models import Country
from cities_light.models import City
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company
from django.shortcuts import render

class CityAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        country = self.forwarded.get('country_company', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class CityAutocompleteJob(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class CityAutocompleteFacturation(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        country = self.forwarded.get('invoicing_country', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
def NewSearchCompany(request):
    keyword = request.GET.get("id_name", "")
    searched_company= Company.objects.filter(name__icontains=keyword, approved= True).order_by('name')
    
    return render(request, 'website/home/company_list.html', { 'searched_company': searched_company, 'totalcompanys':searched_company.count(),'namekeyword': keyword, 'searchkey':keyword, 'company_search':'YES'})
