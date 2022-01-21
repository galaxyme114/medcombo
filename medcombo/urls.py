"""medcombo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),    
    url(r'^', include('medcombo.configuration.usercustom.urls')),
    url(r'^', include('medcombo.configuration.usercustom.groups.urls')),
    url(r'^', include('medcombo.configuration.usercustom.permissions.urls')),
    url(r'^', include('medcombo.configuration.authentication.urls')),
    url(r'^', include('medcombo.configuration.location.urls')),
    url(r'^', include('medcombo.configuration.company.urls')),
    url(r'^', include('medcombo.website.home.urls')),
    url(r'^', include('medcombo.myweb.company.urls')),
    url(r'^', include('medcombo.myweb.product.urls')),
    url(r'^', include('medcombo.myweb.catalogue.urls')),
    url(r'^', include('medcombo.myweb.public.urls')),
    url(r'^', include('medcombo.myweb.dashboard_client.urls')),
    url(r'^', include('medcombo.social_network.chat.urls')),
    url(r'^', include('medcombo.social_network.contacts.urls')),
    url(r'^', include('medcombo.crm.dashboard_admin.urls')),
    url(r'^', include('medcombo.crm.admins.urls')),
    url(r'^', include('medcombo.crm.call.urls')),
    url(r'^', include('medcombo.crm.economic.urls')), 
    url(r'^', include('medcombo.crm.contact.urls')),
    url(r'^', include('medcombo.crm.lead.urls')), 
    url(r'^', include('medcombo.crm.opportunity.urls')), 
    url(r'^', include('medcombo.crm.products.urls')), 
    url(r'^', include('medcombo.crm.task.urls')),     
    url(r'^', include('medcombo.product.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^', include('medcombo.myweb.dashboard_client.post.urls')),
    url(r'^', include('medcombo.myweb.job.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns