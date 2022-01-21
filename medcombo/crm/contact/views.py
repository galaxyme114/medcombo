from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from .forms import LeadForm, CompanyContactForm, CountryContactForm
from .forms import LeadForm_en,LeadForm_zh,LeadForm_zhh,LeadForm_de,LeadForm_fr,LeadForm_it,LeadForm_pt,LeadForm_ja
from medcombo.crm.opportunity.models import Opportunity, HistoryOpportunity
from medcombo.configuration.usercustom.models import User, Work
from medcombo.configuration.company.models import Company
from medcombo.crm.call.models import Call, HistoryCall
from .models import PolityToken
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import csv
import os
from cities_light.models import Country
from cities_light.models import City
from dal import autocomplete
from medcombo.product.models import CsvArchivo
from django.utils.crypto import get_random_string
import os.path
from django.utils import translation


class CreateContacCrm(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = User
    template_name = "crm/contact/add_contact.html"
    form_class = LeadForm
    form_class2 = LeadForm_de
    form_class3 = LeadForm_en
    form_class5 = LeadForm_fr
    form_class6 = LeadForm_it
    form_class7 = LeadForm_pt
    form_class8 = LeadForm_zh
    form_class9 = LeadForm_ja
    form_class1 = LeadForm_zhh
    second_form_class = CompanyContactForm
    success_url = reverse_lazy('ListContacCrm')
    
    def get_context_data(self, **kwargs):
        context = super(CreateContacCrm, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            formulario = Work.objects.filter(language_id=3)
        if actual_lang == 'es':
            formulario = Work.objects.filter(language_id=4)
        if actual_lang == 'it':
            formulario = Work.objects.filter(language_id=6)
        if actual_lang == 'pt':
            formulario = Work.objects.filter(language_id=7)
        if actual_lang == 'de':
            formulario = Work.objects.filter(language_id=2)
        if actual_lang == 'fr':
            formulario = Work.objects.filter(language_id=5)
        if actual_lang == 'ja':
            formulario = Work.objects.filter(language_id=9)
        if actual_lang == 'zh-hans':
            formulario = Work.objects.filter(language_id=8)
        if actual_lang == 'zh-hant':
            formulario = Work.objects.filter(language_id=1)
        context['work']= 0
        context['formulario'] = formulario
        return context

    def post(self, request, *args, **kwargs):
        print('++++++++++++++++++++++++++++++++++++++++++++++++')
        self.object = self.get_object
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            form = self.form_class3(request.POST)
        if actual_lang == 'es':
            form = self.form_class(request.POST)
        if actual_lang == 'it':
            form = self.form_class6(request.POST)
        if actual_lang == 'pt':
            form = self.form_class7(request.POST)
        if actual_lang == 'de':
            form = self.form_class2(request.POST)
        if actual_lang == 'fr':
            form = self.form_class5(request.POST)
        if actual_lang == 'ja':
            form = self.form_class9(request.POST)
        if actual_lang == 'zh-hans':
            form = self.form_class8(request.POST)
        if actual_lang == 'zh-hant':
            form = self.form_class1(request.POST)
        workid = request.POST.get('work')
        if workid:
            work= Work.objects.get(pk=workid)
        else:
            work = None

        #form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        tracing = request.POST.getlist('tracing')
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.company = form2.save()
            companyid= user.company.pk
            company=Company.objects.get(pk=companyid)
            company.notify= False
            company.save()
            user.work= work
            user.save()
            new_user = User.objects.get(id=user.pk)
            for t in tracing:
                employee = User.objects.get(id=int(t))
                new_user.tracing.add(employee)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

#Module: Leads - Sales
class ListContacCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    model = User
    #ordering = ['id']
    template_name = "crm/contact/list.html"

    def get_context_data(self, **kwargs):
        context = super(ListContacCrm, self).get_context_data(**kwargs)
        my_country = CountryContactForm
        context['my_country'] = my_country
        return context

    def get_queryset(self):
        return User.objects.filter(lead=1).order_by('-date_joined')



class DetailContacCrm(PermissionRequiredMixin, DetailView):
    permission_required = 'usercustom.sales_user'
    model = User
    template_name = "crm/contact/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailContacCrm, self).get_context_data(**kwargs)
        opportunity_list = Opportunity.objects.filter(client_id=self.kwargs.get('pk')).values_list('id', flat=True)
        call_list = Call.objects.filter(client_id=self.kwargs.get('pk')).values_list('id', flat=True)
        context['histories'] = HistoryOpportunity.objects.filter(opportunity_id__in=opportunity_list)
        context['calls'] = HistoryCall.objects.filter(call_id__in=call_list)
        return context

class UpdateContacCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.sales_user'
    model = User
    second_model= Company
    template_name = "crm/contact/add_contact.html"
    form_class = LeadForm
    form_class2 = LeadForm_de
    form_class3 = LeadForm_en
    form_class5 = LeadForm_fr
    form_class6 = LeadForm_it
    form_class7 = LeadForm_pt
    form_class8 = LeadForm_zh
    form_class9 = LeadForm_ja
    form_class1 = LeadForm_zhh
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

        actual_lang = translation.get_language()
        pk= self.kwargs['pk']
        if pk:
            myuser= User.objects.get(pk=pk)
            mywork_id= myuser.work
            if mywork_id:
                idwork= mywork_id.id #el id que voy a cargar en el select
            else:
                idwork=0
        else:
            idwork= 0
        if actual_lang == 'en':
            formulario = Work.objects.filter(language_id=3)
        if actual_lang == 'es':
            formulario = Work.objects.filter(language_id=4)
        if actual_lang == 'it':
            formulario = Work.objects.filter(language_id=6)
        if actual_lang == 'pt':
            formulario = Work.objects.filter(language_id=7)
        if actual_lang == 'de':
            formulario = Work.objects.filter(language_id=2)
        if actual_lang == 'fr':
            formulario = Work.objects.filter(language_id=5)
        if actual_lang == 'ja':
            formulario = Work.objects.filter(language_id=9)
        if actual_lang == 'zh-hans':
            formulario = Work.objects.filter(language_id=8)
        if actual_lang == 'zh-hant':
            formulario = Work.objects.filter(language_id=1)
        context['work']= idwork
        context['formulario'] = formulario
        return context

    def post(self, request,*args, **kwargs):
        self.object = self.get_object
        id_user = kwargs['pk']
        user = self.model.objects.get(id=id_user)
        company = self.second_model.objects.get(id=user.company_id)
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            form = self.form_class3(request.POST, instance=user)
        if actual_lang == 'es':
            form = self.form_class(request.POST, instance=user)
        if actual_lang == 'it':
            form = self.form_class6(request.POST, instance=user)
        if actual_lang == 'pt':
            form = self.form_class7(request.POST, instance=user)
        if actual_lang == 'de':
            form = self.form_class2(request.POST, instance=user)
        if actual_lang == 'fr':
            form = self.form_class5(request.POST, instance=user)
        if actual_lang == 'ja':
            form = self.form_class9(request.POST, instance=user)
        if actual_lang == 'zh-hans':
            form = self.form_class8(request.POST, instance=user)
        if actual_lang == 'zh-hant':
            form = self.form_class1(request.POST, instance=user)
        workid = request.POST.get('work')
        if workid:
            work= Work.objects.get(pk=workid)
        else:
            work = None
        #form = self.form_class(request.POST, instance=user)
        form2 = self.second_form_class(request.POST, instance=company)
        tracing = request.POST.getlist('tracing')
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.company = form2.save()
            user.work= work
            user.save()
            new_user = User.objects.get(id=user.pk)
            new_user.tracing.clear()
            for t in tracing:
                employee = User.objects.get(id=int(t))
                new_user.tracing.add(employee)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class DeleteContacCrm(LoginRequiredMixin, DeleteView):
	model = User
	template_name = "crm/contact/delete.html"
	success_url = reverse_lazy('Home')

class PrivacyPolity(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    template_name = "crm/contact/privacy_policy.html"
    model= Company
    second_model= PolityToken
    fields = ['policy_accept', 'date_policy_accept', 'ip_policy_accept']

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolity, self).get_context_data(**kwargs)
        token = PolityToken.objects.filter(token=self.kwargs.get('token'), state=False)
        if token.exists():
            context['state'] = True
            context['token'] = token.first()
        else:
            context['state'] = False
        return context

    def post(self, request, *args, **kwargs):
        token = PolityToken.objects.get(id=request.POST.get('token_id'))
        token.state = True
        token.save()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        company = Company.objects.get(id=token.company_id)
        company.policy_accept = True
        company.date_policy_accept = datetime.today().date()
        company.ip_policy_accept = ip
        company.save()
        return HttpResponseRedirect(reverse_lazy('Home'))

class PrivacyPolityConfirm(PermissionRequiredMixin, TemplateView):
    permission_required = 'usercustom.sales_user'
    template_name = "crm/contact/content_email_polity.html"

class PrivacyPolitySend(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = PolityToken
    fields = '__all__'
    template_name= "crm/contact/sendprivacypolity.html"
    success_url = reverse_lazy('ListContacCrm')

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolitySend, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        token = get_random_string(length=40)
        company = request.POST.get('company_id')
        email_user = request.POST.get('user_email')
        body = render_to_string(
            'crm/contact/content_email_polity.html', {
                'dominio': request.build_absolute_uri('/PrivacyPolity/' + token),
                'user': User.objects.get(pk=self.kwargs.get('pk')),
            }
        )
        email_message = EmailMessage(
            subject='Medcombo - Politicas de Privacidad',
            body=body,
            from_email='riera_1992@hotmail.com',
            to=[email_user]
        )
        email_message.content_subtype = 'html'
        email_message.send()
        polityToken = PolityToken(token=token, company_id=company)
        polityToken.save()
        return HttpResponseRedirect(reverse_lazy('ListContacCrm'))

@permission_required('usercustom.sales_user')
def index(request):
        return render(request, 'crm/contact/inicio.html')

@permission_required('usercustom.sales_user')
def ContactDelete(request):
    id = request.POST.get('value')
    my_contact = User.objects.get(id=id)
    my_contact.delete()
    return HttpResponse('Ok')

class CityAutocompleteContact(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class CityAutocompleteContactTwo(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        country = self.forwarded.get('country_company', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

@permission_required('usercustom.sales_user')
def SendPrivacyPolity(request):
    token = get_random_string(length=40)
    user = request.POST.get('value')
    company = request.POST.get('company_id')
    email_user = request.POST.get('user_email')
        
    body = render_to_string(
        'crm/contact/content_email_polity.html', {
            'dominio': request.build_absolute_uri('/PrivacyPolity/' + token),
            'user': User.objects.get(pk=int(user)),
        }
    )
    email_message = EmailMessage(
        subject='Medcombo - Politicas de Privacidad',
        body=body,
        from_email='riera_1992@hotmail.com',
        to=[email_user]
    )
    email_message.content_subtype = 'html'
    email_message.send()
    polityToken = PolityToken(token=token, company_id=int(company))
    polityToken.save()
    return HttpResponse("Ok")

@permission_required('usercustom.sales_user')
def AddUserLead(request):
    id = request.POST.get('value')
    my_user_lead = User.objects.get(id=id)
    user_new = User.objects.filter(lead=False).filter(employee=False)
    my_list = []
    if user_new.count() == 0:
        my_user_lead.username = 1000
    else:
        for user in user_new:
            value = str(user.username).isdigit()
            if value == True:
                my_list.append(int(user.username))
        order = sorted(my_list, key=int, reverse=True)
        if order:
            my_user_lead.username = order[0] + 1
        else:
            my_user_lead.username = 1000
    my_user_lead.lead = False
    my_user_lead.employee = False
    my_user_lead.save()
    id_company = my_user_lead.company.pk
    print(id_company)
    company= Company.objects.get(pk=id_company)
    company.approved= True
    company.save()
    return HttpResponse('Ok')