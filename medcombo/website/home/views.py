from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from medcombo.product.models import Area, Category, SubCategory, Keyword, PolicyPrivacyModel, Sponsor,Product
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import translation
from medcombo.crm.dashboard_admin.models import BannerIndex
from cities_light.models import Country
from django.core.mail import send_mail
from cities_light.models import Country
from datetime import date
from medcombo.product.models import FavoriteProduct

from medcombo.crm.dashboard_admin.models import Event

from medcombo.configuration.company.models import Company

class Home(TemplateView):
    template_name = "website/home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Column1= []
        Column2= []
        Column3= []
        actual_lang = translation.get_language()
        print(actual_lang)
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
        misareas = Area.objects.filter(language_id=idlang, active=True)
        # totalAreas = misareas.count()
        # areasPorColumna= totalAreas/3
        columna = 1
        for area in misareas:
            if columna == 1:
                Column1.append(area)

            if columna == 2:
                Column2.append(area)
            if columna == 3:
                Column3.append(area)
            columna = columna + 1
            if columna == 4:
                columna = 1
        context["events"] = Event.objects.order_by("-end_event", "-start_event")
        
        context['area1'] = Column1
        context['area2'] = Column2
        context['area3'] = Column3
        
        return context
        
class About(TemplateView):
    template_name = "website/home/aboutme.html"

class Prices(TemplateView):
    template_name = "website/home/prices.html"

class Sitemap(TemplateView):
    template_name = "website/home/sitemap.html"

    def get_context_data(self, **kwargs):
        context = super(Sitemap, self).get_context_data(**kwargs)
        language_select_act = translation.get_language()
        areas = Area.objects.filter(active=True,language__value_language=language_select_act)

        for area in areas:
            categories = Category.objects.filter(active=True, relationship=area)
            for cate in categories:
                subcates = SubCategory.objects.filter(active=True, relationship=cate)
                for sub in subcates:
                    keys = Keyword.objects.filter(area=area, category=cate, subcategory=sub)
                    sub.child_keywords = keys
                cate.child_subcategories = subcates
            area.child_categories = categories

        companies = Company.objects.filter(approved=True)
        context["events"] = Event.objects.order_by("-end_event", "-start_event")

        context['areas'] = areas
        context['companies'] = companies
        
        return context
# class KeywordSubCategory(ListView):
#     template_name = "website/home/SubCategories_Keywords_Index.html"
#     #template_name = "website/home/respaldotemporal.html"
    

def CategoriesArea(request, my_category_area):
    #el metodo get carga el area, categoria y subcategoria, keywords seleccionados
    Column1= []
    Column2= []
    Column3= []
    my_area_temp = my_category_area

    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 4
    elif actual_lang == 'de':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 3
    elif actual_lang == 'fr':
        idlang = 5
    elif actual_lang == 'it':
        idlang = 6
    elif actual_lang == 'pt':
        idlang = 7
    elif actual_lang == 'zh-hans':
        idlang = 8
    elif actual_lang == 'ja':
        idlang = 9
    elif actual_lang == 'zh-hant':
        idlang = 1
    
    area_array = []
    area_array.append(my_area_temp)
    for i in area_array:
        my_area = str(i).replace("-", " ")
    
    miarea= Area.objects.filter(language_id=idlang, name=my_area, active= True)
    if miarea:
        areaGet= Area.objects.get(language_id=idlang, name=my_area, active= True)
        area=areaGet.pk

    else:
        areaGet= None
        area=None

    mycategories = Category.objects.filter(relationship=area, language_id=idlang, active=True)
    totalcategories= mycategories.count()
    columna = 1
    for cat in mycategories:
        if columna == 1:
            Column1.append(cat)

        if columna == 2:
            Column2.append(cat)

        if columna == 3:
            Column3.append(cat)

        columna = columna + 1

        if columna == 4:
            columna = 1
    if totalcategories == 0:
        print('el area no posee categorias...')
        #verifico si tiene keywords
        mikey = Keyword.objects.filter(area_id=area, language_id=idlang)
        totalkeys= mikey.count()

        if totalkeys == 0:
            print('el area tampoco posee keywords')

        else:
            columna = 1
            for key in mikey:
                if columna == 1:
                    Column1.append(key)

                if columna == 2:
                    Column2.append(key)

                if columna == 3:
                    Column3.append(key)

                columna = columna + 1

                if columna == 4:
                    columna = 1

    favoritos = FavoriteProduct.objects.all().filter(user_id= request.user.id)
    ##productos premium(patrocinados)
    fecha= date.today()
    lista_patrocinados_vigentes = []
    patrocinados= Sponsor.objects.filter(active=True)
    for sponsor in patrocinados:
            pk= sponsor.pk
            inicio= sponsor.start
            fin= sponsor.end
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                myproduct= Product.objects.filter(pk= producto_pk, area= area, approved= True).order_by('-algorithmic_value').count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    misponsor = Sponsor.objects.filter(pk=pk)
                    lista_patrocinados_vigentes.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()
    return render(request, 'website/home/Area_Categories_Index.html', 
        {'area': miarea, 
        'areapk': area,
        'category1': Column1, 
        'category2': Column2, 
        'category3': Column3,
        'patrocinados': lista_patrocinados_vigentes,
        'favoritos': favoritos})


class PrivacyPolicy(ListView):
    template_name = "website/home/privacy_policy.html"
    model= PolicyPrivacyModel

class FAQ(TemplateView):
    template_name = "website/home/FAQ.html"

class Contacto(TemplateView):
    template_name = "website/home/contact_base.html"
    model = Country

    def get_context_data(self, **kwargs):
        context = super(Contacto, self).get_context_data(**kwargs)
        countrys = Country.objects.all()
        context['countrys'] = countrys
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            pais = request.POST.get('pais')
            email = request.POST.get('email')
            contenido = request.POST.get('contenido')
            pais_get= Country.objects.get(pk=pais)
            print("mail check!", contenido, email)
            send_mail(name+'-'+pais_get.name,
            contenido,
            email,
            ['contacto@medcombo.es', 'dmabdeveloper@gmail.com'],
            fail_silently= False,
            )
            return redirect('home')

class ContactoPrice(TemplateView):
    template_name = "website/home/contact_base.html"
    model = Country

    def get_context_data(self, **kwargs):
        context = super(ContactoPrice, self).get_context_data(**kwargs)
        price_order = self.kwargs.get('pk')
        countrys = Country.objects.all()
        context['countrys'] = countrys
        context['price_list'] = price_order
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            pais = request.POST.get('pais')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            contenido = request.POST.get('contenido')
            pais_get= Country.objects.get(pk=pais)
            send_mail(subject + "(" + name + '-' + pais_get.name +")",
            contenido,
            email,
            ['contacto@medcombo.es'],
            fail_silently= True,
            )
            return redirect('home')


class ListNews(ListView):
    template_name = 'website/home/list_news.html'
    model = BannerIndex
    ordering = ['order_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_select_act = translation.get_language()
        banner_list = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).order_by('-order_created')
        context['banner_list'] = banner_list
        return context


class DetailNews(DetailView):
    template_name = 'website/home/detail_news.html'
    model = BannerIndex 
    ordering = ['order_created']
    
    def get_context_data(self, **kwargs):
        bannerindex = BannerIndex.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        consult_banner = BannerIndex.objects.filter(id=bannerindex.pk)
        language_select_act = translation.get_language()
        foot_banner = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).order_by('-order_created').exclude(pk=self.kwargs.get('pk'))
        foot_banner_count = BannerIndex.objects.filter(activate=True,language__value_language=language_select_act).exclude(pk=self.kwargs.get('pk')).count()
        context['consult_banner'] = consult_banner
        context['foot_detail_banner'] = foot_banner
        context['count_detail_banner'] = foot_banner_count
        return context

