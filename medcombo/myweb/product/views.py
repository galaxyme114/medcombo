from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from medcombo.product.models import Product, AdminProduct, Keyword, SynonymKeyword, SuggestionKeyword, BoostingKeyword, Area, Category, SubCategory, Keyword
from medcombo.product.forms import CategoriesForm, CategoriesForm9
from medcombo.configuration.usercustom.models import User
from medcombo.configuration.company.models import Company
import json
from medcombo.crm.economic.models import Proposal_Commercial, Proposal_Product
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from medcombo.product.forms import CategoriesForm1, CategoriesForm2, CategoriesForm3, CategoriesForm5, CategoriesForm6
from medcombo.product.forms import CategoriesForm7, CategoriesForm8
from medcombo.product.models import CsvArchivo
import csv
from medcombo.crm.dashboard_admin.models import LanguageCampaign
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.utils import translation
import collections
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from decimal import Decimal 
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class MywebProductAdminList(LoginRequiredMixin, ListView):
    model = Product
    template_name = "myweb/product/list.html"
    #paginate_by = 20
    context_object_name = 'products'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.company.pk:
    #         #context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
    #         productos = Product.objects.filter(company=self.request.user.company.pk).order_by("language")
    #         # page = self.request.GET.get('page', 1)
    #         # paginator = Paginator(producto, 20)
    #         # try:
    #         #     productos = paginator.page(page)
    #         # except PageNotAnInteger:
    #         #     productos = paginator.page(1)
    #         # except EmptyPage:
    #         #     productos = paginator.page(paginator.num_pages)
    #         context['products'] = productos

    #     else:
    #         context = {}
    #     return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            extension=''
            existenCSV = CsvArchivo.objects.all().count()
            if(existenCSV > 0):
                CsvArchivo.objects.get().delete()
            ok= request.FILES['csv']
            filename = str(request.FILES['csv'])
            if filename.endswith('.csv'):
                extension = 'csv'
            if extension != 'csv':
                print('****************extension incorrecta*******************')
                return HttpResponseRedirect(reverse_lazy('MyWebProductAdminList'))
            objeto = CsvArchivo(
                name = request.FILES['csv'],
                file = request.FILES.get('csv')
                )
            objeto.save()
            archivo = CsvArchivo.objects.get()
            ruta= archivo.file
            path= "medcombo/media/" + str(ruta)
            with open (path) as f:
                reader= csv.reader(f)
                for row in reader: 
                    lista = row[0]             #obtengo mi lista 
                    elemento = lista.split(';')
                
                    languageInstance= LanguageCampaign.objects.get(name_language=elemento[5])
                    areaInstance= Area.objects.get(name=elemento[2])
                    categoryInstance= Category.objects.get(name=elemento[3])
                    subcategoryInstance= SubCategory.objects.get(name=elemento[4])
                    companyInstance= Company.objects.get(name=elemento[6])
                    crearUsuario = Product(
                        name= elemento[0],
                        description=elemento[1],
                        area= areaInstance,
                        category= categoryInstance,
                        subcategory= subcategoryInstance,
                        company= companyInstance,
                        language= languageInstance,
                        )
                    crearUsuario.save()
                return HttpResponseRedirect(reverse_lazy('MyWebProductAdminList'))
        else:
            return HttpResponseRedirect(reverse_lazy('MyWebProductAdminList'))

def boosting_create(pk, company):
        #Boosting to ISO Certification and Manufacturer
        id_company = company
        id_product = pk
        my_product = Product.objects.get(id=id_product)
        company_filter = Company.objects.filter(id=id_company)
        product_filter = Product.objects.filter(id=id_product)
        iso = ''
        manufacturer = 0
        for c in company_filter:
            manufacturer = c.type_company
            iso = c.certification_iso
        if manufacturer == 8:
            for p in product_filter:
                if p.algorithmic_value:
                    my_product.algorithmic_value = p.algorithmic_value + 10
                    my_product.save()
                    print('Yes Manufacturer')
        product_filter = Product.objects.filter(id=id_product)
        if iso == '' or iso is None:
            print('None')
        else:
            for p in product_filter:
                if p.algorithmic_value:
                    my_product.algorithmic_value = p.algorithmic_value + 10
                    my_product.save()
                    print('Yes ISO')
        #------------------------------------------------
def add_boosting(id_company):
    my_products = Product.objects.filter(company=id_company)
    for products in my_products:
        product = Product.objects.get(id=products.id)
        product.algorithmic_value = products.algorithmic_value + 1
        product.save()

def add_for_keyword(id_company,new_product):
    #Adding for keywords
    find_product = Product.objects.filter(company=id_company)
    find = []
    my_keywords = []
    for fp in find_product:
        key_products = fp.keyword.all()
        for keys in key_products:
            if keys != '' or keys is not None:
                find.append(keys.id)
    my_keywords = set(find)
    for count in my_keywords:
        boosting_keyword = BoostingKeyword.objects.filter(company=id_company,keyword__id=count)
        #Editing
        if boosting_keyword:
            products = Product.objects.filter(keyword__id=count,company=id_company)
            score = Product.objects.filter(keyword__id=count,company=id_company).count()
            save_boosting = BoostingKeyword.objects.get(company=id_company, keyword=count)
            my_values = score * 2
            my_flags = int(my_values/10)
            save_boosting.value = my_values
            save_boosting.flag = my_flags
            save_boosting.save()
            to_keyword = BoostingKeyword.objects.filter(company=id_company, keyword=count)
            for boosting in to_keyword:
                for one in products:
                    save_product = Product.objects.get(id=one.id)
                    added = boosting.flag * 10
                    if save_product.id == new_product:
                        new = Product.objects.get(id=new_product)
                        new.algorithmic_value = new.algorithmic_value + added
                        new.save()
                    else:
                        if added == 0:
                            save_product.algorithmic_value = save_product.algorithmic_value + added
                            save_product.save()
                        else:
                            if boosting.value == added:
                                save_product.algorithmic_value = save_product.algorithmic_value + 10
                                save_product.save()
        #Creating
        else:
            product = Product.objects.filter(keyword__id=count,company=id_company).count()
            my_company = Company.objects.get(id=id_company)
            keyword_add = Keyword.objects.get(id=count)
            my_value = product * 2
            my_flag = int(my_value/10)
            save_key = BoostingKeyword(company=my_company, keyword=keyword_add,value=my_value,flag=my_flag)
            save_key.save()
            products = Product.objects.filter(keyword__id=count,company=id_company)
            to_keyword = BoostingKeyword.objects.filter(company=id_company, keyword=count)
            for boosting in to_keyword:
                for one in products:
                    save_product = Product.objects.get(id=one.id)
                    added = boosting.flag * 10
                    if save_product.id == new_product:
                        new = Product.objects.get(id=new_product)
                        new.algorithmic_value = new.algorithmic_value + added
                        new.save()
                    else:
                        if added == 0:
                            save_product.algorithmic_value = save_product.algorithmic_value + added
                            save_product.save()
                        else:
                            if boosting.value == added:
                                save_product.algorithmic_value = save_product.algorithmic_value + 10
                                save_product.save()
    #--------------------------------------

def ajax_category(request):
    my_id = request.POST.get('value')
    category = Category.objects.filter(relationship_id=my_id)

    return render(request, 'myweb/product/ajax_category.html', {'categorys': category})

def ajax_subcategory(request):
    my_id = request.POST.get('value')
    subcategory = SubCategory.objects.filter(relationship_id=my_id)

    return render(request, 'myweb/product/ajax_subcategory.html', {'subcategorys': subcategory})

def ajax_search_item(request):
    area_value = request.POST.get('area_value')
    category_value = request.POST.get('category_value')
    subcategory_value = request.POST.get('subcategory_value')
    keyword = request.POST.getlist('remove[]')
    area = Area.objects.get(id=area_value)
    category = Category.objects.get(id=category_value)
    subcategory = SubCategory.objects.get(id=subcategory_value)
    keywords = []
    for key in keyword:
        keyword_item = Keyword.objects.filter(id=key)
        keywords.extend(keyword_item)

    return render(request, 'myweb/product/ajax_selected_category.html', {'area': area, 'category': category, 'subcategory': subcategory, 'keywords': keywords})

class MywebProductCreate(LoginRequiredMixin, CreateView): #español
    model = Product
    template_name = 'myweb/product/create.html'
    form_class = CategoriesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        context['areas'] =  Area.objects.filter(language_id=4)

        return context

    def post(self, request, *args, **kwargs):
        print('4')
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreate'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')

            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
                print("------------", form)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update.html'
    form_class = CategoriesForm

    def get_context_data(self, **kwargs):
        print('español')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        print('********************************PRODUCTO ACTUALIZADO OLD******************************')
        area_old = self.request.POST.get('area_old')
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        print(area_old)
        if area_old == None or area_old == '': 
            areaInstance_old= None
        else:
            areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        #si alguna de las areas o categorias anteriores son diferentes, borro las keywords de la instancia!!!!!!!!
        return reverse('MyWebProductAdminList')#, kwargs={'pk': self.object.pk})

class MywebProductAdminDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'myweb/product/detail.html'

class Proposalmethod(LoginRequiredMixin, ListView):
    model = Proposal_Commercial
    template_name = "crm/economic/proposal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal = Proposal_Commercial.objects.filter(user_id=self.kwargs.get('pk'))
        
        # if proposal:
        #     proposal = Proposal_Commercial.objects.get(user_id=self.kwargs.get('pk'))
        #     values = Proposal_Product.objects.filter(commercial_prod_id=proposal.id)
        #if proposal:
        context['proposals'] = proposal
        # context['values'] = values
        return context
    

def Unapprove_propo_ajax(request):
    pro_id = request.POST.get('id')
    proposal = Proposal_Commercial.objects.get(pk=pro_id)
    values = Proposal_Product.objects.filter(commercial_prod_id=pro_id)
    
    return render(request, "crm/economic/unapproved.html", {'proposal_more':proposal, 'values':values})


