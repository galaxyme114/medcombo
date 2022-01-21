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
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from medcombo.configuration.usercustom.models import User
from django import template
from medcombo.product.models import Product, PolicyPrivacyModel
from medcombo.configuration.company.models import Company
from medcombo.product.models import SuggestionKeyword, SynonymKeyword, Area, Category, SubCategory, Keyword
from django.http import HttpResponse
from medcombo.crm.dashboard_admin.models import LanguageCampaign
from django.utils import translation
import tablib
from import_export import resources
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.timezone import localtime, now
from medcombo.crm.dashboard_admin.models import LanguageCampaign

#Module: Admin - marketing
class AdminUserCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model= User
    template_name = "crm/admin/user.html"

    def get_context_data(self, **kwargs):
        context = super(AdminUserCrm, self).get_context_data(**kwargs)
        productos= Product.objects.filter(approved='False').count()
        webs= Company.objects.filter(approved='False').count()
        key= SuggestionKeyword.objects.filter(status='En Proceso').count()
        context['products']=productos
        context['key']=key
        context['webs']=webs
        return context

def AdminUserConfirmGenerate(request, id_user):
    random_new_password = get_random_string(length=8)
    miuser= User.objects.get(id=id_user)
    if request.method== 'GET':
        nombre= miuser.email
    else:
        miuser.set_password(random_new_password)
        miuser.save()
        send_mail('Medcombo', 'Esta es su nueva contraseña de seguridad "'+ random_new_password + '". Su usuario es "'+miuser.email+'".',
        'contacto@medcombo.es',
            [miuser.email],
            fail_silently= True,
            )
        return redirect('AdminUserCrm')
    return render(request, 'crm/admin/user_confirm.html', {'form': nombre})

def AdminUserConfirmRestablecer(request, id_user):
    miuser= User.objects.get(id=id_user)
    if request.method== 'GET':
        nombre=miuser.first_name + " " + miuser.last_name
    else:
        send_mail('Medcombo',
            'Su contraseña ha sido restablecida. Esta es su contraseña: '+ miuser.password,
            'contacto@medcombo.es',
            [miuser.email],
            fail_silently= True,
            )
        return redirect('AdminUserCrm')
    return render(request, 'crm/admin/user_confirm.html', {'form': nombre})

@permission_required('usercustom.management_user')
def AdminProductCrm(request):
    usuaris=[]
    emails=[]
    #productos= Product.objects.all().filter(approved='False', notify='True') #mis productos por aprobar
    productos= Product.objects.all()
    if request.method == 'GET':
        productoss= Product.objects.filter(approved='False', notify='True').count()
        webs= Company.objects.filter(approved='False').count()
        key= SuggestionKeyword.objects.filter(status='En Proceso').count()
    if request.method == 'POST':
        print('post admin product')
        idproduct = request.POST.get('pk')
        miproduct= Product.objects.filter(pk=idproduct).update(approved="True", notify='False')
        productoss= Product.objects.filter(approved='False').count()
        key= SuggestionKeyword.objects.filter(status='En Proceso').count()
        webs= Company.objects.filter(approved='False').count()
               
    for producto in productos:
        print("product", producto)
        idcompany= producto.company_id #obtengo el id de la compañia a la que pertence el producto
        usuarios= User.objects.filter(company_id=idcompany) #obtengo todos los usuarios que pertenecen a esa compañia
        for user in usuarios:
            email= user.username
            if email in emails: #si ese email ya existe en mi lista, continuo y NO lo agrego
                continue
            else: #si ese email no existe en mi listado, agrego el usuario a la lista, y el email que es unico
                user.ac_count = Product.objects.filter(company_id=user.company_id, approved=False).count()
                usuaris.extend(usuarios)
                emails.append(email)
    contexto= {'usuarios': usuaris, 'products': productoss, 'key': key, 'webs': webs}
    return render(request, "crm/admin/product.html", contexto)

def approve_product_ajax(request):
    print('since approve product ajax')
    idproduct = request.GET.get('pk')
    print(idproduct)
    miproduct= Product.objects.filter(pk=idproduct).update(approved="True")
    productoss= Product.objects.filter(approved='False').count()
    key= SuggestionKeyword.objects.filter(status='En Proceso').count()
    webs= Company.objects.filter(approved='False').count()
    return HttpResponse('Ok')

class AdminKeywordCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = SuggestionKeyword
    template_name = "crm/admin/keyword.html"

    def get_context_data(self, **kwargs):
        context = super(AdminKeywordCrm, self).get_context_data(**kwargs)
        language_filter = LanguageCampaign.objects.all().order_by('value_language')
        queryset = SuggestionKeyword.objects.filter(status='En Proceso')
        context['language_filter'] = language_filter
        context['key'] = queryset
        
        return context

    def post(self, request, *args, **kwargs):
        idarea = request.POST.get('areaselected')
        id_language = request.POST.get('language_selected')
        language = LanguageCampaign.objects.get(pk= id_language)
        idcategory = request.POST.get('categoryselected')
        idsubcategory = request.POST.get('subcategoryselected')
    
        if idcategory=='' or idcategory==None:
            actual_lang = translation.get_language()
            if actual_lang=='es':
                messages.error(request, 'No existe artículo')
            if actual_lang=='zh-hant':
                messages.error(request, '不存在的項目')
            if actual_lang=='de':
                messages.error(request, 'Kein vorhandener Gegenstand')
            if actual_lang=='en':
                messages.error(request, 'No existen Item')
            if actual_lang=='fr':
                messages.error(request, 'Aucun article existant')
            if actual_lang=='it':
                messages.error(request, 'Nessun articolo esistente')
            if actual_lang=='pt':
                messages.error(request, 'Item inexistente')
            if actual_lang=='zh-hans':
                messages.error(request, '不存在的项目')
            if actual_lang=='ja':
                messages.error(request, '存在するアイテムはありません')
            return HttpResponseRedirect(reverse_lazy('AdminKeywordCrm'))

        area= Area.objects.get(id=idarea)
        category= Category.objects.get(id=idcategory)
        subcategory= SubCategory.objects.get(id=idsubcategory)
        idkeyword = request.POST.get('idselected')
        SuggestionKeyword.objects.filter(pk=idkeyword).update(status="Aprobado")
        Keyword.objects.create(
            name= request.POST.get('namekey'),
            category= category,
            area= area,
            subcategory = subcategory,
            language = language)
        return redirect('AdminKeywordCrm')

@permission_required('usercustom.management_user')
def AdminMywebCrm(request):
    users=[]
    #queryset =  Company.objects.filter(approved=False, notify=True)
    queryset =  Company.objects.all()
    for empresa in queryset:
        idempresa= empresa.pk
        user= User.objects.filter(company_id=idempresa,lead=False)
        users.extend(user)

    if request.method == 'GET':
        productoss= Product.objects.filter(approved='False', notify=True).count()
        key= SuggestionKeyword.objects.filter(status='En Proceso').count()
        #webs= Company.objects.filter(approved='False', notify=True).count()
        webs = Company.objects.all().count()
    if request.method == 'POST':
        
        idcompany = request.POST.get('pk')
        micompany= Company.objects.filter(pk=idcompany).update(approved="True", notify=False)
        productoss= Product.objects.filter(approved='False').count()
        # webs= Company.objects.filter(approved='False').count()
        webs= Company.objects.all().count()
        key= SuggestionKeyword.objects.filter(status='En Proceso').count()
        
    contexto= {'company': users, 'products': productoss, 'key': key, 'webs': webs}
    return render(request, "crm/admin/myweb.html", contexto)

class PrivacyPolicy(PermissionRequiredMixin, TemplateView):
    permission_required = 'usercustom.marketing_user'
    template_name = "crm/contact/privacy_policy.html"

def load_myweb_admin(request): 
    idcompany = request.GET.get('id')
    miuser= User.objects.get(company_id=idcompany)
    User.objects.filter(company=idcompany).update(com_approve_date=localtime(now()))
    send_mail('Medcombo', 'Felicidades, su solicitud ha sido aprobada exitosamente, ya puede acceder a su sitio web.',
        'contacto@medcombo.es',
            [miuser.email],
            fail_silently= True,
            )
    return render(request, 'crm/admin/myweb.html')

def delete_myweb_admin(request):
    idcompany = request.GET.get('id')
    miuser= User.objects.get(company_id=idcompany)
    Company.objects.filter(pk=idcompany).delete()
    send_mail('Medcombo', 'Lo sentimos, su solicitud ha sido rechazada.',
        'contacto@medcombo.es',
            [miuser.email],
            fail_silently= True,
            )
    print('mensaje enviado')
    return render(request, 'crm/admin/myweb.html')