# List event modlue
class ListEvents(ListView):
    template_name = 'website/home/list_events.html'
    model = Event
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_select_act = translation.get_language()
        event_list = Event.objects.order_by("-end_event", "-start_event")
        context['event_list'] = event_list
        return context


class DetailEvent(DetailView):
    template_name = 'website/home/detail_event.html'
    model = Event 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_event = Event.objects.get(pk=self.kwargs.get('pk'))
        extra_events = Event.objects.order_by("-end_event", "-start_event").exclude(pk=self.kwargs.get('pk'))
        context['current_event'] = current_event
        context['extra_events'] = extra_events
        return context

def KeywordSubCategoryNew(request, my_area_keyword, my_category_keyword, my_subcategory_keyword):
    #el metodo get carga el area, categoria y subcategoria, keywords seleccionados
    Column1= []
    Column2= []
    Column3= []
    my_area_temp = my_area_keyword
    my_category_temp = my_category_keyword
    my_subcategory_temp = my_subcategory_keyword
    # my_area = my_area_keyword
    # my_category = my_category_keyword
    # my_subcategory = my_subcategory_keyword
    area_array = []
    area_array.append(my_area_temp)
    for i in area_array:
        my_area = str(i).replace("-", " ")

    category_array = []
    category_array.append(my_category_temp)
    for i in category_array:
        my_category = str(i).replace("-", " ")

    subcategory_array = []
    subcategory_array.append(my_subcategory_temp)
    for i in subcategory_array:
        my_subcategory = str(i).replace("-", " ")

    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 4
    elif actual_lang == 'de':
            idlang = 2
    elif actual_lang == 'en':
        idlang = 3
    elif actual_lang == 'fr':
        idlang = 5
    elif actual_lang == 'it':
        idlang = 6
    elif actual_lang == 'pt':
        idlang = 7
    elif actual_lang == 'zh-hans':
        idlang = 8
    elif actual_lang == 'ja':
        idlang = 9
    elif actual_lang == 'zh-hant':
        idlang = 1
    
    miarea= Area.objects.filter(language_id=idlang, name=my_area, active= True)
    if miarea:
        areaGet= Area.objects.get(language_id=idlang, name=my_area, active=True)
        area=areaGet.pk
    else:
        areaGet = None
        area = None

    micategoria= Category.objects.filter(language_id=idlang, name=my_category, active=True)
    if micategoria:
        categoryGet= Category.objects.get(language_id=idlang, name=my_category, active=True)
        category=categoryGet.pk
    else:
        categoryGet=None
        category=None

    misubcategoria= SubCategory.objects.filter(language_id=idlang, name=my_subcategory, active=True)
    if misubcategoria:
        subcategoryGet= SubCategory.objects.get(language_id=idlang, name=my_subcategory, active=True)
        subcategory=subcategoryGet.pk
    else:
        subcategoryGet=None
        subcategory=None

    mikey = Keyword.objects.filter(subcategory_id=subcategory, category_id=category, area_id=area, language_id=idlang)
    totalkeys= mikey.count()
    columna = 1
    for key in mikey:
        if columna == 1:
            Column1.append(key)

        if columna == 2:
            Column2.append(key)

        if columna == 3:
            Column3.append(key)

        columna = columna + 1

        if columna == 4:
            columna = 1
    if totalkeys == 0:
            print('la subcategoria no posee keywords')

    favoritos = FavoriteProduct.objects.all().filter(user_id= request.user.id)
    ##productos premium(patrocinados)
    fecha= date.today()
    lista_patrocinados_vigentes = []
    patrocinados= Sponsor.objects.filter(active=True)
    for sponsor in patrocinados:
            pk= sponsor.pk
            inicio= sponsor.start
            fin= sponsor.end
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                myproduct= Product.objects.filter(pk= producto_pk, area= area, category= category, subcategory=subcategory, approved= True).order_by('-algorithmic_value').count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    misponsor = Sponsor.objects.filter(pk=pk)
                    lista_patrocinados_vigentes.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()
    return render(request, 'website/home/SubCategories_Keywords_Index.html', 
        {'area': miarea, 
        'favoritos': favoritos,
        'category': micategoria, 
        'subcategory': misubcategoria, 
        'keyword1': Column1, 
        'keyword2': Column2, 
        'keyword3': Column3,
        'patrocinados': lista_patrocinados_vigentes})


