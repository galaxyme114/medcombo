from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from medcombo.configuration.usercustom.models import User
from medcombo.crm.contact.forms import LeadForm
from django.contrib.auth.mixins import LoginRequiredMixin

class LeadSuccessCrm(LoginRequiredMixin, TemplateView):
    template_name = "crm/lead/lead_success.html"

class LeadCrm(LoginRequiredMixin, CreateView):
    model = User
    form_class = LeadForm
    template_name = 'crm/lead/create.html'
    success_url = reverse_lazy('LeadSuccessCrm')