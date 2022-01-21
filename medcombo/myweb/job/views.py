from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Job, Resume, Contract, Workday
from .forms import JobForm, JobForm_en, JobForm_zhh, JobForm_it, JobForm_pt, JobForm_de, JobForm_fr, JobForm_ja, JobForm_zh, ResumeForm, JobFilterForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import translation
from cities_light.models import Country, City
from django.db.models import Q

from django.core.paginator import Paginator

class CreateJob(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    form_class3 = JobForm_en
    form_class5 = JobForm_fr
    form_class6 = JobForm_it
    form_class7 = JobForm_pt
    form_class8 = JobForm_zh
    form_class9 = JobForm_ja
    form_class1 = JobForm_zhh
    form_class2 = JobForm_de
    template_name = 'myweb/job/create.html'
    success_url = reverse_lazy('list_offers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            formulario = JobForm_en
        if actual_lang == 'es':
            formulario = JobForm
        if actual_lang == 'it':
            formulario = JobForm_it
        if actual_lang == 'pt':
            formulario = JobForm_pt
        if actual_lang == 'de':
            formulario = JobForm_de
        if actual_lang == 'fr':
            formulario = JobForm_fr
        if actual_lang == 'ja':
            formulario = JobForm_ja
        if actual_lang == 'zh-hans':
            formulario = JobForm_zh
        if actual_lang == 'zh-hant':
            formulario = JobForm_zhh
        print(actual_lang)
        context['formulario'] = formulario
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            
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
            if form.is_valid():
                contract = request.POST.get('type_contract')
                workday = request.POST.get('work_day')
                print(contract)
                print(workday)
                # form.work_day= workday
                objeto = form.save()
                Job.objects.filter(pk=objeto.id).update(work_day=workday, type_contract= contract)
            
            
        return HttpResponseRedirect(reverse_lazy('list_offers'))


class ListJob(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'myweb/job/list_inscription_admin.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user.id)

class DetailJob(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'myweb/job/detail_admin.html'

class UpdateJob(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    form_class3 = JobForm_en
    form_class5 = JobForm_fr
    form_class6 = JobForm_it
    form_class7 = JobForm_pt
    form_class8 = JobForm_zh
    form_class9 = JobForm_ja
    form_class1 = JobForm_zhh
    form_class2 = JobForm_de
    template_name = "myweb/job/create.html"
    success_url = reverse_lazy('list_offers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        pk= self.kwargs['pk']
        if pk:
            myjob= Job.objects.get(pk=pk)
            print(myjob.type_contract)
            mycontract_id= myjob.type_contract
            myworkday_id= myjob.work_day
            idcontract= mycontract_id.id
            idworkday= myworkday_id.id
        else:
            idcontract= 0
            idworkday= 0
        print(mycontract_id)
        if actual_lang == 'en':
            formulario = JobForm_en
        if actual_lang == 'es':
            print('miiii pkkk')
            formulario = JobForm
            print('exitoso')
        if actual_lang == 'it':
            formulario = JobForm_it
        if actual_lang == 'pt':
            formulario = JobForm_pt
        if actual_lang == 'de':
            formulario = JobForm_de
        if actual_lang == 'fr':
            formulario = JobForm_fr
        if actual_lang == 'ja':
            formulario = JobForm_ja
        if actual_lang == 'zh-hans':
            formulario = JobForm_zh
        if actual_lang == 'zh-hant':
            formulario = JobForm_zhh
        print(actual_lang)
        context['contract']= idcontract
        context['workday']= idworkday
        context['formulario'] = formulario
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            
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
            if form.is_valid():
                #contract = request.POST.get('type_contract')
                #workday = request.POST.get('work_day')
                value=request.POST.get('show')
                if value=='on':
                    value= True
                else:
                    value= False
                # form.work_day= workday
                job_id = self.kwargs['pk']
                #myjob = Job.objects.get(pk=job_id)
                myjob= Job.objects.filter(pk=job_id)
                #objeto = form.save()
                myjob.update(name=request.POST.get('name'), 
                places=request.POST.get('places'),
                city=request.POST.get('city'),
                country=request.POST.get('country'),
                assignment=request.POST.get('assignment'),
                requirements=request.POST.get('requirements'),
                advantages=request.POST.get('advantages'), 
                salary_minimum=request.POST.get('salary_minimum'), 
                salary_maximum=request.POST.get('salary_maximum'),
                type_contract=request.POST.get('type_contract'),
                work_day= request.POST.get('work_day'),
                show= value,

                )
                
        return HttpResponseRedirect(reverse_lazy('list_offers'))

@login_required
def DeleteJob(request):
    if request.is_ajax:
        if request.method == 'POST':
            job = request.POST.get('job')
            deleting = Job.objects.get(pk=job)
            deleting.delete()
            return HttpResponse('Done')
    return HttpResponse('Error in request!')

@login_required
def ActiveJob(request):
    if request.is_ajax:
        if request.method == 'POST':
            id = request.POST.get('active')
            active = Job.objects.get(pk=id)
            if active.active == True:
                active.active = False
            else:
                active.active = True
            send = active.active
            active.save()
            return HttpResponse(send)
    return HttpResponse('Error in request!')

class RegistrationJob(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'myweb/job/create_inscription.html'
    success_url = reverse_lazy('list-front-offers')

    def get_context_data(self, **kwargs):
        context = super(RegistrationJob,self).get_context_data(**kwargs)
        resume = Resume.objects.filter(participant=self.request.user.pk,offer=self.kwargs.get('pk')).count() #manda un numero
        context['job'] = self.kwargs.get('pk')
        context['check'] = resume
        return context

    def get_success_url(self):
        pk_job = self.kwargs.get('pk')
        update_job = Job.objects.get(id=pk_job)
        query_job = Resume.objects.filter(offer=pk_job,condition="Pending").count()
        update_job.pending = query_job
        update_job.save()
        return reverse('list-front-offers')

class ListFrontJob(ListView):
    template_name = 'myweb/job/list.html'
    model = Job
    form_class = JobFilterForm
    
    def get_context_data(self, **kwargs):
        context = super(ListFrontJob,self).get_context_data(**kwargs)
        actual_lang = translation.get_language()
        objects = Job.objects.filter(active=True)
        countrys = Country.objects.all()
        
        if actual_lang == 'en':
            contracts = Contract.objects.filter(language_id= 3)
            shifts = Workday.objects.filter(language_id= 3)
        if actual_lang == 'es':
            contracts = Contract.objects.filter(language_id= 4)
            shifts = Workday.objects.filter(language_id= 4)
        if actual_lang == 'it':
            contracts = Contract.objects.filter(language_id= 6)
            shifts = Workday.objects.filter(language_id= 6)
        if actual_lang == 'pt':
            contracts = Contract.objects.filter(language_id= 7)
            shifts = Workday.objects.filter(language_id= 7)
        if actual_lang == 'de':
            contracts = Contract.objects.filter(language_id= 2)
            shifts = Workday.objects.filter(language_id= 2)
        if actual_lang == 'fr':
            contracts = Contract.objects.filter(language_id= 5)
            shifts = Workday.objects.filter(language_id= 5)
        if actual_lang == 'ja':
            contracts = Contract.objects.filter(language_id= 9)
            shifts = Workday.objects.filter(language_id= 9)
        if actual_lang == 'zh-hans':
            contracts = Contract.objects.filter(language_id= 8)
            shifts = Workday.objects.filter(language_id= 8)
        if actual_lang == 'zh-hant':
            contracts = Contract.objects.filter(language_id= 1)
            shifts = Workday.objects.filter(language_id= 1)
        
        paginator = Paginator(objects, 3)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)

        context['object_list'] = page_obj
        context['page_obj'] = page_obj
        context['countrys'] = countrys
        context['contracts'] = contracts
        context['shifts'] = shifts

        return context 

    def post(self, request, *args, **kwargs):
 
        if request.method == 'POST':
            actual_lang = translation.get_language()
            search_txt = request.POST.get('search_txt')
            countries = request.POST.getlist('country[]')
            salary = request.POST.get('salary')
            contract = request.POST.get('contract')
            shift = request.POST.get('shift')

            if salary != "":
                minium = salary.split("-")[0]
                maximum = salary.split("-")[1]
                if len(countries) != 0:
                    if contract !="":
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, salary_minimum__gt=minium, salary_maximum__lte=maximum, type_contract_id=contract, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, salary_minimum__gt=minium, salary_maximum__lte=maximum, type_contract_id=contract)
                    else:
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, salary_minimum__gt=minium, salary_maximum__lte=maximum, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, salary_minimum__gt=minium, salary_maximum__lte=maximum,)
                else:
                    if contract !="":
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt, salary_minimum__gt=minium, salary_maximum__lte=maximum, type_contract_id=contract, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt, salary_minimum__gt=minium, salary_maximum__lte=maximum, type_contract_id=contract)
                    else:
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt, salary_minimum__gt=minium, salary_maximum__lte=maximum, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt, salary_minimum__gt=minium, salary_maximum__lte=maximum)
            else:
                if len(countries) != 0:
                    if contract !="":
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, type_contract_id=contract)
                    else:
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt, country_id__in=countries, )
                else:
                    if contract !="":
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt,  type_contract_id=contract, work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt,  type_contract_id=contract)
                    else:
                        if shift != "":
                            objects = Job.objects.filter(active=True, name__contains=search_txt,  work_day_id=shift)
                        else:
                            objects = Job.objects.filter(active=True, name__contains=search_txt)
            paginator = Paginator(objects, 3)
            page = self.request.POST.get('page')
            page_obj = paginator.get_page(page)

            return render(request, 'myweb/job/filter.html', {'object_list': page_obj, 'page_obj': page_obj})
            
