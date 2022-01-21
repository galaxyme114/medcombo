from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from dal import autocomplete
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from .models import Product, AdminProduct, Keyword, SynonymKeyword, Sponsor
from .models import RatingProduct
from .models import BoostingProduct
from .models import Category
from .models import SubCategory
from .models import BannerWeb
from .models import Searchkey_static
from .models import Click_static
from medcombo.configuration.usercustom.models import User
from medcombo.configuration.company.models import Company
from django.utils.html import format_html
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from medcombo.myweb.dashboard_client.post.models import Post
from cities_light.models import Country, City
from medcombo.product.models import FavoriteProduct
from medcombo.product.forms import BannerWebForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import date
from django.utils import translation

from medcombo.crm.dashboard_admin.models import LanguageCampaign
from medcombo.configuration.company.models import DescriptionCompany

class ListProduct(ListView):
    template_name = 'product/list.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favoritos = FavoriteProduct.objects.all().filter(user_id= self.request.user.id)
        context['favoritos'] = favoritos
        print('mis favoritos')
        print(favoritos)
        return context

class ProductsSearchData(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Keyword.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

    def get_result_value(self, result):
        return str(result.name)

def SearchProduct(request):
   q = request.POST.get('name','')
   #a = Product.objects.filter(keyword__name__icontains=q)
   product = Product.objects.filter(keyword__name=q).order_by('-algorithmic_value').filter(company__country_company='69')
   product_another = Product.objects.filter(keyword__name=q).order_by('-algorithmic_value').exclude(company__country_company='69')
   return render(request, 'product/list.html', {'product': product, 'product_another': product_another})

def ProductCountry(request):
    my_timezone = request.POST.get('timezone')
    city = City.objects.filter(timezone=str(my_timezone))
    if city:
        value = Country.objects.get(id=city[0].country.id)
        return HttpResponse(value.code3)
    else:
        return HttpResponse('ESP')

def ProductCountryTwo(request):
    my_timezone = request.POST.get('timezone')
    city = City.objects.filter(timezone=str(my_timezone))
    if city:
        value = Country.objects.get(id=city[0].country.id)
        return HttpResponse(value.code3)
    else:
        return HttpResponse('ESP')
    
def NewSearchProduct(request, lang, country, product, area, category, subcategory, keyword):
    favoritos = FavoriteProduct.objects.all().filter(user_id= request.user.id)
    actual_languague_p = translation.get_language()
    fecha= date.today()
    lista_patrocinados_vigentes = []
    q_var= request.POST.get('id_name','')
    q = q_var
    print(q_var)
    #buscar sinonimos 23/01 jose
    existe_syn= SynonymKeyword.objects.filter(name__iexact=q)
    if(existe_syn):
        existe_syn= SynonymKeyword.objects.get(name__iexact=q)
        idkeyword_syn= existe_syn.keyword_id
        mykeyword_syn=Keyword.objects.get(pk=idkeyword_syn)
        q= mykeyword_syn.name
    #fin de buscar sinonimos 23/01 jose

    #*************************Searchkey save *******************************
    print("############", request.user, "###########")
    search_user = request.user
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    elif request.META.get('HTTP_X_REAL_IP'):
        ip_address = request.META.get('HTTP_X_REAL_IP')
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    searchkey_static = Searchkey_static()
    searchkey_static.searchkey_name = q
    if search_user.is_authenticated:
        searchkey_static.user = search_user
    searchkey_static.ip_address = ip_address
    searchkey_static.language = LanguageCampaign.objects.get(value_language=actual_languague_p)
    searchkey_static.save()


    my_key = keyword.replace ("-", " ")
    #********************** agregado para breadscrumb ******************
    if(q==None or q==''):
        q=my_key
    #********************** agregado para breadscrumb ******************
    my_location = Country.objects.get(code3=country.upper())
    key = Keyword.objects.filter(name__iexact=my_key)
    another_administrados=[]
    patrocinados_administrados=[]
    product_administrados= []
    if key:
        keypicture = key[0].image
        descriptionkey= key[0].description
        namekey= key[0].name
    else:
        keypicture = None
        descriptionkey = ""
        namekey=q
    patrocinados= Sponsor.objects.filter(active=True, lateral=True)
    patrocinados_two= Sponsor.objects.filter(active=True, lateral=False)
    patrocinados_country = []
    patrocinados_other = []
    if key:
        keyword_url = key[0].name
    else:
        keyword_url = q
    if q:
        # 69 es el id de españa en la lista de paises
        for sponsor in patrocinados:
            pk= sponsor.pk
            #print(sponsor.product.name)
            inicio= sponsor.start
            fin= sponsor.end
            #Sponsor lateral
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                #myproduct= Product.objects.filter(pk= producto_pk, keyword__name__icontains=q, approved= True).order_by('-algorithmic_value').exclude(company__country_company=my_location.id).count()
                myproduct= Product.objects.filter(pk= producto_pk, keyword__name__icontains=q, approved= True).order_by('-algorithmic_value').count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    misponsor = Sponsor.objects.filter(pk=pk)
                    lista_patrocinados_vigentes.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()
        #Sponsor country
        for sponsor in patrocinados_two:
            pk= sponsor.pk
            #print(sponsor.product.name)
            inicio= sponsor.start
            fin= sponsor.end
            #Sponsor lateral
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                #myproduct= Product.objects.filter(pk= producto_pk, keyword__name__icontains=q, approved= True).order_by('-algorithmic_value').exclude(company__country_company=my_location.id).count()
                myproduct= Product.objects.filter(pk= producto_pk, keyword__name__icontains=q, approved= True).order_by('-algorithmic_value').filter(company__country_company=my_location.id).count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    misponsor = Sponsor.objects.filter(pk=pk)
                    patrocinados_country.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()
        #Sponsor other
        for sponsor in patrocinados_two:
            pk= sponsor.pk
            #print(sponsor.product.name)
            inicio= sponsor.start
            fin= sponsor.end
            #Sponsor lateral
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                #myproduct= Product.objects.filter(pk= producto_pk, keyword__name__icontains=q, approved= True).order_by('-algorithmic_value').exclude(company__country_company=my_location.id).count()
                myproduct= Product.objects.filter(pk= producto_pk, keyword__name__icontains=q, approved= True).order_by('-algorithmic_value').exclude(company__country_company=my_location.id).count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    misponsor = Sponsor.objects.filter(pk=pk)
                    patrocinados_other.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()
        product = Product.objects.filter(keyword__name__icontains=q, approved= True,language__value_language=actual_languague_p).order_by('-algorithmic_value').filter(company__country_company=my_location.id)
        product= set(product) #elimina resultados repetidos en una lista
        for other in product:
            administrados= AdminProduct.objects.filter(product=other.pk, keyword__name__icontains=keyword_url).count()
            if administrados != 0:
                producto= Product.objects.filter(pk= other.pk)
                product_administrados.extend(producto)
        product_another = Product.objects.filter(keyword__name__icontains=q, approved=True,language__value_language=actual_languague_p).order_by('-algorithmic_value').exclude(company__country_company=my_location.id)
        product_another= set(product_another) #elimina resultados repetidos en una lista
        for other in product_another:
            administrados= AdminProduct.objects.filter(product=other.pk, keyword__name__icontains=keyword_url).count()
            if administrados != 0:
                produc= Product.objects.filter(pk= other.pk)
                another_administrados.extend(produc)
    else:
        for sponsor in patrocinados:
            pk= sponsor.pk
            inicio= sponsor.start
            fin= sponsor.end
            if str(inicio) <= str(fecha) and str(fin) >= str(fecha):#si la fecha esta vigente, verifico si el producto coincide
                print('fecha vigente') #si la fecha es vigente, verifico si el producto cumple las condiciones de la busqueda
                if sponsor.product:
                    producto_pk= sponsor.product.pk
                else:
                    producto_pk = None
                myproduct= Product.objects.filter(pk= producto_pk, keyword__name__iexact=keyword_url, approved= True).order_by('-algorithmic_value').exclude(company__country_company=my_location.id).count()
                if(myproduct == 0):#no existen coincidencias y no lo agrego
                    print('producto no coincide')
                else:
                    print('producto coincide')
                    misponsor = Sponsor.objects.filter(pk=pk)
                    lista_patrocinados_vigentes.extend(misponsor)
            else:#si la fecha no esta vigente, le cambio el active=false
                misponsor= Sponsor.objects.get(pk=pk)
                misponsor.active = False
                misponsor.save()

        product = Product.objects.filter(keyword__name__iexact=keyword_url, approved= True, language__value_language=actual_languague_p).order_by('-algorithmic_value').filter(company__country_company=my_location.id)
        for other in product:
            administrados= AdminProduct.objects.filter(product=other.pk, keyword__name__iexact=keyword_url).count()
            if administrados != 0:
                producto= Product.objects.filter(pk= other.pk)
                product_administrados.extend(producto)

        product_another = Product.objects.filter(keyword__name__iexact=keyword_url, approved= True, language__value_language=actual_languague_p).order_by('-algorithmic_value').exclude(company__country_company=my_location.id)
        for other in product_another:
            administrados= AdminProduct.objects.filter(product=other.pk, keyword__name__iexact=keyword_url).count()
            if administrados != 0:
                produc= Product.objects.filter(pk= other.pk)
                another_administrados.extend(produc)
    #a = Product.objects.filter(keyword__name__icontains=q)
    #Condition new sponsors
    new_products = []
    new_sponsors = []
    new_products_other = []
    new_sponsors_other = []
    for new in product_administrados:
        sponsor = Sponsor.objects.filter(product=new.pk)
        if not sponsor:
            my_product = Product.objects.filter(id=new.pk)
            new_products.extend(my_product)
    for spon in patrocinados_country:
        sponsor_for = Product.objects.filter(id=spon.product.id)
        new_sponsors.extend(sponsor_for)
    #Another sponsors
    for another in another_administrados:
        sponsor = Sponsor.objects.filter(product=another.pk)
        if not sponsor:
            my_product = Product.objects.filter(id=another.pk)
            new_products_other.extend(my_product)
    for spon in patrocinados_other:
        sponsor_for = Product.objects.filter(id=spon.product.id)
        new_sponsors_other.extend(sponsor_for)
    #results
    product_result = []
    product_result.extend(new_sponsors)
    product_result.extend(new_products)
    #---------
    product_result_other = []
    product_result_other.extend(new_sponsors_other)
    product_result_other.extend(new_products_other)
    #results number
    number_products = len(product_result) + len(product_result_other) + len(set(lista_patrocinados_vigentes))
    #return
    namekey= q_var #agregada 23/01 para cambiar la variable en la pantalla en caso de ser un sinonimo
    return render(request, 'product/list.html', { 'favoritos': favoritos, 'product': product_result, 'product_another': product_result_other, 'sponsor_icon': new_sponsors, 'sponsor_icon_other': new_sponsors_other, 'keyword': descriptionkey, 'namekeyword': namekey, 'patrocinados': set(lista_patrocinados_vigentes), 'totalproducts':number_products,'searchkey': q_var, 'keypicture': keypicture})

def searcharea(request, pk):
   product = Product.objects.filter(area=pk)
   return render(request, 'product/list.html', {'product': product})

def searchcategory(request, pk):
   product = Product.objects.filter(category=pk)
   return render(request, 'product/list.html', {'product': product})

def searchsubcategory(request, pk):
   product = Product.objects.filter(subcategory=pk)
   return render(request, 'product/list.html', {'product': product})

class DetailProduct(DetailView):
    template_name = 'product/detail.html'
    model = Product 

    def get_context_data(self, **kwargs):
        registro = Product.objects.get(pk=self.kwargs.get('pk'))
        aa = registro.company.web

        #****************** click event ******************
        click_static = Click_static()
        click_static.product_name = registro.name
        click_static.save()

        context = super().get_context_data(**kwargs)
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
        produc_id = Product.objects.filter(pk=self.kwargs.get('pk'))
        if produc_id:
            produc = Product.objects.get(pk=self.kwargs.get('pk'))
            context['descriptions'] = DescriptionCompany.objects.filter(company_id=produc.company_id, language_id=idlang)
        else:
            pass
        context['owner'] = User.objects.filter(company=registro.company.id)
        context['isfavorite'] = FavoriteProduct.objects.all().filter(product_id=self.kwargs.get('pk'), user_id= self.request.user.id)
        context['banner_search'] = BannerWeb.objects.filter(banner_company= registro.company.id, language_campaign= idlang )
        if aa[:4] =='http':
            context['web'] = registro.company.web
        else:
            context['web'] = 'http://' + registro.company.web
        if self.request.user.id:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            count_user_real = True
            my_value = 0
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if total % count_user == 0:
                my_value = total / count_user
            else:
                if type(total / count_user) == float:
                    my_value = int(total / count_user) + 0.5
                else:
                    my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            my_user = self.request.user.id
            user_active = User.objects.get(id=my_user)
            #Safe Average in Product-----
            product_active = Product.objects.get(id=registro.id)
            product_active.rating_average = my_value
            product_active.save()
            #Boosting to Rating
            boosting_in_product = BoostingProduct.objects.all().filter(product_boosting=registro.id)
            if boosting_in_product:
                if product_active.rating_average < 4:
                    if boosting_in_product[0].rating_boosting == 'added':
                        product_active.algorithmic_value -= 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'subtracted'
                        rat_save.save()
                else:
                    if boosting_in_product[0].rating_boosting == 'subtracted':
                        product_active.algorithmic_value += 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'added'
                        rat_save.save()
            else:
                if product_active.rating_average >= 4:
                    product_active.algorithmic_value += 10
                    product_active.save()
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='added')
                    object_rat.save()
                else:
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='subtracted')
                    object_rat.save()
            
            rating_to_user = RatingProduct.objects.filter(user_rating=user_active,product_rating=product_active)
            my_user_value = '0'
            for ra in rating_to_user:
                my_user_value = ra.value_rating
            context['rating_user'] = my_user_value
            
            return context
        else:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            my_value = 0
            count_user_real = True
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if total % count_user == 0:
                my_value = total / count_user
            else:
                if type(total / count_user) == float:
                    my_value = int(total / count_user) + 0.5
                else:
                    my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            
            return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            rating_product = request.POST.get('ratingPoints')
            #do not accept values ​​less than zero and greater than five
            if rating_product < '0':
                rating_product = 0
            elif rating_product > '5':
                rating_product = 5
            else:
                rating_product = rating_product
            id_product = Product.objects.get(id=request.POST.get('postID'))
            user_rating = User.objects.get(id=request.user.id)
            query_rating = RatingProduct.objects.filter(user_rating=user_rating,product_rating=id_product)
            my_product = 0
            #Editing
            if query_rating:
                for q in query_rating:
                    my_product = q.id
                rating_save = RatingProduct.objects.get(id=my_product)
                rating_save.value_rating = rating_product
                rating_save.save()
            #Creating
            else:
                object_rating = RatingProduct(user_rating=user_rating, product_rating=id_product, value_rating=rating_product)
                object_rating.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