@permission_required('usercustom.management_user')
def load_products_admin(request):
    idcompany = request.GET.get('id')
    productos = Product.objects.filter(company_id=idcompany, notify=True).order_by('-pk')
    return render(request, 'crm/admin/list_product.html', {'productos': productos})

@permission_required('usercustom.marketing_user')
def Get_keywords(request):
    language= request.GET.get('language') #enviarlo mediante un formulario desde la vista
    if language == None:
        language = 4
    idkey = request.GET.get('id')
    keyword = SuggestionKeyword.objects.filter(id=idkey)
    area= Area.objects.filter(language= language)
    category= Category.objects.filter(language= language)
    subcategory= SubCategory.objects.filter(language= language)
    return render(request, 'crm/admin/mykey_load.html', {
     'key': keyword,
     'area': area, 
     'category': category, 
     'subcategory': subcategory,
     'language': language})

class load_keywords(LoginRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    model = SuggestionKeyword
    template_name = "crm/admin/mykey.html"
    success_url = reverse_lazy('AdminKeywordCrm')

    def get_context_data(self, **kwargs):
        context = super(load_keywords, self).get_context_data(**kwargs)
        language_filter = LanguageCampaign.objects.all().order_by('value_language')
        idkey = self.kwargs.get('pk')
        language = self.kwargs.get('lang')
        context['langu'] = int(language)
        context['language_filter'] = language_filter
        context['idkey'] = idkey
        
        return context

class ApproveMyWebCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.management_user'
    model = Company
    fields = ['approved','notify'] #es el unico campo que voy a actualizar, los demas solo los muestro
    template_name = "crm/admin/to_approve_web.html"
    success_url = reverse_lazy('AdminMywebCrm')

class SeeProductCrm(UpdateView):
    model = Product
    fields = ['picture','picture2', 'picture3', 'picture4'] #es el unico campo que voy a actualizar, los demas solo los muestro
    template_name = "crm/admin/see_image_product.html"
    success_url = reverse_lazy('AdminProductCrm')

#Module: Categories
class AdminCategoryCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.marketing_user'
    template_name = "crm/admin/categories.html"
    model = Area

    def get_context_data(self, **kwargs):
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
        misareas = Area.objects.filter(language_id=idlang)
        context['object_list2'] = misareas
        return context


@permission_required('usercustom.marketing_user')
def area_keywords_ajax(request):
    print('**************************************************')
    idarea = request.GET.get('idarea')
    keywords = Keyword.objects.filter(area_id=idarea, category_id=None, subcategory_id=None)
    print(keywords)
    print('*****************************************************')
    return render(request, 'crm/admin/ajaKeyarea.html', {'keywords': keywords})

@permission_required('usercustom.marketing_user')
def keywords_ajax(request):
    idsubcategory = request.GET.get('id')
    keywords = Keyword.objects.filter(subcategory_id=idsubcategory)
    for key in keywords:
        key.synonym = SynonymKeyword.objects.filter(keyword_id=key.pk)
    print('******************************************  keywords_ajax *****************************************')
    return render(request, 'crm/admin/ajaxKey.html', {'keywords': keywords})


@permission_required('usercustom.marketing_user')
def category_keywords_ajax(request):
    idcategory = request.GET.get('idcategory')
    keywords = Keyword.objects.filter(category_id=idcategory)
    for key in keywords:
        key.synonym = SynonymKeyword.objects.filter(keyword_id=key.pk)
    return render(request, 'crm/admin/ajaxKeycategory.html', {'keywords': keywords})

@permission_required('usercustom.marketing_user')
def subcategories_ajax(request):
    idcategory = request.GET.get('id')
    subcategories = SubCategory.objects.filter(relationship_id=idcategory)
    return render(request, 'crm/admin/ajaxSubCategory.html', {'subcategories': subcategories})

@permission_required('usercustom.marketing_user')
def categories_ajax(request):
    idarea = request.GET.get('id')
    categories = Category.objects.filter(relationship_id=idarea)
    return render(request, 'crm/admin/ajaxCategory.html', {'categories': categories})

@permission_required('usercustom.marketing_user')
def UpdateAdminCategoryKeywordCrm(request, area, category, subcategory):
    #el metodo get carga el area, categoria y subcategoria, keywords seleccionados
    miarea= Area.objects.filter(pk=area)
    language_filter = LanguageCampaign.objects.all().order_by('value_language')
    if subcategory != '0':
        misubcategoria= SubCategory.objects.filter(pk=subcategory)
        micategoria= Category.objects.filter(pk=category)
        mikey= Keyword.objects.filter(subcategory_id= subcategory)
        if mikey.count() == 0:
            mikey=None
    elif category != '0':
        misubcategoria= None
        micategoria= Category.objects.filter(pk=category)
        subnivel= SubCategory.objects.filter(relationship=category).count() #para ver si tiene subcategorias
        if subnivel == 0:
            mikey= Keyword.objects.filter(category_id= category)
            if mikey.count() == 0:
                mikey=None
        else:
            mikey=None
    else:
        misubcategoria=None
        micategoria=None
        subnivel= Category.objects.filter(relationship=area).count() #para ver si tiene categorias
        if subnivel == 0:
            mikey= Keyword.objects.filter(area_id= area)
            if mikey.count() == 0:
                mikey=None
        else:
            mikey=None

    #el metodo post actualiza el area, categoria o subcategoria seleccionados
    if request.method == 'POST':
        actual_lang = translation.get_language()
        idlanguage= request.POST.get('language')
        nombre= request.POST.get('miname')
        descripcion= request.POST.get('description')
        if nombre=='' or nombre.isspace() or nombre==None or nombre.isdigit():
            if actual_lang=='es':
                messages.error(request, 'Debe ingresar un nombre válido')
            if actual_lang=='zh-hant':
                messages.error(request, '您必須輸入一個有效的名字')
            if actual_lang=='de':
                messages.error(request, 'Sie müssen einen gültigen Namen eingeben')
            if actual_lang=='en':
                messages.error(request, 'You must enter a valid name')
            if actual_lang=='fr':
                messages.error(request, 'Vous devez entrer un nom valide')
            if actual_lang=='it':
                messages.error(request, 'Devi inserire un nome valido')
            if actual_lang=='pt':
                messages.error(request, 'Você deve inserir um nome válido')
            if actual_lang=='zh-hans':
                messages.error(request, '您必须输入一个有效的名字')
            if actual_lang=='ja':
                messages.error(request, '有効な名前を入力する必要があります')
            return render(request, 'crm/admin/categories_keyword.html', {'area': miarea, 'category': micategoria, 'subcategory': misubcategoria, 'keyword': mikey, 'language_filter':language_filter})        
        
        imagen_existente = request.POST.get('foto_existente')
        languageInstance = LanguageCampaign.objects.get(pk=idlanguage)
        pk = request.POST.get('pkcategory') #idcategoria
        namecategory = request.POST.get('namecategory') #nombre de categoria
        mkey = request.POST.get('mkey')
        if namecategory == 'area':
            imagen= request.FILES.get('picture')
            if imagen_existente == 'borrado':
                areaupdate= Area.objects.filter(pk=pk).update(
                name= request.POST.get('miname').strip(),
                description= request.POST.get('description'),
                active= request.POST.get('isActive'),
                language= idlanguage,
                image= '',
                h_tag=mkey,
                )
            elif imagen == None or imagen == '':
                areaupdate= Area.objects.filter(pk=pk).update(
                name= request.POST.get('miname').strip(),
                description= request.POST.get('description'),
                active= request.POST.get('isActive'),
                language= idlanguage,
                h_tag=mkey,
                )
            
            else:
                areaupdate= Area.objects.get(pk=pk)
                areaupdate.name= request.POST.get('miname').strip()
                areaupdate.description = request.POST.get('description')
                areaupdate.image = request.FILES.get('picture')
                areaupdate.active = request.POST.get('isActive')
                areaupdate.language = languageInstance
                areaupdate.save()
        elif namecategory=='category':
            imagen= request.FILES.get('picture')
            if imagen_existente == 'borrado':
                categoryupdate= Category.objects.filter(pk=pk).update(
                name= request.POST.get('miname').strip(),
                description= request.POST.get('description'),
                active= request.POST.get('isActive'),
                language= idlanguage,
                image= '',
                h_tag=mkey,
                )
            elif imagen == None or imagen == '':
                categoryupdate= Category.objects.filter(pk=pk).update(
                name= request.POST.get('miname').strip(),
                description= request.POST.get('description'),
                active= request.POST.get('isActive'),
                language= idlanguage,
                h_tag=mkey,
                )
            
            else:
                categoryupdate= Category.objects.get(pk=pk)
                categoryupdate.name= request.POST.get('miname').strip()
                categoryupdate.description = request.POST.get('description')
                categoryupdate.image = request.FILES.get('picture')
                categoryupdate.active = request.POST.get('isActive')
                categoryupdate.language = languageInstance
                categoryupdate.save()
        elif namecategory == 'subcategory':
            imagen= request.FILES.get('picture')

            if imagen_existente == 'borrado':
                subcategoryupdate= SubCategory.objects.filter(pk=pk).update(
                name= request.POST.get('miname').strip(),
                description= request.POST.get('description'),
                active= request.POST.get('isActive'),
                language = idlanguage,
                image= '',
                h_tag=mkey,
                )
            elif imagen == None or imagen == '':
                subcategoryupdate= SubCategory.objects.filter(pk=pk).update(
                name= request.POST.get('miname').strip(),
                description= request.POST.get('description'),
                active= request.POST.get('isActive'),
                language = idlanguage,
                h_tag=mkey,
                )
            
            else:
                subcategoryupdate= SubCategory.objects.get(pk=pk)
                subcategoryupdate.name= request.POST.get('miname').strip()
                subcategoryupdate.description = request.POST.get('description')
                subcategoryupdate.image = request.FILES.get('picture')
                subcategoryupdate.active = request.POST.get('isActive')
                subcategoryupdate.language = languageInstance
                subcategoryupdate.save()
        
    return render(request, 'crm/admin/categories_keyword.html', {'area': miarea, 'category': micategoria, 'subcategory': misubcategoria, 'keyword': mikey ,'language_filter':language_filter})

@permission_required('usercustom.marketing_user')
def loadKeys(request):
    id = request.GET.get('id')
    status = request.GET.get('status')
    if status == 'sub':
        keywords = Keyword.objects.filter(subcategory=id)
    elif status == 'cat':
        keywords = Keyword.objects.filter(category=id)
    elif status == 'are':
        keywords = Keyword.objects.filter(area=id)
    return render(request, 'crm/admin/loadingkeys.html', {'keywords': keywords})

@permission_required('usercustom.marketing_user')
def ListAdminCategoryKeywordCrm(request, language):
    miarea= Area.objects.filter(language= language)
    actual_lang = translation.get_language()
    language_filter = LanguageCampaign.objects.all().order_by('value_language')
    if request.method == 'POST':
        nombre= request.POST.get('name')
        descripcion= request.POST.get('description')
        if nombre=='' or nombre.isspace() or nombre==None or nombre.isdigit():
            if actual_lang=='es':
                messages.error(request, 'Debe ingresar un nombre válido')
            if actual_lang=='zh-hant':
                messages.error(request, '您必須輸入一個有效的名字')
            if actual_lang=='de':
                messages.error(request, 'Sie müssen einen gültigen Namen eingeben')
            if actual_lang=='en':
                messages.error(request, 'You must enter a valid name')
            if actual_lang=='fr':
                messages.error(request, 'Vous devez entrer un nom valide')
            if actual_lang=='it':
                messages.error(request, 'Devi inserire un nome valido')
            if actual_lang=='pt':
                messages.error(request, 'Você deve inserir um nome válido')
            if actual_lang=='zh-hans':
                messages.error(request, '您必须输入一个有效的名字')
            if actual_lang=='ja':
                messages.error(request, '有効な名前を入力する必要があります')
            return render(request, 'crm/admin/create_categories_keyword.html', {'areas': miarea, 'language_pk': int(language)})

        # idlanguage= request.POST.get('language')
        languageInstance = LanguageCampaign.objects.get(pk=language)
        nivel = request.POST.get('nivel') #indica el numero del nivel donde se va a insertar
        print("nivel", nivel)
        if nivel == '1': #no requiere id categoria madre
            objeto = Area(
                name= request.POST.get('name').strip(),
                description= request.POST.get('description'),
                image= request.FILES.get('picture'),
                active= request.POST.get('isActive'),
                language= languageInstance,
                h_tag=request.POST.get('mainkey'),
                )
            objeto.save()
        elif nivel == '2': #requiere id del area
            idarea= request.POST.get('relationship')
            areaInstance = Area.objects.get(pk=idarea)
            objeto = Category(
                relationship = areaInstance,
                name= request.POST.get('name').strip(),
                description= request.POST.get('description'),
                image= request.FILES.get('picture'),
                active= request.POST.get('isActive'),
                language= languageInstance,
                h_tag=request.POST.get('mainkey'),
                )
            objeto.save()
            #al insertar un nuevo subnivel, reviso si la categoria madre posee keywords y la asigno al subnivel actual
            keywords= Keyword.objects.filter(area = idarea, category= None, subcategory= None)
            if keywords.count() > 0: #posee keywords
                for key in keywords:
                    idkey= key.pk
                    key_update= Keyword.objects.filter(pk=idkey).update(category=objeto.pk)

        elif nivel == '3': #requiere id de categoria
            idcategory= request.POST.get('relationship')
            categoryInstance = Category.objects.get(pk=idcategory)
            objeto = SubCategory(
                relationship = categoryInstance,
                name= request.POST.get('name').strip(),
                description= request.POST.get('description'),
                image= request.FILES.get('picture'),
                active= request.POST.get('isActive'),
                language= languageInstance,
                h_tag=request.POST.get('mainkey'),
                )
            objeto.save()
            #al insertar un nuevo subnivel, reviso si la categoria madre posee keywords y la asigno al subnivel actual
            keywords= Keyword.objects.filter(category= idcategory, subcategory= None)
            if keywords.count() > 0: #posee keywords
                for key in keywords:
                    idkey= key.pk
                    key_update= Keyword.objects.filter(pk=idkey).update(subcategory=objeto.pk)
    return render(request, 'crm/admin/create_categories_keyword.html', {'areas': miarea, 'language_pk': int(language), 'language_filter':language_filter})

@permission_required('usercustom.marketing_user')
def Crear_Keyword_Ajax(request):
    idlanguage = request.GET.get('idlanguage')
    idarea = request.GET.get('idarea')

    #*****************************************************
    language = LanguageCampaign.objects.get(id=idlanguage)
    area= Area.objects.get(id=idarea)
    namekeyword = request.GET.get('namekey')
   
    existeSyn= SynonymKeyword.objects.filter(name__iexact=namekeyword)
    if(existeSyn):
        print('existe el sinonimo')
        return HttpResponse('error')
    #*****************************************************
    miarea= Area.objects.filter(pk=idarea)
    idcategory = request.GET.get('idcategory')
    idsubcategory = request.GET.get('idsubcategory')
    add_key = False
    #si es el ultimo nivel, agrego la palabra clave
        
    if idsubcategory != 0 and idsubcategory != None: #estoy en el ultimo nivel, agrego la keyword
        add_key = True
    elif idcategory != 0 and idcategory != None: #quizas posea alguna subcategoria
        subnivel= SubCategory.objects.filter(relationship=idcategory).count()
        if subnivel > 0: #posee subniveles, entonces no agrego la key
            return HttpResponse('nivelfail')
        else: #no posee subniveles, agrego
            add_key = True
    else: #quizas posea alguna categoria
        subnivel= Category.objects.filter(relationship=idarea).count()
        if subnivel > 0: #posee subniveles, entonces no agrego la key
            print('--------->el area posee al menos un subnivel, no fue posible agregar la palabra clave')
            return HttpResponse('nivelfail')
        else: #no posee subniveles, agrego
            add_key = True
            print('3')

    if namekeyword == '' or namekeyword is None:
        return HttpResponse('fail')

    else:
        
        if idcategory == 0 or idcategory == None:
            category= None
            
        else:
            category= Category.objects.get(pk=idcategory)

        if idsubcategory == 0 or idsubcategory == None:
            subcategory= None

        else:
            subcategory= SubCategory.objects.get(pk=idsubcategory)

        if add_key== True: #estoy en el ultimo nivel, puedo guardar la palabra
            Keyword.objects.create(
                name= namekeyword,
                category= category,
                area= area,
                subcategory = subcategory,
                language = language)

    return redirect('AdminUserCrm')
        

class DeleteKeywordCrm(DeleteView):
    model = Keyword
    template_name = "crm/admin/confirm_delete_keyword.html"
    success_url = reverse_lazy('AdminCategoryCrm')

class UpdateKeywordCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.marketing_user'
    model = Keyword
    fields = ['name', 'description', 'language', 'image'] 
    template_name = "crm/admin/confirm_update_keyword.html"
    success_url = reverse_lazy('AdminCategoryCrm')

    def post(self, request, *args, **kwargs):
        pk_key=self.kwargs['pk']

        mykey=Keyword.objects.get(pk=pk_key)
        mykey.name = request.POST.get('name')
        mykey.description = request.POST.get('description')
        languageInstance = LanguageCampaign.objects.get(pk=request.POST.get('language'))
        mykey.language = languageInstance
        if request.FILES.get('image') is not None:
            mykey.image = request.FILES.get('image')
        else:
            if request.POST.get('image-clear') is not None:
                mykey.image = request.FILES.get('image')
        mykey.save()

        area= mykey.area.pk
        categorya= mykey.category
        if categorya != None:
            category= categorya.pk
        else:
            category=0
        subcategorya=mykey.subcategory
        if subcategorya != None:
            subcategory=subcategorya.pk
        else:
            subcategory=0
        
        return HttpResponseRedirect(reverse('UpdateAdminCategoryKeywordCrm', kwargs={ 'area':area, 'category':category, 'subcategory':subcategory}))

class DeleteSubCategoryCrm(DeleteView):
    model = SubCategory
    template_name = 'crm/admin/confirm_delete_subcategory.html'
    success_url = reverse_lazy('AdminCategoryCrm')

class DeleteCategoryCrm(DeleteView):
    model = Category
    template_name = 'crm/admin/confirm_delete_category.html'
    success_url = reverse_lazy('AdminCategoryCrm')

class DeleteAreaCrm(DeleteView):
    model = Area
    template_name = 'crm/admin/confirm_delete_area.html'
    success_url = reverse_lazy('AdminCategoryCrm')

#Module: Privacy - System
class PrivacyPolicyCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.system_user'
    template_name = "crm/admin/privacies_policies.html"
    model = PolicyPrivacyModel

class CreatePrivacyPolicyCrm(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.system_user'
    model = PolicyPrivacyModel
    fields= '__all__'
    template_name = 'crm/admin/create_privacies_policies.html'
    success_url = reverse_lazy('PrivacyPolicyCrm')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            pk = request.POST.get('language')
            mylang= LanguageCampaign.objects.get(pk=pk)
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
                return HttpResponseRedirect(reverse_lazy('CreatePrivacyPolicyCrm'))
            newPrivacy = PolicyPrivacyModel(
                    language= mylang,
                    description= mydesc)
            existe= PolicyPrivacyModel.objects.filter(language= pk).count()
            if(existe== 0): #si no existen politicas para ese idioma, las creo. si existe una, la actualizo
                newPrivacy.save()
                return HttpResponseRedirect(reverse_lazy('PrivacyPolicyCrm'))
            else:
                PolicyPrivacyModel.objects.get(language=pk).delete()
                newPrivacy.save()
                return HttpResponseRedirect(reverse_lazy('PrivacyPolicyCrm'))
       
class UpdatePrivacyPolicyCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.system_user'
    model = PolicyPrivacyModel
    fields = ['description']
    template_name = "crm/admin/update_privacypolicy.html"
    success_url = reverse_lazy('PrivacyPolicyCrm')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            send = PolicyPrivacyModel.objects.get(pk=self.kwargs.get('pk'))
            mydesc = request.POST.get('description')
            if mydesc=='' or mydesc.isspace() or mydesc==None or mydesc.isdigit() or mydesc=='<p><br></p>' or mydesc=='<br><p></p>':
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
                return HttpResponseRedirect(reverse_lazy('UpdatePrivacyPolicyCrm', kwargs={'pk':self.kwargs.get('pk')}))
                #return reverse('UpdatePrivacyPolicyCrm', kwargs={'pk': 7})
            send.description = request.POST.get('description')
            send.save()
            return HttpResponseRedirect(reverse_lazy('PrivacyPolicyCrm'))

@permission_required('usercustom.marketing_user')
def CategoriesCrmDelete(request):
    id = request.POST.get('value')
    model = request.POST.get('model')
    if model == 'sc':
        my_category = SubCategory.objects.get(id=id)
        my_category.delete()
    elif model == 'cat':
        my_category = Category.objects.get(id=id)
        my_category.delete()
    else:
        my_category = Area.objects.get(id=id)
        my_category.delete()
    return HttpResponse('Ok')

@permission_required('usercustom.marketing_user')
def KeywordsCrmDelete(request):
    id = request.POST.get('value')
    my_key = Keyword.objects.get(id=id)
    my_key.delete()
    return HttpResponse('Ok')

@permission_required('usercustom.marketing_user')
def Order_categories_admin(request):
    elementos_ordenados = request.GET.get('orden')
    separador = ","
    lista_ordenada = elementos_ordenados.split(separador)
    i=1
    for elemento in lista_ordenada:
        if elemento == '' or elemento == None:
            print('')
        else:
            id_categoria= elemento
            categoria = Category.objects.get(pk = id_categoria)
            categoria.posicion= i
            categoria.date = datetime.today()
            categoria.save()
        i= i+1

    return HttpResponse('Ok')

@permission_required('usercustom.marketing_user')
def Order_subcategories_admin(request):
    elementos_ordenados = request.GET.get('orden')
    separador = ","
    lista_ordenada = elementos_ordenados.split(separador)
    i=1
    for elemento in lista_ordenada:
        if elemento == '' or elemento == None:
            print('')
        else:
            id_scategoria= elemento
            scategoria = SubCategory.objects.get(pk = id_scategoria)
            scategoria.posicion= i
            scategoria.date = datetime.today()
            scategoria.save()
        i= i+1

    return HttpResponse('Ok')

@permission_required('usercustom.marketing_user')
def Order_areas_admin(request):
    elementos_ordenados = request.GET.get('orden')
    separador = ","
    lista_ordenada = elementos_ordenados.split(separador)
    i=1
    for elemento in lista_ordenada:
        if elemento == '' or elemento == None:
            print('')
        else:
            id_area= elemento
            area = Area.objects.get(pk = id_area)
            area.posicion= i
            area.date = datetime.today()
            area.save()
        i= i+1
    return HttpResponse('Ok')

def Order_keywords_admin(request):
    elementos_ordenados = request.POST.get('orden')
    print(elementos_ordenados)
    separador = ","
    lista_ordenada = elementos_ordenados.split(separador)
    i=1
    for elemento in lista_ordenada:
        if elemento == '' or elemento == None or elemento.isdigit()==False:
            print(elemento)
        else:
            id_key= elemento
            keyword = Keyword.objects.get(pk = id_key)
            keyword.posicion= i
            keyword.save()
            print('/////////////////////////')
            print(keyword.posicion)

        i= i+1
    return HttpResponse('Ok')

@permission_required('usercustom.marketing_user')
def KeywordDelete(request):
    id = request.POST.get('value')
    my_keyword = SuggestionKeyword.objects.get(id=id)
    my_keyword.delete()
    return HttpResponse('Ok')
    

def dismiss_product_ajax(request):
    idproduct = request.GET.get('pk')
    miproduct= Product.objects.get(pk=idproduct)
    idcompany= miproduct.company
    Product.objects.filter(pk=idproduct).delete()
    miuser= User.objects.get(company_id=idcompany)
    send_mail('Medcombo- Notificación Producto', 'Lo sentimos, su solicitud ha sido rechazada.',
        'Medcombo@gmail.com',
            [miuser.email],
            fail_silently= True,
            )
    return HttpResponse('Ok')

def add_synonym(request):
    synonym_name = request.POST.get('synonym')
    key_id = request.POST.get('key')
    synonym_id = request.POST.get('synonym_id')
    #ahora debo consultar si la palabra ya existe en la tabla keyword, y mandar un mensaje de error
    print(synonym_name)
    print(key_id)
    existeKey= Keyword.objects.filter(name__iexact=synonym_name)
    if(existeKey):
        print('ya existe esta keyword')
        return HttpResponse('error')
    else:
        existeSyn= SynonymKeyword.objects.filter(name__iexact=synonym_name)
        if(existeSyn):
            print('existe el sinonimo')
            return HttpResponse('error')
        else:
            if synonym_id == "-1":
                keyword=Keyword.objects.get(pk=key_id)
                
                SynonymKeyword.objects.create(
                    name= synonym_name,
                    keyword = keyword)
            else:
                aaa = SynonymKeyword.objects.get(id=synonym_id)
                aaa.name = synonym_name
                aaa.save()

    return HttpResponse('guardado')

def delete_synonym(request):
    synonym_id = request.POST.get('synonym_id')
    SynonymKeyword.objects.filter(id=synonym_id).delete()
    return HttpResponse('guardado')

