from django.conf.urls import url
from .views import DashboardClient



urlpatterns = [
               url(r'^dashboard_client/$', DashboardClient.as_view(), name='dashboard_client'),  
              ]  