class CreateCategories(LoginRequiredMixin, TemplateView):
    template_name = 'product/category/create.html'

class ListCategories(LoginRequiredMixin, TemplateView):
    template_name = 'product/category/list.html'

class CategoryAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        area = self.forwarded.get('area', None)
        qs = Category.objects.all()
        condition = None
        if area:
            result = qs.filter(relationship=area)
            condition = area
        else:
            result = ""
            condition = condition
        if self.q:
            result = qs.filter(name__istartswith=self.q, relationship=condition)
        return result

class SubCategoryAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        category = self.forwarded.get('category', None)
        qs = SubCategory.objects.all()
        condition = None
        if category:
            result = qs.filter(relationship=category)
            condition = category
        else:
            result = ""
            condition = condition
        if self.q:
            result = qs.filter(name__istartswith=self.q, relationship=condition)
        return result

class MywebDetailProduct(DetailView):
    template_name = 'myweb/public/detail_product2.html'
    model = Product
    
    def get_context_data(self, **kwargs):
        registro = Product.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['owner'] = User.objects.filter(company=registro.company.id)
        context['isfavorite'] = FavoriteProduct.objects.all().filter(product_id=self.kwargs.get('pk'), user_id= self.request.user.id)
        #context['favoritos'] = FavoriteProduct.objects.filter(product_id= pk)
        if self.request.user.id:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            count_user_real = True
            my_value = 0
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if total % count_user == 0:
                my_value = total / count_user
            else:
                if type(total / count_user) == float:
                    my_value = int(total / count_user) + 0.5
                else:
                    my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            my_user = self.request.user.id
            user_active = User.objects.get(id=my_user)
            #Safe Average in Product-----
            product_active = Product.objects.get(id=registro.id)
            product_active.rating_average = my_value
            product_active.save()
            #Boosting to Rating
            boosting_in_product = BoostingProduct.objects.all().filter(product_boosting=registro.id)
            if boosting_in_product:
                if product_active.rating_average < 4:
                    if boosting_in_product[0].rating_boosting == 'added':
                        product_active.algorithmic_value -= 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'subtracted'
                        rat_save.save()
                else:
                    if boosting_in_product[0].rating_boosting == 'subtracted':
                        product_active.algorithmic_value += 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'added'
                        rat_save.save()
            else:
                if product_active.rating_average >= 4:
                    product_active.algorithmic_value += 10
                    product_active.save()
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='added')
                    object_rat.save()
                else:
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='subtracted')
                    object_rat.save()
            #----------------------------
            #----------------------------
            rating_to_user = RatingProduct.objects.filter(user_rating=user_active,product_rating=product_active)
            my_user_value = '0'
            for ra in rating_to_user:
                my_user_value = ra.value_rating
            context['rating_user'] = my_user_value
            print(context)
            return context
        else:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            count_user_real = True
            my_value = 0
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if total % count_user == 0:
                my_value = total / count_user
            else:
                if type(total / count_user) == float:
                    my_value = int(total / count_user) + 0.5
                else:
                    my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            rating_product = request.POST.get('ratingPoints')
            #do not accept values ​​less than zero and greater than five
            if rating_product < '0':
                rating_product = 0
            elif rating_product > '5':
                rating_product = 5
            else:
                rating_product = rating_product
            id_product = Product.objects.get(id=request.POST.get('postID'))
            user_rating = User.objects.get(id=request.user.id)
            query_rating = RatingProduct.objects.filter(user_rating=user_rating,product_rating=id_product)
            my_product = 0
            #Editing
            if query_rating:
                for q in query_rating:
                    my_product = q.id
                rating_save = RatingProduct.objects.get(id=my_product)
                rating_save.value_rating = rating_product
                rating_save.save()
            #Creating
            else:
                object_rating = RatingProduct(user_rating=user_rating, product_rating=id_product, value_rating=rating_product)
                object_rating.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