def getpdf(request, value):  
    proposal = Proposal_Commercial.objects.filter(pk=value)
    logo = ImageReader('http://ec2-3-133-109-99.us-east-2.compute.amazonaws.com/static/img/logo.png')

    if proposal:
        proposal = Proposal_Commercial.objects.get(pk=value)
        values = Proposal_Product.objects.filter(commercial_prod_id=value)
        values_len = Proposal_Product.objects.filter(commercial_prod_id=value).count()
    
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename="Proposal.pdf"'  
    p = canvas.Canvas(response)  
    p.setFont("Times-Roman", 13)
    """BaseDocTemplate(  
        leftMargin= 30,  
        rightMargin= 30,  
        topMargin= 30,  
        bottomMargin= 30 
    )"""
    w, h = A4
    p.drawImage(logo, 20, 740, width=160, height=50)
    x = 390
    y = h - 110
    p.setFillColorRGB(0, 0.4, 0.7)
    p.setStrokeColorRGB(0, 0.4, 0.7)
    p.line(x, y, 550, y)
    x = 435
    y = h - 45
    p.setFillColorRGB(0, 0.4, 0.7)
    p.setStrokeColorRGB(0, 0.4, 0.7)
    p.line(x, 701, x, 762)
    p.rect(390, h - 140, 160, 60)
    p.setFillColorRGB(0, 0.4, 0.7) #127,155,205
    p.rect(20, 605, 540, 22, stroke = 0, fill = 1)
    p.setStrokeColorRGB(0.0, 1, 0.0)
    p.setFillColorRGB(0, 0, 0)  # Relleno para el texto 
    p.drawString(390,770, "ECONOMIC PROPOSAL") 
    p.drawString(400,740, "Titulo  " + str(proposal.title))
    p.drawString(400,710, "Date    " + str(proposal.edit_date))

    p.setFillColorRGB(1, 1, 1)
    p.drawString(30,610, "Producto")
    p.setFillColorRGB(1, 1, 1)
    p.drawString(350,610, "Discount ")
    p.setFillColorRGB(0, 0, 0)

    for i in range(values_len):
        p.drawString(30,580 - i*30, str(values[i].product.name))
        p.setFillColorRGB(0, 0, 0)
        p.drawString(350,580 - i*30 , values[i].discount + "%")  
        temp = i
    p.setFillColorRGB(1, 1, 1)
    p.drawString(200,640- (temp+1)*30 , "Total amount") 
    p.setFillColorRGB(0, 0, 0)
    p.drawString(200,610- (temp+1)*30 , proposal.total + "€")
    p.setFillColorRGB(1, 1, 1) 
    p.drawString(420,670- (temp+2)*30, "Price without Taxes")
    p.setFillColorRGB(0, 0, 0)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(30,520- (temp+3)*30, "Payment Conditions: " + proposal.payment_terms)
    if int(len(proposal.comments)) <= 100:
        p.drawString(30,520- (temp+4)*30, "Comments: " + proposal.comments)
    else:
        strlen = len(proposal.comments)
        string = proposal.comments
        chunks, chunk_size = strlen, 100
        strmake = [string[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        p.drawString(30,520- (temp+4)*30, "Comments: ")
        for count,strele in enumerate(strmake):
            p.drawString(30,520- (temp+5+count)*30, strele)

    p.setFillColorRGB(0, 0.4, 0.7)
    p.setStrokeColorRGB(0, 0.4, 0.7)
    p.line(20, 30, 250, 30)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(270,30, "Pág. 1 of 1")
    p.line(350, 30, 570, 30)
    p.showPage()  
    p.save()  
    return response 

def accept_proposal(request):
    my_id = request.POST.get('value')
    proposal = Proposal_Commercial.objects.get(pk=my_id)
    proposal.validata = True
    proposal.save()
    return HttpResponse('Ok')


class MywebProductDelete(LoginRequiredMixin, DeleteView):
    template_name = 'myweb/product/delete.html'
    model = Product
    #success_url = reverse_lazy('MyWebProductAdminList')

    def get_success_url(self):
        my_products = Product.objects.filter(company=self.request.user.company.id)
        for products in my_products:
            product = Product.objects.get(id=products.id)
            product.algorithmic_value = products.algorithmic_value - 1
            product.save()
        #Substracting for keywords
        company_id = self.request.user.company.id
        find_product = Product.objects.filter(company=company_id)
        find = []
        my_keywords = []
        for fp in find_product:
            key_products = fp.keyword.all()
            for keys in key_products:
                if keys != '' or keys is not None:
                    find.append(keys.id)
        my_keywords = set(find)
        for count in my_keywords:
            boosting_keyword = BoostingKeyword.objects.filter(company=company_id,keyword__id=count)
            #Minus
            if boosting_keyword:
                products = Product.objects.filter(keyword__id=count,company=company_id)
                score = Product.objects.filter(keyword__id=count,company=company_id).count()
                save_boosting = BoostingKeyword.objects.get(company=company_id, keyword=count)
                my_values = score * 2
                my_flags = int(my_values/10)
                save_boosting.value = my_values
                save_boosting.flag = my_flags
                save_boosting.save()
                to_keyword = BoostingKeyword.objects.filter(company=company_id, keyword=count)
                for boosting in to_keyword:
                    for one in products:
                        save_product = Product.objects.get(id=one.id)
                        minus = boosting.flag * 10
                        if minus == 0:
                            save_product.algorithmic_value = save_product.algorithmic_value - minus
                            save_product.save()
                        else:
                            if boosting.value == minus:
                                save_product.algorithmic_value = save_product.algorithmic_value - 10
                                save_product.save()
        return reverse('MyWebProductAdminList')

@login_required
def SearchKeywords(request):
    if request.is_ajax():
        idSubcategory = request.POST.get('idSubcategory')
        keywords = Keyword.objects.filter(subcategory_id=idSubcategory)
        return render(request, 'myweb/product/ajax_keyword.html', {'keywords': keywords})
    #flag = request.POST.get('flag')
    #     if idSubcategory == '' or idSubcategory is None:
    #         idSubcategory = 0
    #     if flag == '1':
    #         myCategory = Category.objects.filter(relationship=idSubcategory)
    #         if myCategory:
    #             my_result = {}
    #             data = json.dumps(my_result)
    #         else:
    #             my_keywords = Keyword.objects.filter(area=idSubcategory).order_by('name')
    #             my_result = {}
    #             for r in my_keywords:
    #                 #my_result[r.id] = r.name
    #                 my_result[r.name] = r.id
    #             #data = json.dumps(my_result)
    #             my_result_2 = collections.OrderedDict(sorted(my_result.items()))
    #             data = json.dumps(my_result_2, sort_keys=False)
    #     elif flag == '2':
    #         mySubcategory = SubCategory.objects.filter(relationship=idSubcategory)
    #         if mySubcategory:
    #             my_result = {}
    #             data = json.dumps(my_result)
    #         else:
    #             my_keywords = Keyword.objects.filter(category=idSubcategory).order_by('name')
    #             my_result = {}
    #             for r in my_keywords:
    #                 #my_result[r.id] = r.name
    #                 my_result[r.name] = r.id
    #             my_result_2 = collections.OrderedDict(sorted(my_result.items()))
    #             data = json.dumps(my_result_2, sort_keys=False)
    #             #data = json.dumps(my_result)
    #     else:
    #         my_keywords = Keyword.objects.filter(subcategory=idSubcategory).order_by('name')
    #         my_result = {}
    #         for r in my_keywords:
    #             #my_result[r.id] = r.name
    #             my_result[r.name] = r.id
    #         my_result_2 = collections.OrderedDict(sorted(my_result.items()))
    #         data = json.dumps(my_result_2, sort_keys=False)
    #         #data = json.dumps(my_result)
    # else:
    #     data = 'Fail'
    # mimetype = 'application/json'
    # return HttpResponse(data,mimetype)


@login_required
def SendSuggestion(request):
    if request.method == 'POST':
        my_language = request.POST.get('languages_select')
        if my_language == "es":
            lang_id = 4
        elif my_language == "en":
            lang_id = 3
        elif my_language == "zh-hant":
            lang_id = 1
        elif my_language == "de":
            lang_id = 2
        elif my_language == "fr":
            lang_id = 5
        elif my_language == "it":
            lang_id = 6
        elif my_language == "pt":
            lang_id = 7
        elif my_language == "zh-hans":
            lang_id = 8
        else:
            lang_id = 9

        my_word = request.POST.get('suggestion')
        print("--------------------", my_word)
        if my_word == '' or my_word is None:
            return HttpResponse('No')
        else:
            # existeKey= Keyword.objects.filter(name__iexact=my_word)
            # if(existeKey):
            #     print('ya existe esta keyword')
            #     return HttpResponse('No')
            # else:
            existeSyn= SynonymKeyword.objects.filter(name__iexact=my_word)
            if(existeSyn):
                print('existe el sinonimo')
                return HttpResponse('No')
            else:
                user = User.objects.get(id=request.user.id)
                status = "En Proceso"
                send_suggestion = SuggestionKeyword(name=my_word, user=user, status=status, language_id=lang_id)
                send_suggestion.save()
                return HttpResponse('Ok')
    return HttpResponse('Error in request!')

def ProductDelete(request):
    id = request.POST.get('value')
    my_product = Product.objects.get(id=id)
    my_product.delete()
    return HttpResponse('Ok')

class MywebProductCreateJapones(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_japones.html'
    form_class = CategoriesForm9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateJapones'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm9()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreateItaliano(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_italiano.html'
    form_class = CategoriesForm6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        print('6')
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateItaliano'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm6()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreatePortugues(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_portugues.html'
    form_class = CategoriesForm7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreatePortugues'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm7()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreateFrances(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_frances.html'
    form_class = CategoriesForm5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateFrances'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm5()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreateAleman(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_aleman.html'
    form_class = CategoriesForm2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        print('antes del post')
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateAleman'))
            '''
            language = request.POST.get('language')
            print(language)
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    print('sin key')
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    print('con key')
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                print('error')
                form = CategoriesForm2()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreateIngles(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_ingles.html'
    form_class = CategoriesForm3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            print(mydesc)
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateIngles'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm3()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreateChinoSimplificado(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_chinosimplificado.html'
    form_class = CategoriesForm8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateChinoSimplificado'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()

            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm8()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductCreateChinoTradicional(LoginRequiredMixin, CreateView):
    template_name = 'myweb/product/create_chinotradicional.html'
    form_class = CategoriesForm1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            '''
            mydesc= request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>':
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
                return HttpResponseRedirect(reverse_lazy('MywebProductCreateChinoTradicional'))
            '''
            language = request.POST.get('language')
            keywords = request.POST.getlist('keyword[]')
            if(language== '4'):
                form = CategoriesForm(request.POST, request.FILES)
            elif(language== '1'):
                form = CategoriesForm1(request.POST, request.FILES)
            elif(language== '2'):
                form = CategoriesForm2(request.POST, request.FILES)
            elif(language== '3'):
                form = CategoriesForm3(request.POST, request.FILES)
            elif(language== '5'):
                form = CategoriesForm5(request.POST, request.FILES)
            elif(language== '6'):
                form = CategoriesForm6(request.POST, request.FILES)
            elif(language== '7'):
                form = CategoriesForm7(request.POST, request.FILES)
            elif(language== '8'):
                form = CategoriesForm8(request.POST, request.FILES)
            elif(language== '9'):
                form = CategoriesForm9(request.POST, request.FILES)
            my_company = self.request.user.company.id
            products_saved = Product.objects.filter(company=my_company).count()
            if form.is_valid():
                if keywords == "" or keywords is None:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    return HttpResponseRedirect('/myweb/product/list')
                else:
                    form.language= language
                    my_object = form.save()
                    new = Product.objects.get(id=my_object.pk)
                    new.algorithmic_value = new.algorithmic_value + products_saved
                    today = date.today()
                    new.request_date = today
                    new.save()
                    for key in keywords:
                        p = Keyword.objects.get(id=key)
                        my_object.keyword.add(p)
                    #Boosting added products
                    add_boosting(my_company)
                    #Boosting ISO and Manufacturer
                    boosting_create(my_object.pk, my_object.company.id)
                    #Boosting Keywords
                    add_for_keyword(my_company,my_object.pk)
                    return HttpResponseRedirect('/myweb/product/list')
            else:
                form = CategoriesForm1()
                return HttpResponseRedirect('/myweb/product/list')

class MywebProductUpdateIngles(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_ingles.html'
    form_class = CategoriesForm3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdateAleman(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_aleman.html'
    form_class = CategoriesForm2

    def get_context_data(self, **kwargs):
        print('aleman')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdateFrances(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_frances.html'
    form_class = CategoriesForm5

    def get_context_data(self, **kwargs):
        print('create_frances')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdatePortugues(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_portugues.html'
    form_class = CategoriesForm7

    def get_context_data(self, **kwargs):
        print('create_portugues')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdateItaliano(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_italiano.html'
    form_class = CategoriesForm6

    def get_context_data(self, **kwargs):
        print('create_italiano')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdateJapones(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_japones.html'
    form_class = CategoriesForm9

    def get_context_data(self, **kwargs):
        print('create_japones')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdateChinoTradicional(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_chinotradicional.html'
    form_class = CategoriesForm1

    def get_context_data(self, **kwargs):
        print('create_chinotradicional')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')
        #return reverse('MywebProductAdminDetail', kwargs={'pk': self.object.pk})

class MywebProductUpdateChinoSimplificado(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'myweb/product/update_chinosimplificado.html'
    form_class = CategoriesForm8

    def get_context_data(self, **kwargs):
        print('create_chinosimplificado')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs.get('pk'))
        context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')
        return context

    def get_success_url(self):
        productInstance= Product.objects.get(pk=self.kwargs.get('pk'))
        foto1 = self.request.POST.get('foto_existente1')
        foto2 = self.request.POST.get('foto_existente2')
        foto3 = self.request.POST.get('foto_existente3')
        foto4 = self.request.POST.get('foto_existente4')
        #eliminar fotos******************
        if foto1=='borrado':
            productInstance.picture=''
        if foto2=='borrado':
            productInstance.picture2=''
        if foto3=='borrado':
            productInstance.picture3=''
        if foto4=='borrado':
            productInstance.picture4=''
        productInstance.save()
        #fin eliminar fotos**************
        area_old = self.request.POST.get('area_old')
        areaInstance_old= Area.objects.get(pk=area_old)
        category_old = self.request.POST.get('category_old')
        if category_old == None or category_old == '':
            categoryInstance_old = None
        else:
            categoryInstance_old= Category.objects.get(pk=category_old)
        subcategory_old = self.request.POST.get('subcategory_old')
        if subcategory_old == None or subcategory_old == '':
            subcategoryInstance_old = None
        else:
            subcategoryInstance_old= SubCategory.objects.get(pk=subcategory_old)
        if productInstance.area != areaInstance_old or productInstance.category != categoryInstance_old or productInstance.subcategory !=  subcategoryInstance_old:
            keywords_to_delete = productInstance.keyword.all()
            for key in keywords_to_delete:
                productInstance.keyword.remove(key)
        return reverse('MyWebProductAdminList')


def Ajax_administrar_keywords(request):
    keys=[]
    palabra= []
    iduser= request.user.pk
    id_language = request.POST.get('language_pk')
    usuario= User.objects.get(pk= iduser)
    idcompany= usuario.company
    productos= Product.objects.filter(company= idcompany) #TODOS MIS PRODUCTOS
    for producto in productos:
        ProductInstance= Product.objects.get(pk= producto.pk)
        keywords= ProductInstance.keyword.all()
        for myword in keywords:
            if myword in keys:
                continue
            else:
                keywor= Keyword.objects.filter(pk=myword.pk, language=id_language)
                keys.extend(keywor)
    relationship= AdminProduct.objects.filter(user= iduser)
    language_select= LanguageCampaign.objects.get(pk=id_language)
    
    return render(request, 'myweb/product/administrar_key_product_select.html', {'keywords': keys, 'productos':productos, 'relacion': relationship, 'language_select': language_select})


def Ajax_update_keywords_product(request):
    key_asignados= []
    key_no_asignados= []
    id_area = request.GET.get('id_area')
    id_category = request.GET.get('id_category')
    id_subcategory = request.GET.get('id_subcategory')
    id_product = request.GET.get('id_product')
    keywords_producto = Product.objects.get(pk= id_product).keyword.all()
    if id_category== None or id_category=='':
        keywords_select = Keyword.objects.filter(
            area_id= id_area,
            category_id= None,
            subcategory_id= None).order_by('-pk')
    elif id_subcategory== None or id_subcategory=='':  
        keywords_select = Keyword.objects.filter(
            area_id= id_area, 
            category_id= id_category,
            subcategory_id= None).order_by('-pk')
    else:
        keywords_select = Keyword.objects.filter(
            area_id= id_area, 
            category_id= id_category,
            subcategory_id= id_subcategory).order_by('-pk')
    for key in keywords_select:
        print(key)
        if key in keywords_producto:
            key_asignados.append(key)
        else:
            key_no_asignados.append(key)
    return render(request, 'myweb/product/keywords_update_product.html', {'keywords': keywords_select, 'id_producto': id_product, 'asignados': key_asignados, 'no_asignados': key_no_asignados})


def Ajax_asignar_keyword_product(request):
    id_producto = request.GET.get('id_producto')
    id_keyword = request.GET.get('id_keyword')
 
    productInstance = Product.objects.get(pk= id_producto)
    language_product= productInstance.language
    keywordInstance = Keyword.objects.get(pk= id_keyword)
    language_keyword= keywordInstance.language

    id_area_producto = productInstance.area
    id_category_producto = productInstance.category
    id_subcategory_producto = productInstance.subcategory
    
    id_area_keyword = keywordInstance.area
    id_category_keyword = keywordInstance.category
    id_subcategory_keyword = keywordInstance.subcategory

    if id_area_producto== id_area_keyword and id_category_producto== id_category_keyword and id_subcategory_producto == id_subcategory_keyword:
        productInstance.keyword.add(keywordInstance) #asigno la palabra al producto
        if language_product != language_keyword:
            productInstance.language= keywordInstance.language
            productInstance.save()
    else:
        keywords_to_delete= productInstance.keyword.all()
        for key in keywords_to_delete:
            print(key)
            productInstance.keyword.remove(key)
            print(key.name)
        #AL ASIGNAR NUEVAS PALABRAS CLAVES, AUTOMATICAMENTE CAMBIO EL AREA, CATEGORIA, Y SUBCATEGORIA
        productInstance.area= id_area_keyword
        productInstance.category= id_category_keyword
        productInstance.subcategory= id_subcategory_keyword
        productInstance.keyword.add(keywordInstance)
        if language_product != language_keyword:
            productInstance.language= keywordInstance.language
        productInstance.save()
    return HttpResponse('Ok')


def Ajax_eliminar_keyword_product(request):

    id_producto = request.GET.get('id_producto')
    id_keyword = request.GET.get('id_keyword')
    print(id_producto)
    print(id_keyword)
    productInstance = Product.objects.get(pk= id_producto)
    keywordInstance = Keyword.objects.get(pk= id_keyword)

    id_area_producto = productInstance.area
    id_category_producto = productInstance.category
    id_subcategory_producto = productInstance.subcategory
    
    id_area_keyword = keywordInstance.area
    id_category_keyword = keywordInstance.category
    id_subcategory_keyword = keywordInstance.subcategory

    if id_area_producto== id_area_keyword and id_category_producto== id_category_keyword and id_subcategory_producto == id_subcategory_keyword:
        print('sólo voy a eliminar la keyword')
        productInstance.keyword.remove(keywordInstance) #asigno la palabra al producto
    else:
        productInstance.keyword.remove(keywordInstance) 
        print('qué pasó aquí?, no deberia darse esta condicion')
    return HttpResponse('Ok')


def MywebProductAdmininistrar(request):
    keys=[]
    palabra= []
    iduser= request.user.pk
    usuario= User.objects.get(pk= iduser)
    idcompany= usuario.company
    productos= Product.objects.filter(company= idcompany) #TODOS MIS PRODUCTOS
    for producto in productos:
        ProductInstance= Product.objects.get(pk= producto.pk)
        keywords= ProductInstance.keyword.all()
        for myword in keywords:
            print(myword.pk)
            if myword in keys:
                continue
            else:
                keywor= Keyword.objects.filter(pk=myword.pk)
                keys.extend(keywor)
    print(keys)
    relationship= AdminProduct.objects.filter(user= iduser)
    
    return render(request, 'myweb/product/administrar_key_product.html', {'keywords': keys, 'productos':productos, 'relacion': relationship})


def Ajax_administrar_product(request):
    productid = request.GET.get('productid')
    keyid = request.GET.get('keyid')
    userid = request.GET.get('userid')
    existe= AdminProduct.objects.filter(user= userid, keyword= keyid, product= productid).count()#si es cero(0), no existe, lo salvo
    prodInstance= Product.objects.get(pk=productid)
    userInstance= User.objects.get(pk=userid)
    keyInstance= Keyword.objects.get(pk=keyid)

    if existe == 0: #voy a agregar
        existen= AdminProduct.objects.filter(user= userid, keyword= keyid).count()
        if existen <= 2: #aun puedo agregar mas productos

            AgregarAdministrar= AdminProduct(
                product= prodInstance,
                user= userInstance,
                keyword= keyInstance
                )
            AgregarAdministrar.save()
            print('agregado')
            return HttpResponse('Agregado')

        elif existen >= 3: #ya alcance el limite de 3 productos
            return HttpResponse('Elimine')
    else:
        AdminProduct.objects.get(
            product= productid,
            user= userid,
            keyword= keyid,
            ).delete()
        print('eliminado')
        return HttpResponse('Eliminado')
    

def Ajax_administrar_product_listado(request):
    keyid = request.POST.get('keyid')
    userid = request.POST.get('userid')
    usuario= User.objects.get(pk= userid)
    idcompany= usuario.company
    keyword= Keyword.objects.get(pk=keyid)
    productos= Product.objects.filter(company= idcompany) #TODOS MIS PRODUCTOS del usuario
    productos_aprobados= AdminProduct.objects.filter(user= userid, keyword= keyid)
    return render(request, 'myweb/product/administrar_key_product_listado.html', {'productos': productos, 'aprobados':productos_aprobados, 'keyword':keyword})

    