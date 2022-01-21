from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from medcombo.configuration.company.models import Company, DescriptionCompany, LanguageModel
from medcombo.configuration.company.models import BoostingCompany
from medcombo.configuration.usercustom.models import User
from medcombo.configuration.company.forms import CityForm, CompanyUpdateForm, CompanyFacturationForm
from django.shortcuts import render
from medcombo.product.models import Product
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from django.shortcuts import render, redirect
from django.utils import translation
from django.contrib import messages
from datetime import date


def DeleteLogoCompany(request):
    my_company =Company.objects.get(id=request.user.company.id)
    my_company.logo = None
    my_company.save()
    return HttpResponse('Ok')

class MywebCompanyDetail(LoginRequiredMixin, DetailView):
    template_name = 'myweb/company/detail.html'
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['descriptions'] = DescriptionCompany.objects.all()
        return context

class MywebCompanyDetailFacturacion(LoginRequiredMixin, DetailView):
    template_name = 'myweb/company/detail_facturacion.html'
    model = Company

class MywebConfirmForm(LoginRequiredMixin, TemplateView):
    template_name = 'myweb/company/confirm_form.html'

class MywebCompanyCreate(LoginRequiredMixin, CreateView):
    template_name = 'myweb/company/create.html'
    #model = Company
    form_class = CityForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            objeto = form.save()
            today = date.today()
            create = Company.objects.get(pk=objeto.id)
            create.createdate = today
            create.save()
            model2 = User.objects.filter(pk=self.request.user.id).update(company=objeto.id)
            my_company = Company.objects.get(id=objeto.pk)
            object_boosting = BoostingCompany(company_boosting=my_company, certification_boosting='subtracted', manufacturer_boosting='subtracted')
            object_boosting.save()
            return HttpResponseRedirect('/myweb/product/list/')
        return render(request, self.template_name, {'form': form})  

class MywebCompanyUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'myweb/company/update.html'
    model = Company
    form_class = CompanyUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=self.kwargs.get('pk'))
        context['descriptions'] = DescriptionCompany.objects.all()
        return context

    def get_success_url(self):
        #Boosting to ISO Certification and Manufacturer
        my_company = Company.objects.get(id=self.object.pk)
        certification = Company.objects.filter(id=self.object.pk)
        boosting = BoostingCompany.objects.filter(company_boosting=my_company)
        if boosting:
            boosting_company = BoostingCompany.objects.get(company_boosting=my_company)
        my_product = Product.objects.filter(company=my_company)
        iso = ''
        manufacturer = 0
        for c in certification:
            manufacturer = c.type_company
            iso = c.certification_iso
        #Editing
        if boosting:
            if manufacturer == 8:
                if boosting[0].manufacturer_boosting == 'subtracted':
                    if my_product:
                        if len(my_product) == 0:
                            for p in my_product:
                                product = Product.objects.get(id=p.id)
                                product.algorithmic_value = p.algorithmic_value + 10
                                product.save()
                            boosting_company.manufacturer_boosting = 'added'
                            boosting_company.save()
                        else:
                            if boosting_company.manufacturer_flag_boosting == True:
                                for p in my_product:
                                    product = Product.objects.get(id=p.id)
                                    product.algorithmic_value = p.algorithmic_value + 10
                                    product.save()
                                boosting_company.manufacturer_flag_boosting = False
                            boosting_company.manufacturer_boosting = 'added'
                            boosting_company.save()
            else:
                if boosting[0].manufacturer_boosting == 'added':
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value - 10
                            product.save()
                        boosting_company.manufacturer_boosting = 'subtracted'
                        boosting_company.manufacturer_flag_boosting = True
                        boosting_company.save()
            if iso == '' or iso is None:
                if boosting[0].certification_boosting == 'added':
                    my_product = Product.objects.filter(company=my_company)
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value - 10
                            product.save()
                        boosting_company.certification_boosting = 'subtracted'
                        boosting_company.save()
            else:
                if boosting[0].certification_boosting == 'subtracted':
                    my_product = Product.objects.filter(company=my_company)
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value + 10
                            product.save()
                        boosting_company.certification_boosting = 'added'
                        boosting_company.save()
        #Creating
        else:
            object_boosting = BoostingCompany(company_boosting=my_company, certification_boosting='subtracted', manufacturer_boosting='subtracted')
            object_boosting.save()
            new_boosting = BoostingCompany.objects.filter(company_boosting=my_company)
            my_boosting = BoostingCompany.objects.get(company_boosting=my_company)
            if manufacturer == 8:
                if new_boosting[0].manufacturer_boosting == 'subtracted':
                    my_product = Product.objects.filter(company=my_company)
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value + 10
                            product.save()
                        my_boosting.manufacturer_boosting = 'added'
                        my_boosting.save()
            else:
                if new_boosting[0].manufacturer_boosting == 'added':
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value - 10
                            product.save()
                        my_boosting.manufacturer_boosting = 'subtracted'
                        my_boosting.save()
            if iso == '' or iso is None:
                if new_boosting[0].certification_boosting == 'added':
                    my_product = Product.objects.filter(company=my_company)
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value - 10
                            product.save()
                        my_boosting.certification_boosting = 'subtracted'
                        my_boosting.save()
            else:
                if new_boosting[0].certification_boosting == 'subtracted':
                    my_product = Product.objects.filter(company=my_company)
                    if my_product:
                        for p in my_product:
                            product = Product.objects.get(id=p.id)
                            product.algorithmic_value = p.algorithmic_value + 10
                            product.save()
                        my_boosting.certification_boosting = 'added'
                        my_boosting.save()
        return reverse('detail_company', kwargs={'pk': self.object.pk})

