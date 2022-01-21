
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
from .models import Call, HistoryCall
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateCallCrm(LoginRequiredMixin, CreateView):
    model = Call
    fields = '__all__'
    template_name = "crm/call/create.html"
    success_url = reverse_lazy('ListCallCrm') 

class ListCallCrm(LoginRequiredMixin, ListView):
    model = Call
    ordering = ['id']
    template_name = "crm/call/list.html"

class DetailCallCrm(LoginRequiredMixin, CreateView):
    model = HistoryCall
    fields = '__all__'
    template_name = "crm/call/detail.html"
    success_url = reverse_lazy('ListCallCrm')    

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['calls'] = Call.objects.get(pk=self.kwargs.get('pk'))
        return context

class UpdateCallCrm(LoginRequiredMixin, UpdateView):
    model = Call
    fields = '__all__'
    template_name = "crm/call/create.html"
    success_url = reverse_lazy('ListCallCrm')

class DeleteCallCrm(LoginRequiredMixin, DeleteView):
	model = Call
	template_name = "crm/call/delete.html"
	success_url = reverse_lazy('ListCallCrm')
  
