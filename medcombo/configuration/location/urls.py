from django.urls import include, path
from .views import load_cities
from django.conf.urls import url

urlpatterns = [
               url(r'^ajax/load-cities$', load_cities, name='ajax_load_cities'), 
              ]