class MywebProductDetailMenu(DetailView):
    template_name = 'myweb/public/detail_product2.html'
    model = Product

    def get_context_data(self, **kwargs):
        registro = Product.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
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
        banner = BannerWeb.objects.filter(banner_company=registro.company.id, language_campaign= idlang )
        context['banner'] = banner
        context['owner'] = User.objects.filter(company=registro.company.id)
        context['isfavorite'] = FavoriteProduct.objects.all().filter(product_id=self.kwargs.get('pk'), user_id= self.request.user.id)
        #context['favoritos'] = FavoriteProduct.objects.filter(product_id= pk)
        if self.request.user.id:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            count_user_real = True
            my_value = 0
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if total % count_user == 0:
                my_value = total / count_user
            else:
                if type(total / count_user) == float:
                    my_value = int(total / count_user) + 0.5
                else:
                    my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            my_user = self.request.user.id
            user_active = User.objects.get(id=my_user)
            #Safe Average in Product-----
            product_active = Product.objects.get(id=registro.id)
            product_active.rating_average = my_value
            product_active.save()
            #Boosting to Rating
            boosting_in_product = BoostingProduct.objects.all().filter(product_boosting=registro.id)
            if boosting_in_product:
                if product_active.rating_average < 4:
                    if boosting_in_product[0].rating_boosting == 'added':
                        product_active.algorithmic_value -= 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'subtracted'
                        rat_save.save()
                else:
                    if boosting_in_product[0].rating_boosting == 'subtracted':
                        product_active.algorithmic_value += 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'added'
                        rat_save.save()
            else:
                if product_active.rating_average >= 4:
                    product_active.algorithmic_value += 10
                    product_active.save()
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='added')
                    object_rat.save()
                else:
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='subtracted')
                    object_rat.save()
            #----------------------------
            #----------------------------
            rating_to_user = RatingProduct.objects.filter(user_rating=user_active,product_rating=product_active)
            my_user_value = '0'
            for ra in rating_to_user:
                my_user_value = ra.value_rating
            context['rating_user'] = my_user_value
            print(context)
            return context
        else:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            my_value = 0
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if total % count_user == 0:
                my_value = total / count_user
            else:
                if type(total / count_user) == float:
                    my_value = int(total / count_user) + 0.5
                else:
                    my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            rating_product = request.POST.get('ratingPoints')
            #do not accept values ​​less than zero and greater than five
            if rating_product < '0':
                rating_product = 0
            elif rating_product > '5':
                rating_product = 5
            else:
                rating_product = rating_product
            id_product = Product.objects.get(id=request.POST.get('postID'))
            user_rating = User.objects.get(id=request.user.id)
            query_rating = RatingProduct.objects.filter(user_rating=user_rating,product_rating=id_product)
            my_product = 0
            #Editing
            if query_rating:
                for q in query_rating:
                    my_product = q.id
                rating_save = RatingProduct.objects.get(id=my_product)
                rating_save.value_rating = rating_product
                rating_save.save()
            #Creating
            else:
                object_rating = RatingProduct(user_rating=user_rating, product_rating=id_product, value_rating=rating_product)
                object_rating.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

