from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from medcombo.crm.dashboard_admin.models import Banner, Campaign, LanguageCampaign, BannerIndex, CompanyLogo, Event
from medcombo.crm.dashboard_admin.forms import BannerForm, CampaignForm, SponsorForm, BannerIndexForm, CompanyLogoForm, EventForm
from medcombo.product.models import BannerWeb
from medcombo.configuration.company.models import Company
from medcombo.product.models import Sponsor
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
import json
#import base64
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import translation
import csv
import os
from medcombo.product.models import CsvArchivo
from django.utils.crypto import get_random_string
import os.path
from cities_light.models import Country
from cities_light.models import City
from medcombo.product.models import Searchkey_static
from medcombo.product.models import Click_static
from django.db.models import Count
from medcombo.configuration.usercustom.models import User, Work
from medcombo.product.models import Product, SuggestionKeyword, BoostingKeyword, Area, Category, SubCategory, Keyword
#import requests
from PIL import Image
from io import StringIO
import urllib
import datetime
from django.utils import translation
from django.core.paginator import Paginator
from django.contrib import messages
import time
import validators
from PIL import Image

from django.db.models import Q

class DashboardAdmin(PermissionRequiredMixin, TemplateView):
    permission_required = 'usercustom.marketing_user'
    template_name = "crm/dashboard_admin/index.html"

