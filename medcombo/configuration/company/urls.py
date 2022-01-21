from django.conf.urls import url
from .views import CityAutocomplete, CityAutocompleteFacturation, CityAutocompleteJob, NewSearchCompany

urlpatterns = [
               url(r'^city-autocomplete/$', CityAutocomplete.as_view(create_field='name'), name='city-autocomplete'),
               url(r'^city-autocomplete-job/$', CityAutocompleteJob.as_view(create_field='name'), name='city-autocomplete-job'),
               url(r'^city-autocomplete-facturation/$', CityAutocompleteFacturation.as_view(create_field='name'), name='city-autocomplete-facturation'),               
               url(r'^search-company', NewSearchCompany, name='NewSearchCompany'),
]