def SubcategoriesCategoryNew(request, my_area_subcategory, my_category_subcategory):
    Column1= []
    Column2= []
    Column3= []
    
    my_area_temp = my_area_subcategory
    my_category_temp = my_category_subcategory
    
    area_array = []
    area_array.append(my_area_temp)
    for i in area_array:
        my_area = str(i).replace("-", " ")

    category_array = []
    category_array.append(my_category_temp)
    for i in category_array:
        my_category = str(i).replace("-", " ")
    
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 4
    elif actual_lang == 'de':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 3
    elif actual_lang == 'fr':
        idlang = 5
    elif actual_lang == 'it':
        idlang = 6
    elif actual_lang == 'pt':
        idlang = 7
    elif actual_lang == 'zh-hans':
        idlang = 8
    elif actual_lang == 'ja':
        idlang = 9
    elif actual_lang == 'zh-hant':
        idlang = 1
    
    miarea= Area.objects.filter(language_id=idlang, name=my_area, active= True)
    if miarea:
        areaGet= Area.objects.get(language_id=idlang, name=my_area, active= True)
        area=areaGet.pk
    else:
        areaGet = None
        area = None
    
    micategoria= Category.objects.filter(language_id=idlang, name=my_category, active= True)
    if micategoria:
        categoryGet= Category.objects.get(language_id=idlang, name=my_category, active= True)
        category=categoryGet.pk
        
    else:
        categoryGet=None
        category=None
    
    myscategories = SubCategory.objects.filter(relationship=category, language_id=idlang, active=True)
    totalscategories= myscategories.count()
    print(totalscategories)
    columna = 1
    for cat in myscategories:
        if columna == 1:
            Column1.append(cat)

        if columna == 2:
            Column2.append(cat)

        if columna == 3:
            Column3.append(cat)

        columna = columna + 1

        if columna == 4:
            columna = 1
    if totalscategories == 0:
        print('la categoria no posee subcategorias...')
        #verifico si tiene keywords
        mikey = Keyword.objects.filter(category_id=category, area_id=area, language_id=idlang)
        totalkeys= mikey.count()

        if totalkeys == 0:
            print('la categoria tampoco posee keywords')
        else:
            columna = 1
            for key in mikey:
                if columna == 1:
                    Column1.append(key)

                if columna == 2:
                    Column2.append(key)

                if columna == 3:
                    Column3.append(key)

                columna = columna + 1

                if columna == 4:
                    columna = 1

    favoritos = FavoriteProduct.objects.all().filter(user_id= request.user.id)
    ##productos premium(patrocinados)
    fecha= date.today()
    lista_patrocinados_vigentes = []
    patrocinados= Sponsor.objects.filter(active=True)
    for sponsor in patrocinados:
            pk= sponsor.pk
            inicio= sponsor.start
            fin= sponsor.end
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                myproduct= Product.objects.filter(pk= producto_pk, area= area, category= category, approved= True).order_by('-algorithmic_value').count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    misponsor = Sponsor.objects.filter(pk=pk)
                    lista_patrocinados_vigentes.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()
    return render(request, 'website/home/Category_Subcategories_Index.html', 
        {'area': miarea, 
        'areapk': area,
        'categorypk': category,
        'categoria': micategoria,
        'scategory1': Column1, 
        'scategory2': Column2, 
        'scategory3': Column3,
        'totalscategories': totalscategories,
        'patrocinados': lista_patrocinados_vigentes,
        'favoritos': favoritos})
