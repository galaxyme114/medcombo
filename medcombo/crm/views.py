from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
#from pure_pagination.mixins import PaginationMixin
from .models import Opportunity, Task, Call, HistoryOpportunity, HistoryCall
from medcombo.configuration.usercustom.models import User
from .forms import LeadForm, CompanyContactForm, HistoryForm
from medcombo.configuration.company.models import Company
from medcombo.product.models import Product
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

####----------------Modulo Contacto--------------------------
class CreateContacCrm(CreateView): 
    model = User
    template_name = "crm/contact/add_contact.html"
    form_class = LeadForm
    second_form_class = CompanyContactForm
    success_url = reverse_lazy('ListContacCrm')
    
    def get_context_data(self, **kwargs):
        context = super(CreateContacCrm, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.company = form2.save()
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class ListContacCrm(ListView):
    model = User
    ordering = ['-id']
    template_name = "crm/contact/list.html"

    def get_queryset(self):
        return User.objects.filter(lead=1)

class DetailContacCrm(DetailView):
    model = User
    template_name = "crm/contact/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        opportunity_list = Opportunity.objects.filter(client_id=self.kwargs.get('pk')).values_list('id', flat=True)
        call_list = Call.objects.filter(client_id=self.kwargs.get('pk')).values_list('id', flat=True)
        context['histories'] = HistoryOpportunity.objects.filter(opportunity_id__in=opportunity_list)
        context['calls'] = HistoryCall.objects.filter(call_id__in=call_list)
        return context

class UpdateContacCrm(UpdateView):
    model = User
    second_model= Company
    template_name = "crm/contact/add_contact.html"
    form_class = LeadForm
    second_form_class = CompanyContactForm
    success_url = reverse_lazy('ListContacCrm')
    
    def get_context_data(self, **kwargs):
        context = super(UpdateContacCrm, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        user = self.model.objects.get(id=pk)
        company = self.second_model.objects.get(id=user.company_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=company)
        context['id'] = pk
        return context

    def post(self, request,*args, **kwargs):
        self.object = self.get_object
        id_user = kwargs['pk']
        user = self.model.objects.get(id=id_user)
        company = self.second_model.objects.get(id=user.company_id)
        form = self.form_class(request.POST, instance=user)
        form2 = self.second_form_class(request.POST, instance=company)
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.company = form2.save()
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class DeleteContacCrm(DeleteView):
	model = User
	template_name = "crm/contact/delete.html"
	success_url = reverse_lazy('ListContacCrm')

#####------------ Modulo Tareas-------------------
class CreateTaskCrm(CreateView):
    model = Task
    fields = '__all__'
    template_name = "crm/task/create.html"
    success_url = reverse_lazy('ListTaskCrm')

class ListTaskCrm(ListView):
    model = Task
    ordering = ['-id']
    template_name = "crm/task/list.html"

class ReadyTaskCrm(CreateView):
    model = HistoryOpportunity
    fields = '__all__'
    template_name = "crm/task/ready.html"
    success_url = reverse_lazy('ListTaskCrm')

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs.get('pk'))
        return context

class UpdateTaskCrm(UpdateView):
    model = Task
    fields = '__all__'
    template_name = "crm/task/create.html"
    success_url = reverse_lazy('ListTaskCrm')

class DeleteTaskCrm(DeleteView):
	model = Task
	template_name = "crm/task/delete.html"
	success_url = reverse_lazy('ListTaskCrm')

#####---------------Modulo Llamadas---------------
class CreateCallCrm(CreateView):
    model = Call
    fields = '__all__'
    template_name = "crm/call/create.html"
    success_url = reverse_lazy('ListCallCrm') 

class ListCallCrm(ListView):
    model = Call
    ordering = ['id']
    template_name = "crm/call/list.html"

class DetailCallCrm(CreateView):
    model = HistoryCall
    fields = '__all__'
    template_name = "crm/call/detail.html"
    success_url = reverse_lazy('ListCallCrm')    

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['calls'] = Call.objects.get(pk=self.kwargs.get('pk'))
        return context

class UpdateCallCrm(UpdateView):
    model = Call
    fields = '__all__'
    template_name = "crm/call/create.html"
    success_url = reverse_lazy('ListCallCrm')

class DeleteCallCrm(DeleteView):
	model = Call
	template_name = "crm/call/delete.html"
	success_url = reverse_lazy('ListCallCrm')

####----------Modulo oportunidades---------  
class CreateOpportunityCrm(CreateView):
    model = Opportunity
    fields = '__all__'
    template_name = "crm/opportunity/add_create.html"
    success_url = reverse_lazy('OpportunityList')  

class OpportunityList(ListView):
    model = Opportunity
    ordering = ['-id']
    template_name = "crm/opportunity/list.html"

class DetailOpportunityCrm(DetailView):
    model = Opportunity     
    template_name = "crm/opportunity/detail.html"    

    def get_context_data(self, **kwargs):
        registro = Opportunity.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['client'] = User.objects.filter(id=registro.client.id)
        context['histories'] = HistoryOpportunity.objects.filter(opportunity_id=self.kwargs.get('pk'))
        return context

def add_state(request):
    opportunity_id = request.GET.get('opportunity_id')
    state_id = request.GET.get('state')
    register = Opportunity.objects.filter(pk=opportunity_id).update(state=state_id)
    return('pass')      

#####---- Modulo Lead-------------------
class LeadSuccessCrm(TemplateView):
    template_name = "crm/lead/lead_success.html"

class LeadCrm(CreateView):
    model = User
    form_class = LeadForm
    template_name = 'crm/lead/create.html'
    success_url = reverse_lazy('LeadSuccessCrm')

#------------ Modulo Producto ------------
class CreateProductCrm(CreateView):
    model = Product
    fields = ['name', 'product_ID', 'price', 'company', 'ref', 'notes']
    template_name = "crm/product/create.html"
    success_url = reverse_lazy('ListProductCrm')

class ListProductCrm(ListView):
    queryset = Product.objects.filter(company=1)
    context_object_name = 'product'
    template_name = "crm/product/list.html"

class UpdateProductCrm(UpdateView):
    model = Product
    fields = ['name', 'product_ID', 'price', 'ref', 'notes']
    template_name = "crm/product/update.html"
    success_url = reverse_lazy('ListProductCrm')

class DetailProductCrm(DetailView):
    model = Product
    template_name = "crm/product/detail.html"