class MywebCompanyUpdateFacturacion(LoginRequiredMixin, UpdateView):
    template_name = 'myweb/company/update_facturacion.html'
    model = Company
    form_class = CompanyFacturationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('detail_company_facturacion', kwargs={'pk': self.object.pk})

class MywebCompanyCreateDescription(LoginRequiredMixin, CreateView):
    model = DescriptionCompany
    fields= '__all__'
    template_name = 'myweb/company/create_description_company.html'
    success_url = reverse_lazy('detail_company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_company = self.kwargs.get('pk')
        context['company_pk'] = id_company
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            lang_pk = request.POST.get('language')
            company_pk = request.POST.get('company')
            mylang= LanguageModel.objects.get(pk=lang_pk)
            mycompany= Company.objects.get(pk=company_pk)
            mytitle= request.POST.get('title')
            paragraph= request.POST.get('paragraph')
            if paragraph=='' or paragraph.isspace() or paragraph==None or paragraph.isdigit() or paragraph=='<p><br></p>':
                actual_lang = translation.get_language()
                if actual_lang=='es':
                    messages.error(request, 'Debe ingresar una descripción')
                if actual_lang=='zh-hant':
                    messages.error(request, '您必須輸入描述')
                if actual_lang=='de':
                    messages.error(request, 'Sie müssen eine Beschreibung eingeben')
                if actual_lang=='en':
                    messages.error(request, 'You must enter a description')
                if actual_lang=='fr':
                    messages.error(request, 'Vous devez saisir une description')
                if actual_lang=='it':
                    messages.error(request, 'Devi inserire una descrizione')
                if actual_lang=='pt':
                    messages.error(request, 'Você deve inserir uma descrição')
                if actual_lang=='zh-hans':
                    messages.error(request, '您必须输入描述')
                if actual_lang=='ja':
                    messages.error(request, '説明を入力する必要があります')
                return HttpResponseRedirect(reverse_lazy('CreateDescriptionCompany', kwargs={'pk':self.kwargs.get('pk')}))
            
            myvideo= request.FILES.get('video')
            newDescription = DescriptionCompany(
                    title= mytitle,
                    language= mylang,
                    company= mycompany,
                    paragraph= paragraph,
                    video= myvideo
                    )
            existe= DescriptionCompany.objects.filter(language= lang_pk, company=company_pk).count()
            if(existe== 0): #si no existen politicas para ese idioma y esa empresa, las creo. si existe una, la actualizo
                newDescription.save()
                print('guardado')
                return HttpResponseRedirect(reverse_lazy('update_company', kwargs={'pk': company_pk}))
            else:
                DescriptionCompany.objects.get(language=lang_pk, company=company_pk).delete()
                newDescription.save()
                return HttpResponseRedirect(reverse_lazy('update_company', kwargs={'pk': company_pk}))

class MywebCompanyUpdateDescription(LoginRequiredMixin, UpdateView):
    model = DescriptionCompany
    fields = ['title', 'paragraph', 'video']
    template_name = "myweb/company/update_description_company.html"
    success_url = reverse_lazy('detail_company')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            #debo enviar el pk de mi description y guardar cada campo
            mipk= request.POST.get('pk')
            company_pk= request.POST.get('pkcompany')
            paragraph = request.POST.get('paragraph')
            if paragraph=='' or paragraph.isspace() or paragraph==None or paragraph.isdigit() or paragraph=='<p><br></p>':
                actual_lang = translation.get_language()
                if actual_lang=='es':
                    messages.error(request, 'Debe ingresar una descripción')
                if actual_lang=='zh-hant':
                    messages.error(request, '您必須輸入描述')
                if actual_lang=='de':
                    messages.error(request, 'Sie müssen eine Beschreibung eingeben')
                if actual_lang=='en':
                    messages.error(request, 'You must enter a description')
                if actual_lang=='fr':
                    messages.error(request, 'Vous devez saisir une description')
                if actual_lang=='it':
                    messages.error(request, 'Devi inserire una descrizione')
                if actual_lang=='pt':
                    messages.error(request, 'Você deve inserir uma descrição')
                if actual_lang=='zh-hans':
                    messages.error(request, '您必须输入描述')
                if actual_lang=='ja':
                    messages.error(request, '説明を入力する必要があります')
                return HttpResponseRedirect(reverse_lazy('UpdateDescriptionCompany', kwargs={'pk':self.kwargs.get('pk')}))
            
            send = DescriptionCompany.objects.get(pk=mipk)
            send.title = request.POST.get('title')
            send.paragraph = request.POST.get('paragraph')
            if request.FILES.get('video') != None:
                send.video = request.FILES.get('video')
            else:
                pass
            send.save()
            return HttpResponseRedirect(reverse_lazy('update_company', kwargs={'pk': company_pk}))



def MywebCompanyCopyUpdateFacturacion(request, pk):
    company = Company.objects.get(pk=pk)
    company.invoicing_company_name = company.name
    company.invoicing_address = company.address
    company.invoicing_postal_code = company.code_postal
    company.invoicing_telephone = company.telephone
    company.invoicing_city = company.city_company
    company.invoicing_country = company.country_company
    company.save()
    return HttpResponse('Ok')