#Module: Banner - marketing
class BannerList(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = Campaign
    template_name = "crm/dashboard_admin/list.html"

    def get_context_data(self, **kwargs):
        context = super(BannerList, self).get_context_data(**kwargs)
        actual_language = translation.get_language()
        context['banner'] = Banner.objects.all().filter(language_campaign__value_language=actual_language)
        context['list_company_banner'] = BannerWeb.objects.all()
        return context 

class BannerPicture(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = Banner
    template_name = "crm/dashboard_admin/banner.html"

    def get_context_data(self, **kwargs):
        context = super(BannerPicture, self).get_context_data(**kwargs)
        context['campaign'] = self.kwargs.get('pk')
        context['language'] = LanguageCampaign.objects.all().order_by('value_language')
        pk = Banner.objects.all().filter(banner_campaign=int(self.kwargs.get('pk')))
        context['banner'] = pk
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            valor = request.POST.get('requestID')
            banner_campaign = Campaign.objects.get(id=int(request.POST.get('campaignId')))
            language_campaign = LanguageCampaign.objects.get(id=int(request.POST.get('selectBanner')))
            url_campaign = request.POST.get('urlBanner')
            picture_campaign = request.FILES.get('customFileBanner')
            if valor == 'create':
                banner_exist = Banner.objects.filter(banner_campaign=int(request.POST.get('campaignId')), language_campaign=int(request.POST.get('selectBanner')))
                if banner_exist:
                    print('This register has been saved!')
                else:
                    objectBanner = Banner(
                        banner_campaign = banner_campaign,
                        language_campaign = language_campaign,
                        url_campaign = url_campaign,
                        picture_campaign = picture_campaign
                    )
                    objectBanner.save()
            else:
                banner_id = int(request.POST.get('bannerId'))
                banner_update = Banner.objects.get(id=banner_id)
                if picture_campaign is None:
                    picture_campaign = banner_update.picture_campaign
                #print(banner_update.picture_campaign.read())
                banner_update.url_campaign = url_campaign
                banner_update.picture_campaign = picture_campaign
                #img = picture_campaign.read()
                #print("data:image/png;base64," + base64.b64encode(img).decode('utf8'))
                banner_update.save()
            return HttpResponseRedirect('')
        else:
            return HttpResponseRedirect('')

class BannerCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.marketing_user'
    form_class = CampaignForm
    template_name = "crm/dashboard_admin/update.html"
    success_url = reverse_lazy('BannerList')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            actual_lang = translation.get_language()
            start = request.POST.get('start_campaign')
            end = request.POST.get('end_campaign')
            position = request.POST.get('position_campaign')
            form = CampaignForm(request.POST)
            # try:
            #     start = time.strptime(start, '%d/%m/%Y')
            #     end = time.strptime(end, '%d/%m/%Y')
            # except ValueError:
            #     if actual_lang=='es':
            #         messages.error(request, 'Fechas inválidas')
            #     if actual_lang=='zh-hant':
            #         messages.error(request, '無效的日期')
            #     if actual_lang=='de':
            #         messages.error(request, 'SUngültige Daten')
            #     if actual_lang=='en':
            #         messages.error(request, 'Invalid Dates')
            #     if actual_lang=='fr':
            #         messages.error(request, 'Dates invalides')
            #     if actual_lang=='it':
            #         messages.error(request, 'Date non valide')
            #     if actual_lang=='pt':
            #         messages.error(request, 'Datas inválidas')
            #     if actual_lang=='zh-hans':
            #         messages.error(request, '无效的日期')
            #     if actual_lang=='ja':
            #         messages.error(request, '無効な日付')
            #     return HttpResponseRedirect(reverse_lazy('BannerCreate'))

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('BannerList'))
            # if str(start) <= str(end):
            #     print(start)
            #     print(end)
            #     form.save()
            #     return HttpResponseRedirect(reverse_lazy('BannerList'))
            # else:
            #     form_class = CampaignForm
            #     if actual_lang=='es':
            #         messages.error(request, 'Fechas inválidas')
            #     if actual_lang=='zh-hant':
            #         messages.error(request, '無效的日期')
            #     if actual_lang=='de':
            #         messages.error(request, 'SUngültige Daten')
            #     if actual_lang=='en':
            #         messages.error(request, 'Invalid Dates')
            #     if actual_lang=='fr':
            #         messages.error(request, 'Dates invalides')
            #     if actual_lang=='it':
            #         messages.error(request, 'Date non valide')
            #     if actual_lang=='pt':
            #         messages.error(request, 'Datas inválidas')
            #     if actual_lang=='zh-hans':
            #         messages.error(request, '无效的日期')
            #     if actual_lang=='ja':
            #         messages.error(request, '無効な日付')
            #     return HttpResponseRedirect(reverse_lazy('BannerCreate'))
        else:
            form_class = CampaignForm
            if actual_lang=='es':
                messages.error(request, 'Ha ocurrido un error')
            if actual_lang=='zh-hant':
                messages.error(request, '發生錯誤')
            if actual_lang=='de':
                messages.error(request, 'Ein Fehler ist aufgetreten')
            if actual_lang=='en':
                messages.error(request, 'An error has occurred')
            if actual_lang=='fr':
                messages.error(request, "Une erreur s'est produite")
            if actual_lang=='it':
                messages.error(request, 'Si è verificato un errore')
            if actual_lang=='pt':
                messages.error(request, 'Ocorreu um erro')
            if actual_lang=='zh-hans':
                messages.error(request, '发生错误')
            if actual_lang=='ja':
                messages.error(request, 'エラーが発生しました')
            return HttpResponseRedirect(reverse_lazy('BannerCreate'))



class BannerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = Campaign
    form_class = CampaignForm
    template_name = "crm/dashboard_admin/update.html"
    success_url = reverse_lazy('BannerList')

    # def post(self, request, *args, **kwargs):
    #     actual_lang = translation.get_language()
    #     if request.method == 'POST':
    #         start = request.POST.get('start_campaign')
    #         end = request.POST.get('end_campaign')
    #         position = request.POST.get('position_campaign')
    #         form = CampaignForm(request.POST)
    #         form.save()
    #         return HttpResponseRedirect(reverse_lazy('BannerList'))
        #     try:
        #         if actual_lang == 'en':
        #             start = datetime.datetime.strptime(start,"%m/%d/%Y")
        #             end = datetime.datetime.strptime(end,"%m/%d/%Y")
        #         elif actual_lang == 'de':
        #             start = datetime.datetime.strptime(start,"%d.%m.%Y")
        #             end = datetime.datetime.strptime(end,"%d.%m.%Y")
        #         elif actual_lang == 'zh-hans':
        #             start = datetime.datetime.strptime(start,"%Y/%m/%d")
        #             end = datetime.datetime.strptime(end,"%Y/%m/%d")
        #         elif actual_lang == 'ja':
        #             start = datetime.datetime.strptime(start,"%Y-%m-%d")
        #             end = datetime.datetime.strptime(end,"%Y-%m-%d")
        #         elif actual_lang == 'zh-hant':
        #             start = datetime.datetime.strptime(start,"%Y/%m/%d")
        #             end = datetime.datetime.strptime(end,"%Y/%m/%d")
        #         else:
        #             print('+++++++++++++++++++++++++++++ aquii +++++++++++')
        #             start = datetime.datetime.strptime(start,"%d/%m/%Y")
        #             end = datetime.datetime.strptime(end,"%d/%m/%Y")
        #         #start = time.strptime(start, '%d/%m/%Y')
               
        #     except ValueError:
        #         if actual_lang=='es':
        #             messages.error(request, 'Fechas inválidas')
        #         if actual_lang=='zh-hant':
        #             messages.error(request, '無效的日期')
        #         if actual_lang=='de':
        #             messages.error(request, 'SUngültige Daten')
        #         if actual_lang=='en':
        #             messages.error(request, 'Invalid Dates')
        #         if actual_lang=='fr':
        #             messages.error(request, 'Dates invalides')
        #         if actual_lang=='it':
        #             messages.error(request, 'Date non valide')
        #         if actual_lang=='pt':
        #             messages.error(request, 'Datas inválidas')
        #         if actual_lang=='zh-hans':
        #             messages.error(request, '无效的日期')
        #         if actual_lang=='ja':
        #             messages.error(request, '無効な日付')
        #         return HttpResponseRedirect('/BannerUpdate/'+self.kwargs.get('pk'))

        # if form.is_valid():
        #     # if str(start) <= str(end):
        #     #     print(start)
        #     #     print(end)
        #     #     form.save()
        #     #     return HttpResponseRedirect(reverse_lazy('BannerList'))
        #     # else:
        #     #     form_class = CampaignForm
        #     #     if actual_lang=='es':
        #     #         messages.error(request, 'Fechas inválidas')
        #     #     if actual_lang=='zh-hant':
        #     #         messages.error(request, '無效的日期')
        #     #     if actual_lang=='de':
        #     #         messages.error(request, 'SUngültige Daten')
        #     #     if actual_lang=='en':
        #     #         messages.error(request, 'Invalid Dates')
        #     #     if actual_lang=='fr':
        #     #         messages.error(request, 'Dates invalides')
        #     #     if actual_lang=='it':
        #     #         messages.error(request, 'Date non valide')
        #     #     if actual_lang=='pt':
        #     #         messages.error(request, 'Datas inválidas')
        #     #     if actual_lang=='zh-hans':
        #     #         messages.error(request, '无效的日期')
        #     #     if actual_lang=='ja':
        #     #         messages.error(request, '無効な日付')
        #     #     return HttpResponseRedirect('/BannerUpdate/'+self.kwargs.get('pk'))
        # else:
        #     form_class = CampaignForm
        #     if actual_lang=='es':
        #         messages.error(request, 'Ha ocurrido un error')
        #     if actual_lang=='zh-hant':
        #         messages.error(request, '發生錯誤')
        #     if actual_lang=='de':
        #         messages.error(request, 'Ein Fehler ist aufgetreten')
        #     if actual_lang=='en':
        #         messages.error(request, 'An error has occurred')
        #     if actual_lang=='fr':
        #         messages.error(request, "Une erreur s'est produite")
        #     if actual_lang=='it':
        #         messages.error(request, 'Si è verificato un errore')
        #     if actual_lang=='pt':
        #         messages.error(request, 'Ocorreu um erro')
        #     if actual_lang=='zh-hans':
        #         messages.error(request, '发生错误')
        #     if actual_lang=='ja':
        #         messages.error(request, 'エラーが発生しました')
        #     return HttpResponseRedirect('/BannerUpdate/'+self.kwargs.get('pk'))

@permission_required('usercustom.marketing_user')
def SearchBoosting(request,area,category,subcategory,keyword):
    q = request.POST.get('q','')
    if q:
        product = Product.objects.filter(keyword__name__icontains=q).order_by('-algorithmic_value')
    else:
        product = Product.objects.all().exclude(company=1).order_by('-algorithmic_value')

    paginator = Paginator(product, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'crm/dashboard_admin/boosting.html', {'product': page_obj, 'page_obj':page_obj})

def ListCategories(request):
    if request.method == 'POST':
        #Language selected
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            arealang = 'area'
            categorylang = 'categoría'
            subcategorylang = 'subcategoría'
        elif actual_lang == 'de':
            arealang = 'bereich'
            categorylang = 'kategorie'
            subcategorylang = 'unterkategorie'
        elif actual_lang == 'en':
            arealang = 'area'
            categorylang = 'category'
            subcategorylang = 'subcategory'
        elif actual_lang == 'fr':
            arealang = 'zone'
            categorylang = 'catégorie'
            subcategorylang = 'sous catégorie'
        elif actual_lang == 'it':
            arealang = 'zona'
            categorylang = 'categoria'
            subcategorylang = 'sotto-categoria'
        elif actual_lang == 'pt':
            arealang = 'area'
            categorylang = 'categoria'
            subcategorylang = 'subcategoria'
        elif actual_lang == 'zh-hans':
            arealang = '区域'
            categorylang = '类别'
            subcategorylang = '子类别'
        elif actual_lang == 'ja':
            arealang = '面積'
            categorylang = 'カテゴリー'
            subcategorylang = 'サブカテゴリ'
        elif actual_lang == 'zh-hant':
            arealang = '區'
            categorylang = '類別'
            subcategorylang = '子類別'
        my_keyword = request.POST.get('key')
        if my_keyword is None or my_keyword == "":
            register = None
        else:
            register = Keyword.objects.filter(name__iexact=my_keyword)
        results = []
        if register:
            for r in register:
                if r.area:
                    results.append(r.area.name)
                else:
                    results.append(arealang)
                if r.category:
                    results.append(r.category.name)
                else:
                    results.append(categorylang)
                if r.subcategory:
                    results.append(r.subcategory.name)
                else:
                    results.append(subcategorylang)
                data = json.dumps(results)
            mimetype = 'application/json'
            return HttpResponse(data, mimetype)
        else:
            my_list = {'a':arealang, 'b':categorylang, 'c':subcategorylang}
            results.append(my_list.get('a'))
            results.append(my_list.get('b'))
            results.append(my_list.get('c'))
            data = json.dumps(results)
            mimetype = 'application/json'
            return HttpResponse(data, mimetype)
    return HttpResponse('Error in request!')

@permission_required('usercustom.marketing_user')
def SendBoosting(request):
    if request.method == 'POST':
        actual_lang = translation.get_language()
        valueToAdd = 0
        idProduct = request.POST.get('productId')
        valueAdded = request.POST.get('value_added')
        referenceProduct = Product.objects.get(id=idProduct)
        if valueAdded.isdigit():
            valueAdded = valueAdded
        elif valueAdded.startswith('-') and valueAdded[1:].isdigit():
            valueAdded = valueAdded
        else:
            valueAdded = 0
            if actual_lang=='es':
                return HttpResponse('Debe ingresar un valor numérico')
            if actual_lang=='zh-hant':
                return HttpResponse('您必須輸入一個數值')
            if actual_lang=='de':
                return HttpResponse('Sie müssen einen numerischen Wert eingeben')
            if actual_lang=='en':
                return HttpResponse('You must enter a numerical value')
            if actual_lang=='fr':
                return HttpResponse('Vous devez saisir une valeur numérique')
            if actual_lang=='it':
                return HttpResponse('Devi inserire un valore numerico')
            if actual_lang=='pt':
                return HttpResponse('Você deve inserir um valor numérico')
            if actual_lang=='zh-hans':
                return HttpResponse('您必须输入一个数值')
            if actual_lang=='ja':
                return HttpResponse('数値を入力する必要があります')
            
        valueToAdd = referenceProduct.algorithmic_value + int(valueAdded)
        referenceProduct.algorithmic_value = valueToAdd
        referenceProduct.save()
        return HttpResponse('Ok')
    return HttpResponse('Error in request!')

#Module: Boosting - marketing
class Boosting(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = Product
    template_name = "crm/dashboard_admin/boosting.html"

    def get_context_data(self, **kwargs):
        context = super(Boosting, self).get_context_data(**kwargs)
        products = Product.objects.all().exclude(company=1).order_by('-algorithmic_value')
        paginator = Paginator(products, 20)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['product'] = page_obj
        context['page_obj'] = page_obj
        return context

#Module: Stats - marketing
class Stats(PermissionRequiredMixin, TemplateView):
    permission_required = 'usercustom.marketing_user'
    template_name = "crm/dashboard_admin/stats.html"

    def get_context_data(self, **kwargs):
        context = super(Stats, self).get_context_data(**kwargs)
        statistic_all = Searchkey_static.objects.all().exclude(searchkey_name="").count()
        click_all = Click_static.objects.all().count()
        if statistic_all != 0:
            statistic = Searchkey_static.objects.exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 
            click_statistic = Click_static.objects.values('product_name').annotate(dcount=Count('product_name')).order_by('-dcount')
            
            statis_language = Searchkey_static.objects.exclude(searchkey_name="").exclude(language=None).values('language_id').annotate(dcount=Count('language_id')).order_by('-dcount')
            arr_statis_pie = [[]]
            arr_statis_pie.clear()
            head = ['language', 'dcount']
            arr_statis_pie.append(head)
            for statis in statis_language:
                temp = []
                language = LanguageCampaign.objects.get(id=statis["language_id"])
                temp.append(language.name_language)
                temp.append(float(statis['dcount']))
                arr_statis_pie.append(temp)
                statis["language"] = language
                statis["child"] = Searchkey_static.objects.filter(language_id=statis["language_id"]).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 

            count_none_user = Searchkey_static.objects.filter(user=None).exclude(searchkey_name="").count()
            count_user = Searchkey_static.objects.filter(~Q(user=None)).exclude(searchkey_name="").count()
            arr_statis_user = [[]]
            arr_statis_user.clear()
            arr_statis_user.append(['user', 'dcount'])
            arr_statis_user.append(['visitor', count_none_user])
            arr_statis_user.append(['user', count_user])

            statis_user = Searchkey_static.objects.exclude(searchkey_name="").exclude(user=None).values('user_id').annotate(dcount=Count('user_id')).order_by('-dcount')
            for statis in statis_user:
                user = User.objects.get(id=statis["user_id"])
                statis["user"] = user
                childs = Searchkey_static.objects.filter(user_id=statis["user_id"]).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 
                for child in childs:
                    child["last_date"] = Searchkey_static.objects.filter(user_id=statis["user_id"], searchkey_name=child["searchkey_name"]).values('search_date').order_by('-search_date')[0]
                statis["child"] = childs
            statis_none_user = {}
            statis_none_user["user_id"] = None
            statis_none_user["dcount"] = count_none_user
            childs = Searchkey_static.objects.filter(user=None).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 
            for child in childs:
                child["last_date"] = Searchkey_static.objects.filter(user=None, searchkey_name=child["searchkey_name"]).values('search_date').order_by('-search_date')[0]
            statis_none_user["child"] = childs

            statis_ipaddress = Searchkey_static.objects.exclude(searchkey_name="").values('ip_address').annotate(dcount=Count('searchkey_name')).order_by('-dcount')
            
            arr_statis_address = [[]]
            arr_statis_address.clear()
            arr_statis_address.append(['ip_address', 'dcount'])
            for statis in statis_ipaddress:
                if statis["ip_address"]:
                    arr_statis_address.append([statis["ip_address"], float(statis['dcount'])])
                else:
                    arr_statis_address.append(["None", float(statis['dcount'])])

            print(statis_none_user)
            context['statis_user'] = statis_user
            context['statis_none_user'] = statis_none_user
            context['statis_language'] = statis_language
            context['arr_statis_pie'] = arr_statis_pie
            context['arr_statis_user'] = arr_statis_user
            context['arr_statis_address'] = arr_statis_address
            context['statistic_all'] = statistic_all
            context['click_all'] = click_all
            context['statistic'] = statistic
            context['click_statistic'] = click_statistic

        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            start = request.POST.get('start_date')
            end = request.POST.get('end_date')
            statistic_all = Searchkey_static.objects.filter(search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").count()
            click_all = Click_static.objects.filter(click_date__gte=start, click_date__lte=end).count()
            if statistic_all != 0:
                statistic = Searchkey_static.objects.filter(search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount')
                click_statistic = Click_static.objects.filter(click_date__gte=start, click_date__lte=end).values('product_name').annotate(dcount=Count('product_name')).order_by('-dcount')
                
                statis_language = Searchkey_static.objects.filter(search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").exclude(language=None).values('language_id').annotate(dcount=Count('language_id')).order_by('-dcount')
                arr_statis_pie = [[]]
                arr_statis_pie.clear()
                head = ['language', 'dcount']
                arr_statis_pie.append(head)
                for statis in statis_language:
                    temp = []
                    language = LanguageCampaign.objects.get(id=statis["language_id"])
                    temp.append(language.name_language)
                    temp.append(float(statis['dcount']))
                    arr_statis_pie.append(temp)
                    statis["language"] = language
                    statis["child"] = Searchkey_static.objects.filter(language_id=statis["language_id"], search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 

                count_none_user = Searchkey_static.objects.filter(user=None, search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").count()
                count_user = Searchkey_static.objects.filter(~Q(user=None), search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").count()
                arr_statis_user = [[]]
                arr_statis_user.clear()
                arr_statis_user.append(['user', 'dcount'])
                arr_statis_user.append(['visitor', count_none_user])
                arr_statis_user.append(['user', count_user])

                statis_user = Searchkey_static.objects.filter(search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").exclude(user=None).values('user_id').annotate(dcount=Count('user_id')).order_by('-dcount')
                for statis in statis_user:
                    user = User.objects.get(id=statis["user_id"])
                    statis["user"] = user
                    childs = Searchkey_static.objects.filter(user_id=statis["user_id"], search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 
                    for child in childs:
                        child["last_date"] = Searchkey_static.objects.filter(user_id=statis["user_id"], searchkey_name=child["searchkey_name"], search_date__gte=start, search_date__lte=end).values('search_date').order_by('-search_date')[0]
                    statis["child"] = childs
                statis_none_user = {}
                statis_none_user["user_id"] = None
                statis_none_user["dcount"] = count_none_user
                childs = Searchkey_static.objects.filter(user=None, search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").values('searchkey_name').annotate(dcount=Count('searchkey_name')).order_by('-dcount') 
                for child in childs:
                    child["last_date"] = Searchkey_static.objects.filter(user=None, searchkey_name=child["searchkey_name"], search_date__gte=start, search_date__lte=end).values('search_date').order_by('-search_date')[0]
                statis_none_user["child"] = childs

                statis_ipaddress = Searchkey_static.objects.filter(search_date__gte=start, search_date__lte=end).exclude(searchkey_name="").values('ip_address').annotate(dcount=Count('searchkey_name')).order_by('-dcount')
                
                arr_statis_address = [[]]
                arr_statis_address.clear()
                arr_statis_address.append(['ip_address', 'dcount'])
                for statis in statis_ipaddress:
                    if statis["ip_address"]:
                        arr_statis_address.append([statis["ip_address"], float(statis['dcount'])])
                    else:
                        arr_statis_address.append(["None", float(statis['dcount'])])
            
                return render(request, 'crm/dashboard_admin/stats.html', {'statistic': statistic, 'statistic_all':statistic_all, 'click_statistic':click_statistic, 'click_all':click_all, 'start':start, 'end':end, 'statis_user': statis_user, 'statis_none_user': statis_none_user, 'statis_language': statis_language, 'arr_statis_pie': arr_statis_pie, 'arr_statis_address': arr_statis_address, 'arr_statis_user': arr_statis_user})
            else:
                return render(request, 'crm/dashboard_admin/stats.html', {'start': start, 'end':end})

#Module: Sponsor - marketing
class SponsorList(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = Sponsor
    template_name = "crm/dashboard_admin/sponsor.html"

class SponsorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.marketing_user'
    form_class = SponsorForm
    template_name = "crm/dashboard_admin/sponsor_create.html"
    success_url = reverse_lazy('Sponsor_List')

    def get_context_data(self, **kwargs):
        context = super(SponsorCreate, self).get_context_data(**kwargs)
        userLead= User.objects.filter(lead=True)
        context['Leads'] = userLead
        return context

class SponsorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = Sponsor
    form_class = SponsorForm
    template_name = "crm/dashboard_admin/sponsor_create.html"
    success_url = reverse_lazy('Sponsor_List')

def autocompleteModelBoosting(request):
    if request.is_ajax():
        q = request.GET.get('phrase', '').capitalize()
        actual_languague_p = translation.get_language()
        search_qs = Keyword.objects.filter(name__startswith=q, language__value_language=actual_languague_p)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@permission_required('usercustom.marketing_user')
def SponsorCompany(request):
    if request.method == 'POST':
        id = request.POST.get('company')
        company = Company.objects.filter(id=id)
        for name in company:
            my_company = name.name
        return HttpResponse(my_company)
    return HttpResponse('Error in request!')

@permission_required('usercustom.marketing_user')
def SponsorTable(request):
    id = request.POST.get('company')
    product = Product.objects.filter(company=id)
    return render(request, 'crm/dashboard_admin/search_product_sponsor.html', {'product': product})

@permission_required('usercustom.marketing_user')
def SponsorSearchTable(request):
    id = request.POST.get('company')
    name_product = request.POST.get('product')
    product = Product.objects.filter(company=id, name__icontains=name_product)
    return render(request, 'crm/dashboard_admin/search_product_sponsor.html', {'product': product})

@permission_required('usercustom.marketing_user')
def SponsorAjaxIcon(request):
    if request.is_ajax:
        if request.method == 'POST':
            id = request.POST.get('sponsor')
            active = Sponsor.objects.get(pk=id)
            if active.active == True:
                active.active = False
            else:
                active.active = True
            send = active.active
            active.save()
            return HttpResponse(send)
    return HttpResponse('Error in request!')

#Module: Banner Index - marketing
class BannerIndexList(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = BannerIndex
    template_name = "crm/dashboard_admin/banner_list_index.html"
    ordering = ['date'] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = self.kwargs.get('lang')
        if actual_lang:
            actual_lang = actual_lang
        else:
            actual_lang = 'es'
        if actual_lang == 'es':
            idlang = 4
        elif actual_lang == 'en':
            idlang = 3
        elif actual_lang == 'de':
            idlang = 2
        elif actual_lang == 'fr':
            idlang = 5
        elif actual_lang == 'it':
            idlang = 6
        elif actual_lang == 'pt':
            idlang = 7
        elif actual_lang == 'zh-hant':
            idlang = 1
        elif actual_lang == 'zh-hans':
            idlang = 8
        elif actual_lang == 'ja':
            idlang = 9
        mybanner = BannerIndex.objects.filter(language=idlang)
        paginator = Paginator(mybanner, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['selected'] = actual_lang
        context['banner'] = page_obj
        context['page_obj'] = page_obj
        context['language_medmagazine'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

class BannerIndexCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.marketing_user'
    model = BannerIndex 
    form_class = BannerIndexForm
    template_name = "crm/dashboard_admin/banner_index.html"
    #success_url = reverse_lazy('BannerIndexList/es')

    def get_context_data(self, **kwargs):
        context = super(BannerIndexCreate, self).get_context_data(**kwargs)
        context['language'] = LanguageCampaign.objects.all()
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 4
        elif actual_lang == 'en':
            idlang = 3
        elif actual_lang == 'de':
            idlang = 2
        elif actual_lang == 'fr':
            idlang = 5
        elif actual_lang == 'it':
            idlang = 6
        elif actual_lang == 'pt':
            idlang = 7
        elif actual_lang == 'zh-hant':
            idlang = 1
        elif actual_lang == 'zh-hans':
            idlang = 8
        elif actual_lang == 'ja':
            idlang = 9
        context['language_selected_id'] = idlang
        return context

    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':
            id_language = request.POST.get('language')
            order_created = request.POST.get('order_created') 
            actual_lang = translation.get_language()
            title = request.POST.get('title')
            
            if title==None or title.isspace() or title.isdigit() or title=='' or (order_created.isdigit()==False):
                if actual_lang=='es':
                    messages.error(request, 'Ha ocurrido un error')
                if actual_lang=='zh-hant':
                    messages.error(request, '發生錯誤')
                if actual_lang=='de':
                    messages.error(request, 'Ein Fehler ist aufgetreten')
                if actual_lang=='en':
                    messages.error(request, 'An error has occurred')
                if actual_lang=='fr':
                    messages.error(request, "Une erreur s'est produite")
                if actual_lang=='it':
                    messages.error(request, 'Si è verificato un errore')
                if actual_lang=='pt':
                    messages.error(request, 'Ocorreu um erro')
                if actual_lang=='zh-hans':
                    messages.error(request, '发生错误')
                if actual_lang=='ja':
                    messages.error(request, 'エラーが発生しました')
                return HttpResponseRedirect(reverse_lazy('BannerIndexCreate'))

            picture = request.FILES.get('picture')
            video = request.FILES.get('video')
            description = request.POST.get('description')
            date = request.POST.get('date')
            author = request.POST.get('author')
            title = request.POST.get('title')            
            language = LanguageCampaign.objects.get(id=int(id_language))
            
            try:
                if actual_lang == 'en':
                    date = datetime.datetime.strptime(date,"%m/%d/%Y")
                elif actual_lang == 'de':
                    date = datetime.datetime.strptime(date,"%d.%m.%Y")
                elif actual_lang == 'zh-hans':
                    date = datetime.datetime.strptime(date,"%Y/%m/%d")
                elif actual_lang == 'ja':
                    date = datetime.datetime.strptime(date,"%Y-%m-%d")
                elif actual_lang == 'zh-hant':
                    date = datetime.datetime.strptime(date,"%Y/%m/%d")
                else:
                    date = datetime.datetime.strptime(date,"%d/%m/%Y")
            except ValueError:
                if actual_lang=='es':
                    messages.error(request, 'Fecha inválida')
                if actual_lang=='zh-hant':
                    messages.error(request, '無效的日期')
                if actual_lang=='de':
                    messages.error(request, 'SUngültige Daten')
                if actual_lang=='en':
                    messages.error(request, 'Invalid Date')
                if actual_lang=='fr':
                    messages.error(request, 'Date invalide')
                if actual_lang=='it':
                    messages.error(request, 'Date non valide')
                if actual_lang=='pt':
                    messages.error(request, 'Data inválida')
                if actual_lang=='zh-hans':
                    messages.error(request, '无效的日期')
                if actual_lang=='ja':
                    messages.error(request, '無効な日付')
                return HttpResponseRedirect(reverse_lazy('BannerIndexCreate'))
                
            objectBanner = BannerIndex(
                language = language,
                url='',
                picture = picture,
                description = description,
                date = date,
                author = author,
                order_created = order_created,
                title = title,
                video = video
            )
            objectBanner.save()
            
            
            return HttpResponseRedirect('/BannerIndexList/es')
        else:
            return HttpResponseRedirect('/BannerIndexList/es')

class BannerIndexUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = BannerIndex
    form_class = BannerIndexForm
    template_name = "crm/dashboard_admin/banner_index.html"
    #success_url = reverse_lazy('BannerIndexList/es')

    def get_context_data(self, **kwargs):
        context = super(BannerIndexUpdate, self).get_context_data(**kwargs)
        banner_id = self.kwargs.get('pk')
        banner = BannerIndex.objects.get(id=banner_id)
        print(banner.language.pk)
        context['language_selected_id'] = banner.language.pk
        context['language'] = LanguageCampaign.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            id_language = request.POST.get('language') 
            picture = request.FILES.get('picture')
            video = request.FILES.get('video')
            description = request.POST.get('description')
            date = request.POST.get('date')
            author = request.POST.get('author')
            title = request.POST.get('title')
            order_created = request.POST.get('order_created')
            language = LanguageCampaign.objects.get(id=int(id_language))
            banner_id = self.kwargs.get('pk')
            banner_update = BannerIndex.objects.get(id=banner_id)
            if video is None:
                video = banner_update.video
            if picture is None:
                picture = banner_update.picture
            banner_update.picture = picture
            banner_update.video = video
            banner_update.language = language
            banner_update.description = description
            #Language selected
            actual_lang = translation.get_language()
            if actual_lang == 'en':
                date = datetime.datetime.strptime(date,"%m/%d/%Y")
            elif actual_lang == 'de':
                date = datetime.datetime.strptime(date,"%d.%m.%Y")
            elif actual_lang == 'zh-hans':
                date = datetime.datetime.strptime(date,"%Y/%m/%d")
            elif actual_lang == 'ja':
                date = datetime.datetime.strptime(date,"%Y-%m-%d")
            elif actual_lang == 'zh-hant':
                date = datetime.datetime.strptime(date,"%Y/%m/%d")
            else:
                date = datetime.datetime.strptime(date,"%d/%m/%Y")
            banner_update.date = date
            banner_update.author = author
            banner_update.title = title
            banner_update.order_created = order_created
            banner_update.save()
            
            return HttpResponseRedirect('/BannerIndexList/es')
        else:
            return HttpResponseRedirect('/BannerIndexList/es')

#Module: Company Logo - marketing
class CompanyLogoList(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = CompanyLogo
    template_name = "crm/dashboard_admin/companylogo_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companylogo = CompanyLogo.objects.all()
        paginator = Paginator(companylogo, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['company_logo'] = page_obj
        context['page_obj'] = page_obj
        return context

class CompanyLogoCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.marketing_user'
    model = CompanyLogo 
    form_class = CompanyLogoForm
    template_name = "crm/dashboard_admin/companylogo_create.html"
    
    def get_context_data(self, **kwargs):
        context = super(CompanyLogoCreate, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':
            url = request.POST.get('url')
            title = request.POST.get('title')
            x= validators.url(url)
            if (x!=True):
                return HttpResponseRedirect(reverse_lazy('CompanyLogoCreate'))
            
            picture = request.FILES.get('picture')
            logo_exist = CompanyLogo.objects.filter(url=url)

            if logo_exist:
                print('This register has been saved!')
            else:
                objectLogo = CompanyLogo(
                    url = url,
                    picture = picture,
                    title = title
                )
                objectLogo.save()
            return HttpResponseRedirect('/CompanyLogoList')
        else:
            return HttpResponseRedirect('/CompanyLogoList')

class CompanyLogoUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = CompanyLogo
    form_class = CompanyLogoForm
    template_name = "crm/dashboard_admin/companylogo_create.html"
    
    def get_context_data(self, **kwargs):
        context = super(CompanyLogoUpdate, self).get_context_data(**kwargs)
        logo_id = self.kwargs.get('pk')
        logo = CompanyLogo.objects.get(id=logo_id)
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            url = request.POST.get('url')
            title = request.POST.get('title')
            picture = request.FILES.get('picture')
            logo_id = self.kwargs.get('pk')
            banner_update = CompanyLogo.objects.get(id=logo_id)
            if picture is None:
                picture = banner_update.picture
            banner_update.url = url
            banner_update.title = title
            banner_update.picture = picture
            banner_update.save()
            return HttpResponseRedirect('/CompanyLogoList')
        else:
            return HttpResponseRedirect('/CompanyLogoList')

def CompanyLogoDelete(request):
    my_id = request.POST.get('value')
    companylogo = CompanyLogo.objects.get(id=my_id)
    companylogo.delete()
    return HttpResponse('Ok')
#Module: Event - marketing
class EventList(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = Event
    template_name = "crm/dashboard_admin/event_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.all().order_by("-end_event", "-start_event")
        paginator = Paginator(event, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['event'] = page_obj
        context['page_obj'] = page_obj
        return context

class EventCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.marketing_user'
    model = Event 
    form_class = EventForm
    template_name = "crm/dashboard_admin/event_create.html"
    
    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':
            title = request.POST.get('title')
            picture = request.FILES.get('picture')
            
            start_event = request.POST.get('start_event')
            end_event = request.POST.get('end_event')
            
            description_es = request.POST.get('description_es')
            description_en = request.POST.get('description_en')
            description_pt = request.POST.get('description_pt')
            description_fr = request.POST.get('description_fr')
            description_it = request.POST.get('description_it')
            description_de = request.POST.get('description_de')
            description_zh_hant = request.POST.get('description_zh_hant')
            description_zh_hans = request.POST.get('description_zh_hans')
            description_jp = request.POST.get('description_jp')
            
            objectEvent = Event(
                start_event = start_event,
                end_event = end_event,
                picture = picture,
                title = title,
                description_es = description_es,
                description_en = description_en,
                description_pt = description_pt,
                description_fr = description_fr,
                description_it = description_it,
                description_de = description_de,
                description_zh_hant = description_zh_hant,
                description_zh_hans = description_zh_hans,
                description_jp = description_jp
            )
            objectEvent.save()
            return HttpResponseRedirect('/EventList')
        else:
            return HttpResponseRedirect('/EventList')

class EventUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = Event
    form_class = EventForm
    template_name = "crm/dashboard_admin/event_create.html"
    
    def get_context_data(self, **kwargs):
        context = super(EventUpdate, self).get_context_data(**kwargs)
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            title = request.POST.get('title')
            picture = request.FILES.get('picture')
            
            start_event = request.POST.get('start_event')
            end_event = request.POST.get('end_event')
            
            description_es = request.POST.get('description_es')
            description_en = request.POST.get('description_en')
            description_pt = request.POST.get('description_pt')
            description_fr = request.POST.get('description_fr')
            description_it = request.POST.get('description_it')
            description_de = request.POST.get('description_de')
            description_zh_hant = request.POST.get('description_zh_hant')
            description_zh_hans = request.POST.get('description_zh_hans')
            description_jp = request.POST.get('description_jp')

            logo_id = self.kwargs.get('pk')
            event_update = Event.objects.get(id=logo_id)
            if picture is None:
                picture = event_update.picture
            
            event_update.title = title
            event_update.picture = picture
            event_update.start_event = start_event
            event_update.end_event = end_event

            event_update.description_es = description_es
            event_update.description_en = description_en
            event_update.description_pt = description_pt
            event_update.description_fr = description_fr
            event_update.description_it = description_it
            event_update.description_de = description_de
            event_update.description_zh_hant = description_zh_hant
            event_update.description_zh_hans = description_zh_hans
            event_update.description_jp = description_jp
            event_update.save()
            return HttpResponseRedirect('/EventList')
        else:
            return HttpResponseRedirect('/EventList')

def EventDelete(request):
    my_id = request.POST.get('value')
    companylogo = Event.objects.get(id=my_id)
    companylogo.delete()
    return HttpResponse('Ok')

@permission_required('usercustom.marketing_user')
def ActiveBannerIndex(request):
    if request.is_ajax:
        if request.method == 'POST':
            id = request.POST.get('active')
            active = BannerIndex.objects.get(pk=id)
            if active.activate == True:
                active.activate = False
            else:
                active.activate = True
            send = active.activate
            active.save()
            return HttpResponse(send)
    return HttpResponse('Error in request!')

def DeleteCampaign(request):
    my_id = request.POST.get('value')
    campaign = Campaign.objects.get(id=my_id)
    campaign.delete()
    return HttpResponse('Ok')

def DeleteMedMagazine(request):
    my_id = request.POST.get('value')
    MedMagazine = BannerIndex.objects.get(id=my_id)
    MedMagazine.delete()
    return HttpResponse('Ok')

"""class BannerCompany(LoginRequiredMixin, TemplateView):
    template_name = "crm/dashboard_admin/banner_company.html"""

#Module: Import CSV - Management
class ImportCSV(PermissionRequiredMixin, TemplateView):
    permission_required = 'usercustom.management_user'
    template_name = "crm/dashboard_admin/import_csv.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            extension=''
            existenCSV = CsvArchivo.objects.all().count()
            if(existenCSV > 0):
                CsvArchivo.objects.get().delete()
            filename = str(request.FILES['csv'])
            separador= request.POST.get('separador')
            if separador!=';' and separador!=',':
                print('error en separador')
                actual_lang = translation.get_language()
                if actual_lang=='es':
                    messages.error(request, 'Separador solo admite , ó ;')
                if actual_lang=='zh-hant':
                    messages.error(request, '分隔符僅支持，或;')
                if actual_lang=='de':
                    messages.error(request, 'Trennzeichen unterstützt nur , oder ;')
                if actual_lang=='en':
                    messages.error(request, 'Separator only supports , or ;')
                if actual_lang=='fr':
                    messages.error(request, 'Le séparateur ne prend en charge que , ou ;')
                if actual_lang=='it':
                    messages.error(request, 'Il separatore supporta solo , o ;')
                if actual_lang=='pt':
                    messages.error(request, 'O separador suporta apenas , ou ;')
                if actual_lang=='zh-hans':
                    messages.error(request, '分隔符仅支持，或;')
                if actual_lang=='ja':
                    messages.error(request, '区切り文字は、「、」または「;」のみをサポートします')
                return HttpResponseRedirect(reverse_lazy('Import_CSV'))

            modelo= request.POST.get('modelo')
            print(modelo)
            if filename.endswith('.csv'):
                extension = 'csv'
            if extension != 'csv':
                actual_lang = translation.get_language()
                if actual_lang=='es':
                    messages.error(request, 'Formato incorrecto. Sólo se admite archivos CSV.')
                if actual_lang=='zh-hant': #tradicional
                    messages.error(request, '格式錯誤僅支持CSV文件')
                if actual_lang=='de':
                    messages.error(request, 'Falsches Format Es werden nur CSV-Dateien unterstützt')
                if actual_lang=='en':
                    messages.error(request, 'Incorrect format. Only CSV files are supported.')
                if actual_lang=='fr':
                    messages.error(request, 'Format incorrect Seuls les fichiers CSV sont pris en charge')
                if actual_lang=='it':
                    messages.error(request, 'Formato errato Sono supportati solo file CSV')
                if actual_lang=='pt':
                    messages.error(request, 'Formato incorreto Somente arquivos CSV são suportados')
                if actual_lang=='zh-hans':
                    messages.error(request, '格式错误仅支持CSV文件')
                if actual_lang=='ja':
                    messages.error(request, '不正な形式CSVファイルのみがサポートされています')
                return HttpResponseRedirect(reverse_lazy('Import_CSV'))

            objeto = CsvArchivo(
                name = request.FILES['csv'],
                file = request.FILES.get('csv')
                )
            objeto.save()

            archivo = CsvArchivo.objects.get()
            ruta= archivo.file
            path= "medcombo/media/" + str(ruta)

            if(modelo == 'Productos'):
                with open (path) as f:
                    reader= csv.reader(f, delimiter= separador)
                    for row in reader:
                        elemento= row

                        longitud_csv = len(elemento) #aqui veo cuantos campos trae el archivo (keywords)
                        total_keywords = longitud_csv - 7   #10 es el numero de datos estandar
                        languageInstance= LanguageCampaign.objects.get(name_language=elemento[5])

                        areaInstance= Area.objects.get(name=elemento[2], language=languageInstance.pk)

                        if elemento[3] == None or elemento[3] == '':
                            categoryInstance = None
                        else:
                            categoryInstance= Category.objects.get(name=elemento[3], language=languageInstance.pk)

                        if elemento[4] == None or elemento[4] == '':
                            print('esto')
                            subcategoryInstance = None
                            print(subcategoryInstance)
                        else:
                            print('aquii')
                            subcategoryInstance= SubCategory.objects.get(name=elemento[4], language=languageInstance.pk)
                            print(subcategoryInstance)
                        companyInstance= Company.objects.get(name=elemento[6])
                        producto = Product(
                        name= elemento[0],
                        description=elemento[1],
                        area= areaInstance,
                        category= categoryInstance,
                        subcategory= subcategoryInstance,
                        company= companyInstance,
                        language= languageInstance,
                        approved= True,
                        notify= False,
                        )
                        producto.save()
                        productInstance= Product.objects.get(id= producto.pk)
                        i= 0
                        while i < total_keywords:
                            keyword_name = elemento[7 + i]
                            if(keyword_name == ''):
                                print('keyword en blanco')
                            else:
                                keywordQuery= Keyword.objects.filter(name= keyword_name, language= languageInstance.pk).first()
                                keywordInstance = Keyword.objects.get(id= keywordQuery.pk)
                                productInstance.keyword.add(keywordInstance)
                            i = i + 1
                    print('productos importados')
                    return HttpResponseRedirect(reverse_lazy('Import_CSV'))
            elif(modelo == 'Usuarios'):
                with open (path) as f:
                    reader= csv.reader(f, delimiter= separador)
                    for row in reader: 
                        user_new = User.objects.filter(lead=False).filter(employee=False)
                        my_list = []
                        if user_new.count() == 0:
                            print('este menos')
                            username = 10000
                        else:
                            for user in user_new:
                                value = str(user.username).isdigit()
                                print(value)
                                if value == True:
                                    my_list.append(int(user.username))
                                order = sorted(my_list, key=int, reverse=True)
                                print(order)
                                if order:
                                    print('aqui')
                                    username = order[0] + 1
                                else:
                                    print('por aqui no deberia ser')
                                    username = 10000
                        print(username)   
                        elemento = row
                        #random_username = get_random_string(length=8)
                        languageInstance= LanguageCampaign.objects.get(name_language=elemento[0])
                        workInstance= Work.objects.get(name=elemento[6], language= languageInstance.pk)
                        companyInstance= Company.objects.get(name=elemento[7])
                        print(companyInstance)
                        countryInstance= Country.objects.get(name=elemento[4])
                        #123medcombo clave por defecto
                        crearUsuario = User(
                            password= 'pbkdf2_sha256$100000$8uPQuUkzqmw7$fMm/sEgvKwpPCt8fMVdG3s5xU+PTiwNOyP4GItjIgzk=',
                            username= username,
                            first_name=elemento[1],
                            last_name=elemento[2],
                            email= elemento[3],
                            country= countryInstance,
                            telephone=elemento[5],
                            work= workInstance,
                            lead= False,
                            employee= False,
                            company= companyInstance,
                            )
                        crearUsuario.save()
                    print('usuarios importados')  
                    return HttpResponseRedirect(reverse_lazy('admin_user_sales'))
            elif(modelo == 'Contactos'):
                with open (path) as f:
                    reader= csv.reader(f, delimiter= separador)
                    for row in reader:        
                        elemento = row


                        #crear la empresa **********************************************************
                        if elemento[9] == None or elemento[9] == '':
                            countryInstance= None
                        else:
                            countryInstance= Country.objects.get(name=elemento[9])

                        if elemento[10] == None or elemento[10] == '':
                            cityInstance= None
                        else:
                            cityInstance= City.objects.get(name=elemento[10])
                        if elemento[11]== None or elemento[11]=='':
                            codigo=None
                        else:
                            codigo=elemento[11]
                        if elemento[12]== None or elemento[12]=='':
                            web=''
                        else:
                            web=elemento[12]
                        print(web)
                        crearEmpresa= Company(
                            name=elemento[7],
                            address=elemento[8],
                            country_company=countryInstance,
                            city_company=cityInstance,
                            code_postal=codigo,
                            web=web,
                            approved=False,
                            notify=False,
                            )
                        crearEmpresa.save()
                        #fin crear la empresa ******************************************************


                        languageInstance= LanguageCampaign.objects.get(name_language=elemento[0])
                        workInstance= Work.objects.get(name=elemento[6], language= languageInstance.pk)
                        countryInstance= Country.objects.get(name=elemento[4])
                        companyInstance= Company.objects.get(pk=crearEmpresa.pk)
                        print(companyInstance)
                        crearUsuario = User(
                            username= elemento[3],
                            first_name=elemento[1],
                            last_name=elemento[2],
                            email= elemento[3],
                            country= countryInstance,
                            telephone=elemento[5],
                            work= workInstance,
                            lead= True,
                            employee= False,
                            company= companyInstance
                            )
                        crearUsuario.save()
                    print('contactos importados')
                    return HttpResponseRedirect(reverse_lazy('ListContacCrm'))
            return HttpResponseRedirect(reverse_lazy('Import_CSV'))
        else:
            return HttpResponseRedirect(reverse_lazy('Import_CSV'))

def Sponsor_delete(request):
    my_id = request.POST.get('value')
    sponsor = Sponsor.objects.filter(id=my_id)
    sponsor.delete()
    return HttpResponse('Ok')
