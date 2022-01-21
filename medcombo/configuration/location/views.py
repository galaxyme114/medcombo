from django.shortcuts import render
from .models import City
from django.contrib.auth.decorators import login_required

@login_required
def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(relationship=country_id).order_by('name')
    return render(request, 'location/city_dropdown_list_options.html', {'cities': cities})