class MywebPostDetailMenu(DetailView):
    template_name = 'myweb/public/detail_post.html'
    model = Post

    def get_context_data(self, **kwargs):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        #favoritos = FavoriteProduct.objects.all().filter(user_id= self.request.user.id)
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
        cons = Post.objects.filter(company=post.company.id)
        banner = BannerWeb.objects.filter(banner_company= post.company.id, language_campaign= idlang )
        context['banner'] = banner
        return context

class ListFavorites(LoginRequiredMixin, ListView):
    template_name = 'product/my_favorite_product.html'
    model= FavoriteProduct

class BannerWebCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.marketing_user'
    form_class = BannerWebForm
    model = BannerWeb 
    template_name = "crm/dashboard_admin/banner_company.html"
    success_url = reverse_lazy('BannerList')

class BannerWebUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = BannerWeb
    form_class = BannerWebForm
    template_name = "crm/dashboard_admin/banner_company.html"
    success_url = reverse_lazy('BannerList')

class DetailProductFavorite(DetailView):
    template_name = 'product/detail_product_favoritos.html'
    model = Product 

    def get_context_data(self, **kwargs):
        registro = Product.objects.get(pk=self.kwargs.get('pk'))
        aa = registro.company.web
        context = super().get_context_data(**kwargs)
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
        context['owner'] = User.objects.filter(company=registro.company.id)
        context['isfavorite'] = FavoriteProduct.objects.all().filter(product_id=self.kwargs.get('pk'), user_id= self.request.user.id)
        context['banner_search'] = BannerWeb.objects.filter(banner_company= registro.company.id, language_campaign= idlang )
        if aa[:4] =='http':
            context['web'] = registro.company.web
        else:
            context['web'] = 'http://' + registro.company.web
        if self.request.user.id:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            count_user_real = True
            my_value = 0
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if type(total / count_user) == float:
                my_value = int(total / count_user) + 0.5
            else:
                my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            my_user = self.request.user.id
            user_active = User.objects.get(id=my_user)
            #Safe Average in Product-----
            product_active = Product.objects.get(id=registro.id)
            product_active.rating_average = my_value
            product_active.save()
            #Boosting to Rating
            boosting_in_product = BoostingProduct.objects.all().filter(product_boosting=registro.id)
            if boosting_in_product:
                if product_active.rating_average < 4:
                    if boosting_in_product[0].rating_boosting == 'added':
                        product_active.algorithmic_value -= 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'subtracted'
                        rat_save.save()
                else:
                    if boosting_in_product[0].rating_boosting == 'subtracted':
                        product_active.algorithmic_value += 10
                        product_active.save()
                        rat_save = BoostingProduct.objects.get(id=boosting_in_product[0].id)
                        rat_save.rating_boosting = 'added'
                        rat_save.save()
            else:
                if product_active.rating_average >= 4:
                    product_active.algorithmic_value += 10
                    product_active.save()
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='added')
                    object_rat.save()
                else:
                    product_act = Product.objects.get(id=registro.id)
                    object_rat = BoostingProduct(product_boosting=product_act, rating_boosting='subtracted')
                    object_rat.save()
            #----------------------------
            #----------------------------
            rating_to_user = RatingProduct.objects.filter(user_rating=user_active,product_rating=product_active)
            my_user_value = '0'
            for ra in rating_to_user:
                my_user_value = ra.value_rating
            context['rating_user'] = my_user_value
            print(context)
            return context
        else:
            rating_total = RatingProduct.objects.all().filter(product_rating=registro.id)
            total = 0
            count_user = 0
            my_value = 0
            count_user_real = True
            for r in rating_total:
                total += r.value_rating
                count_user += 1
            if count_user == 0:
                total = 0
                count_user = 1
                count_user_real = False
            if type(total / count_user) == float:
                my_value = int(total / count_user) + 0.5
            else:
                my_value = total / count_user
            context['rating_total'] = total
            if count_user_real == False:
                context['rating_users'] = 0
            else:
                context['rating_users'] = count_user
            context['rating_avr'] = total / count_user
            context['rating_product'] = my_value
            return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            rating_product = request.POST.get('ratingPoints')
            #do not accept values ​​less than zero and greater than five
            if rating_product < '0':
                rating_product = 0
            elif rating_product > '5':
                rating_product = 5
            else:
                rating_product = rating_product
            id_product = Product.objects.get(id=request.POST.get('postID'))
            user_rating = User.objects.get(id=request.user.id)
            query_rating = RatingProduct.objects.filter(user_rating=user_rating,product_rating=id_product)
            my_product = 0
            #Editing
            if query_rating:
                for q in query_rating:
                    my_product = q.id
                rating_save = RatingProduct.objects.get(id=my_product)
                rating_save.value_rating = rating_product
                rating_save.save()
            #Creating
            else:
                object_rating = RatingProduct(user_rating=user_rating, product_rating=id_product, value_rating=rating_product)
                object_rating.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

def DeleteNewbanner(request):
    my_id = request.POST.get('value')
    newbanner = BannerWeb.objects.get(id=my_id)
    newbanner.delete()
    return HttpResponse('Ok')

def ProductCompare(request):
    compare = request.POST.get('value')
    my_pro_id = request.POST.get('id')
    Pro_com = Product.objects.get(id=my_pro_id)
    Pro_com.compare = compare
    Pro_com.save()
    return HttpResponse('OK')