class DetailFrontJob(DetailView):
    model = Job
    template_name = 'myweb/job/detail.html'

class ListResume(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'myweb/job/list_participants.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        id_resume = self.kwargs.get('pk')
        return Resume.objects.filter(offer=id_resume)
    
    def get_context_data(self, **kwargs):
        context = super(ListResume,self).get_context_data(**kwargs)
        context['offer'] = self.kwargs.get('pk')
        return context

class DetailResume(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'myweb/job/detail_participant.html'

def ProcessResume(request):
    if request.is_ajax:
        if request.method == 'POST':
            id = request.POST.get('value')
            resume = Resume.objects.get(pk=id)
            resume.condition = 'Processing'
            resume.save()
            #Update counters
            pk = resume.offer.id
            update_job = Job.objects.get(id=pk)
            #Pending
            pending_job = Resume.objects.filter(offer=pk,condition="Pending").count()
            update_job.pending = pending_job
            update_job.save()
            #Processing
            processing_job = Resume.objects.filter(offer=pk,condition="Processing").count()
            update_job.processing = processing_job
            update_job.save()
            #Selecting
            selecting_job = Resume.objects.filter(offer=pk,condition="Discarding").count()
            update_job.discarding = selecting_job
            update_job.save()
            return HttpResponse('Ok')
    return HttpResponse('Error in request!')

@login_required
def DiscardResume(request):
    if request.is_ajax:
        if request.method == 'POST':
            id = request.POST.get('value')
            resume = Resume.objects.get(pk=id)
            resume.condition = 'Discarding'
            resume.save()
            #Update counters
            pk = resume.offer.id
            update_job = Job.objects.get(id=pk)
            #Pending
            pending_job = Resume.objects.filter(offer=pk,condition="Pending").count()
            update_job.pending = pending_job
            update_job.save()
            #Processing
            processing_job = Resume.objects.filter(offer=pk,condition="Processing").count()
            update_job.processing = processing_job
            update_job.save()
            #Selecting
            selecting_job = Resume.objects.filter(offer=pk,condition="Discarding").count()
            update_job.discarding = selecting_job
            update_job.save()
            return HttpResponse('Ok')
    return HttpResponse('Error in request!')

@login_required
def DeleteResume(request):
    if request.is_ajax:
        if request.method == 'POST':
            id = request.POST.get('value')
            resume = Resume.objects.get(pk=id)
            pk = resume.offer.id
            resume.delete()
            #Update counters
            pk = resume.offer.id
            update_job = Job.objects.get(id=pk)
            #Pending
            pending_job = Resume.objects.filter(offer=pk,condition="Pending").count()
            update_job.pending = pending_job
            update_job.save()
            #Processing
            processing_job = Resume.objects.filter(offer=pk,condition="Processing").count()
            update_job.processing = processing_job
            update_job.save()
            #Selecting
            selecting_job = Resume.objects.filter(offer=pk,condition="Discarding").count()
            update_job.discarding = selecting_job
            update_job.save()
            return HttpResponse('Ok')
    return HttpResponse('Error in request!')

@login_required
def SearchOffer(request):
    if request.is_ajax():
        if request.method == 'POST':
            value = request.POST.get('val','')
            my_object = Job.objects.filter(name__icontains=value, user=request.user.id)
            return render(request, 'myweb/job/search_list.html', {'object_list': my_object})
    return HttpResponse('Error in your request!')

@login_required
def SearchParticipant(request):
    if request.is_ajax():
        if request.method == 'POST':
            value = request.POST.get('val','')
            offer = request.POST.get('ref')
            my_object = Resume.objects.filter(participant__first_name__icontains=value, offer=offer)
            return render(request, 'myweb/job/search_participants.html', {'object_list': my_object})
    return HttpResponse('Error in your request!')