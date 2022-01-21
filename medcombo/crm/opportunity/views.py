from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Opportunity, HistoryOpportunity, StateOpportunity
from medcombo.configuration.usercustom.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .forms import OpportunityForm, OpportunityUpdateForm, OpportunityChangeForm

class CreateOpportunityCrm(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = Opportunity
    #fields = '__all__'
    form_class = OpportunityForm
    template_name = "crm/opportunity/add_create.html"
    #success_url = reverse_lazy('OpportunityList')

    def get_success_url(self):
        opportunity_id = self.object.pk
        my_opportunity = Opportunity.objects.get(id=opportunity_id)
        name_state = StateOpportunity.objects.get(id=1)
        history = HistoryOpportunity(opportunity=my_opportunity,notes=name_state)
        history.save()
        return reverse('OpportunityList')

class UpdateOpportunityCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.sales_user'
    model = Opportunity
    form_class = OpportunityChangeForm
    template_name = "crm/opportunity/add_create.html"

    def get_success_url(self):
        opportunity_id = self.object.pk
        print(opportunity_id)
        return reverse_lazy('DetailOpportunityCrm',kwargs={'pk': opportunity_id})

#Module: Opportunity - sales
class OpportunityList(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    model = Opportunity
    ordering = ['-id']
    template_name = "crm/opportunity/list.html"

    def get_queryset(self):
        return Opportunity.objects.filter(responsible=self.request.user.id)

class DetailOpportunityCrm(PermissionRequiredMixin, DetailView):
    permission_required = 'usercustom.sales_user'
    model = Opportunity     
    template_name = "crm/opportunity/detail.html"    

    def get_context_data(self, **kwargs):
        registro = Opportunity.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['client'] = User.objects.filter(id=registro.client.id)
        context['histories'] = HistoryOpportunity.objects.filter(opportunity_id=self.kwargs.get('pk'))
        context['form_opp'] = OpportunityUpdateForm
        return context

@permission_required('usercustom.sales_user')
def add_state(request):
    opportunity_id = request.GET.get('opportunity_id')
    state_id = request.GET.get('state')
    percentage = 0
    name_state = StateOpportunity.objects.get(id=state_id)
    register = Opportunity.objects.filter(pk=opportunity_id).update(state=state_id)
    print(register)
    my_opportunity = Opportunity.objects.get(id=opportunity_id)
    if my_opportunity.automatic_percent == True:
        name_state.id
        if name_state.id == 1:
            percentage = 20
        elif name_state.id == 2:
            percentage = 50
        elif name_state.id == 3:
            percentage = 75
        elif name_state.id == 4:
            percentage = 100
        else:
            percentage = 0
        my_opportunity.probability = percentage
        my_opportunity.save()
    history = HistoryOpportunity(opportunity=my_opportunity,notes=name_state)
    history.save()
    histories =  HistoryOpportunity.objects.filter(opportunity_id=opportunity_id)
    return render(request, 'crm/opportunity/history_list.html', {'histories': histories})

class OpportunitySummary(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    model = Opportunity
    ordering = ['-id']
    template_name = "crm/opportunity/summary.html"

    def get_queryset(self):
        users_opportunity = User.objects.filter(employee=1).exclude(lead=1)
        return users_opportunity

class OpportunitySummaryDetail(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    model = Opportunity
    ordering = ['-id']
    template_name = "crm/opportunity/detail_summary.html"

    def get_queryset(self):
        id_responsible = self.kwargs.get('pk')
        return Opportunity.objects.filter(responsible=id_responsible)

    def get_context_data(self, **kwargs):
        #registro = Opportunity.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        registro = User.objects.get(pk=self.kwargs.get('pk'))
        #Total Opportunities
        oppotunities_total = Opportunity.objects.filter(responsible=self.kwargs.get('pk')).count()
        oppotunities_total_won = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=4).count()
        oppotunities_total_lost = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=5).count()
        #Total Expected Revenue
        revenue_total = Opportunity.objects.filter(responsible=self.kwargs.get('pk'))
        revenue_total_won = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=4)
        revenue_total_lost = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=5)
        total_rev = 0
        total_rev_w = 0
        total_rev_l = 0
        for rt in revenue_total:
            total_rev = total_rev + rt.expected_revenue
        for rt in revenue_total_won:
            total_rev_w = total_rev_w + rt.expected_revenue
        for rt in revenue_total_lost:
            total_rev_l = total_rev_l + rt.expected_revenue
        #Total Expected Revenue
        oppotunity_new = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=1).count()
        oppotunity_contact = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=2).count()
        oppotunity_send = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=3).count()
        oppotunity_won = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=4).count()
        oppotunity_lost = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=5).count()
        revenue_n = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=1)
        revenue_c = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=2)
        revenue_s = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=3)
        revenue_w = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=4)
        revenue_l = Opportunity.objects.filter(responsible=self.kwargs.get('pk'), state=5)
        rev_n= 0
        rev_c = 0
        rev_s = 0
        rev_w = 0
        rev_l = 0
        for rt in revenue_n:
            rev_n = rev_n + rt.expected_revenue
        for rt in revenue_c:
            rev_c = rev_c + rt.expected_revenue
        for rt in revenue_s:
            rev_s = rev_s + rt.expected_revenue
        for rt in revenue_w:
            rev_w = rev_w + rt.expected_revenue
        for rt in revenue_l:
            rev_l = rev_l + rt.expected_revenue
        #context
        context['responsible'] = registro
        context['total'] = oppotunities_total
        context['total_won'] = oppotunities_total_won
        context['total_lost'] = oppotunities_total_lost
        context['revenue'] = total_rev
        context['revenue_won'] = total_rev_w
        context['revenue_lost'] = total_rev_l
        context['new'] = oppotunity_new
        context['contact'] = oppotunity_contact
        context['send'] = oppotunity_send
        context['won'] = oppotunity_won
        context['lost'] = oppotunity_lost
        context['rev_new'] = rev_n
        context['rev_contact'] = rev_c
        context['rev_send'] = rev_s
        context['rev_won'] = rev_w
        context['rev_lost'] = rev_l
        return context

@permission_required('usercustom.sales_user')
def OpportunityChangePercent(request):
    opportunity_id = request.GET.get('opportunity_id')
    opportunity = Opportunity.objects.get(id=opportunity_id)
    return HttpResponse(opportunity.probability)

@permission_required('usercustom.sales_user')
def DeleteOpportunity(request):
    id = request.POST.get('value')
    opportunity = Opportunity.objects.get(id=id)
    opportunity.delete()
    return HttpResponse('Ok')