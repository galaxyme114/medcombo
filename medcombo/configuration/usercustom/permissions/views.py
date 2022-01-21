from pure_pagination.mixins import PaginationMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import FormPermissions, FormPermissionsGroups
from medcombo.configuration.usercustom.models import User, Work
from django.contrib.auth.models import Group
from medcombo.configuration.usercustom.forms import SingupFormAdmin, SingupFormAdmin_en,SingupFormAdmin_de,SingupFormAdmin_zh, SingupFormAdmin_zhh,SingupFormAdmin_fr,SingupFormAdmin_it,SingupFormAdmin_pt,SingupFormAdmin_ja, SingupEmployForm, ChangePassFormAdmin, SingupEmployFormUpdate, SingupEmployFormUpdatePassword
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from medcombo.product.models import CsvArchivo, Product
from medcombo.myweb.dashboard_client.post.models import Post
from django.utils.crypto import get_random_string
import os.path
from cities_light.models import Country
from medcombo.configuration.company.forms import CityForm
from django.shortcuts import render
from medcombo.configuration.company.models import Company, BoostingCompany
from medcombo.configuration.usercustom.models import UserOnline
from django.utils import translation
from medcombo.configuration.usercustom.models import Userrunning_system

from medcombo.crm.dashboard_admin.models import LanguageCampaign
import pandas as pd
from django.http import JsonResponse
from .resources import UserResource
import datetime

class ListUsersPermission(PermissionRequiredMixin, PaginationMixin, ListView):
    permission_required = 'auth.add_permission'
    template_name = 'configuration/usercustom/permissions/list.html'
    model = User
    paginate_by = 10
    ordering = ['-date_joined']

class UpdatePermission(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_permission'
    template_name = 'configuration/usercustom/permissions/update.html'
    model = User
    form_class = FormPermissions

    def get_success_url(self):
        return reverse('list_permission')

class UpdatePermissionGroups(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_permission'
    template_name = 'configuration/usercustom/permissions/update_groups.html'
    model = User
    form_class = FormPermissionsGroups

    def get_success_url(self):
        return reverse('list_permission')

def DeleteUserRegister(request):
    id = request.POST.get('user')
    user_delete = User.objects.get(id=id)
    user_delete.is_active = False
    user_delete.save()
    return HttpResponse('Ok')

def ActiveUserRegister(request):
    id = request.POST.get('user')
    user_delete = User.objects.get(id=id)
    user_delete.is_active = True
    user_delete.save()
    return HttpResponse('Ok')

def ImportUserAdmin(request):
    
    if request.method == 'POST':
        org_column_names = ["Language", "First Name", "Last Name", "Email", "Country", "Telephone", "Work", "Company"]
        filename = str(request.FILES['file'])
        if filename.endswith('.csv') or filename.endswith(".xls"):
            existenCSV = CsvArchivo.objects.all().count()
            if(existenCSV > 0):
                CsvArchivo.objects.get().delete()
            objeto = CsvArchivo(
                name = request.FILES['file'],
                file = request.FILES.get('file')
                )
            objeto.save()
            archivo = CsvArchivo.objects.get()
            ruta= archivo.file.url
            
            print(ruta, "########")
            from django.conf import settings
            import urllib.request
            if str(ruta).startswith('http'):
                # production server
                full_url = ruta
            else:
                # local server
                full_url = "http://"+request.META['HTTP_HOST'] + str(ruta)
            print(full_url, "##########")
            
            if filename.endswith('.csv'):
                path = "temp.csv"
            else:
                path = "temp.xls"
            
            response = urllib.request.urlretrieve(full_url)
            contents = open(response[0]).read()
            
            f = open(path,'w')
            f.write(contents)
            f.close()
            
            if filename.endswith('.csv'):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)
            
            df.fillna("", inplace=True)
            column_names = list(df)
            dif_len = len(list(set(org_column_names) - set(column_names)))

            if dif_len == 0:
                record_count = len(df.index)
                success_record = 0
                failed_record = 0
                exist_record = 0
                for index, row in df.iterrows():
                    user_new = User.objects.filter(lead=False).filter(employee=False)
                    my_list = []
                    if user_new.count() == 0:
                        username = 10000
                    else:
                        for user in user_new:
                            value = str(user.username).isdigit()
                            if value == True:
                                my_list.append(int(user.username))
                            order = sorted(my_list, key=int, reverse=True)
                            if order:
                                username = order[0] + 1
                            else:
                                username = 10000
                    try:
                        languageInstance = LanguageCampaign.objects.get(value_language=row["Language"])
                        workInstance = Work.objects.get(name=row["Work"], language= languageInstance.pk)
                        countryInstance = Country.objects.get(name=row["Country"])
                    except Exception as e:
                        print(e)
                        failed_record += 1
                        continue
                    try:
                        companyInstance = Company.objects.get(name=row["Company"])
                    except:
                        companyInstance = None
                    print(companyInstance, countryInstance, languageInstance)
                    
                    #123medcombo clave por defecto
                    crearUsuario = User(
                        password= 'pbkdf2_sha256$100000$8uPQuUkzqmw7$fMm/sEgvKwpPCt8fMVdG3s5xU+PTiwNOyP4GItjIgzk=',
                        username= username,
                        first_name=row["First Name"],
                        last_name=row["Last Name"],
                        email= row["Email"],
                        country= countryInstance,
                        telephone=row["Telephone"],
                        work= workInstance,
                        lead= False,
                        employee= False,
                        company= companyInstance,
                    )
                    try:
                        crearUsuario.save()
                        success_record += 1
                    except Exception as e:
                        # email is already exists
                        print(e)
                        exist_record += 1
                os.remove(path)
                return JsonResponse({'status':'true','error_code':'0', 'total': record_count, 'success': success_record, 'failed': failed_record, 'exist': exist_record})
            else:
                os.remove(path)
                # column count is not equals
                return JsonResponse({'status':'false','error_code':'1'})
        else:
            # files should be csv, or xls 
           return JsonResponse({'status':'false','error_code':'2'})

    return HttpResponse("Ok")

def ExportUserAdmin(request):
    person_resource = UserResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    return response
    
#Module: Users - Sales
class ListUserSalesAdmin(PermissionRequiredMixin, ListView): 
    permission_required = 'usercustom.sales_user'
    template_name = 'configuration/usercustom/permissions/list_admin_sales.html'
    model = User
    #ordering = ['-date_joined']
    #paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(lead=False,employee=False).order_by('-date_joined')

@login_required
def SaleUserDelete(request):
    remove = request.POST.getlist('remove[]')
    if remove:
        for each in remove:
            if each != "":
                Del = User.objects.get(pk=int(each))
                Del.delete()
            else:
                print("this is empty string!")

        return HttpResponse('OK')
    else:
        return HttpResponse('NO')

#Module: Users - Management
class ListUserAdmin(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.management_user'
    template_name = 'configuration/usercustom/permissions/list_admin.html'
    model = User
    #ordering = ['-date_joined']
    #paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(lead=False,employee=False).order_by('-date_joined')

#Module: Employee - System
class ListEmployAdmin(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.system_user'
    template_name = 'configuration/usercustom/permissions/employ_admin.html'
    model = User
    #ordering = ['-date_joined']
    #paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(employee=True).order_by('-date_joined')

class CreateUserEmploy(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.system_user'
    model = User
    form_class = SingupEmployForm
    template_name = 'configuration/usercustom/permissions/create_employ.html'
    success_url = reverse_lazy('admin_employ_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        groups = request.POST.getlist('groups')
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name= name
            user.last_name= surname
            user.save()
            new_user = User.objects.get(id=user.pk)
            for g in groups:
                group = Group.objects.get(id=g)
                new_user.groups.add(group)
            new_active_user = UserOnline(user=new_user,active=False)
            new_active_user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UpdateEmploy(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.system_user'
    template_name = 'configuration/usercustom/permissions/update_employ.html'
    model = User
    #fields = ['first_name', 'last_name', 'email', 'groups']
    form_class = SingupEmployFormUpdate

    def get_success_url(self):
        return reverse('admin_employ_list')
    
    def get_context_data(self, **kwargs):
        context = super(UpdateEmploy,self).get_context_data(**kwargs)
        user = User.objects.get(id = self.kwargs.get('pk'))
        context['employ'] = user.username
        return context

@permission_required('usercustom.system_user')
def EmployeeDelete(request):
    id = request.POST.get('user')
    my_contact = User.objects.get(id=id)
    my_contact.delete()
    return HttpResponse('Ok')

class UpdateEmployPassword(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.system_user'
    template_name = 'configuration/usercustom/permissions/change_employee_password.html'
    model = User
    #fields = ['first_name', 'last_name', 'email', 'groups']
    form_class = SingupEmployFormUpdatePassword

    def get_success_url(self):
        return reverse('admin_employ_list')
    
    def get_context_data(self, **kwargs):
        context = super(UpdateEmployPassword,self).get_context_data(**kwargs)
        user = User.objects.get(id = self.kwargs.get('pk'))
        context['employ'] = user.username
        return context

class CreateUserAdmin(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = User
    form_class = SingupFormAdmin
    form_class3 = SingupFormAdmin_en
    form_class5 = SingupFormAdmin_fr
    form_class6 = SingupFormAdmin_it
    form_class7 = SingupFormAdmin_pt
    form_class8 = SingupFormAdmin_zh
    form_class9 = SingupFormAdmin_ja
    form_class1 = SingupFormAdmin_zhh
    form_class2 = SingupFormAdmin_de
    template_name = 'configuration/usercustom/permissions/create_user.html'
    success_url = reverse_lazy('admin_user_sales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            formulario = SingupFormAdmin_en
        if actual_lang == 'es':
            formulario = SingupFormAdmin
        if actual_lang == 'it':
            formulario = SingupFormAdmin_it
        if actual_lang == 'pt':
            formulario = SingupFormAdmin_pt
        if actual_lang == 'de':
            formulario = SingupFormAdmin_de
        if actual_lang == 'fr':
            formulario = SingupFormAdmin_fr
        if actual_lang == 'ja':
            formulario = SingupFormAdmin_ja
        if actual_lang == 'zh-hans':
            formulario = SingupFormAdmin_zh
        if actual_lang == 'zh-hant':
            formulario = SingupFormAdmin_zhh
        print(actual_lang)
        context['formulario'] = formulario
        return context

    def post(self, request, *args, **kwargs):
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
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        country = request.POST.get('country')
        
        if workid.isdigit()==False or first_name=='' or first_name.isspace() or first_name==None or last_name=='' or last_name.isspace() or last_name==None or  password1=='' or password1.isspace() or password1==None or password2=='' or password2.isspace() or password2==None or password2!=password1:
            return HttpResponseRedirect(reverse_lazy('admin_user_create'))
        work= Work.objects.get(pk=workid)
        #form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.work= work
            user.save()
            new_user = User.objects.get(id=user.pk)
            new_active_user = UserOnline(user=new_user,active=False)
            new_active_user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

@permission_required('usercustom.management_user')
def UserDeleteAdmin(request):
    id = request.POST.get('user')
    my_user = User.objects.get(id=id)
    if my_user.company is None:
        my_user.delete()
    else:
        my_company = Company.objects.get(id=my_user.company.id)
        my_company.delete()
        my_user.delete()
    return HttpResponse('Ok')

class UpdateUsersAdmin(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.sales_user'
    template_name = 'configuration/usercustom/permissions/update_user.html'
    model = User
    fields = ['country', 'first_name','last_name']

    def get_context_data(self, **kwargs):
        context = super(UpdateUsersAdmin,self).get_context_data(**kwargs)
        my_user = User.objects.get(id=self.kwargs.get('pk'))
        connected = Userrunning_system.objects.filter(user_id=my_user.id)
        if my_user.company:
            products = Product.objects.filter(company=my_user.company.id).count()
            posts = Post.objects.filter(company=my_user.company.id).count()
        else:
            products = 0
            posts = 0

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

        sum = float()
        if connected:
            for connected_time in connected:
                sum += abs(connected_time.end - connected_time.start).total_seconds() 
            sum_time = int(str(sum).split(".")[0])
            conversion = datetime.timedelta(seconds=sum_time)
            converted_time = str(conversion)

            context['connected_time'] = converted_time
            
        else:
            sum = 0 
            context['connected_time'] = sum
        context['work']= idwork
        context['formulario'] = formulario

        context['username_user'] = my_user.username
        context['product_user'] = products
        context['post_user'] = posts
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user_id = self.kwargs['pk']
            work=request.POST.get('work')
            country=request.POST.get('country')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            print(work)
            User.objects.filter(pk=user_id).update(work=work,first_name= first_name, last_name= last_name,country=country)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_user_sales')

class UpdateUsersPassAdmin(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.management_user'
    template_name = 'configuration/usercustom/permissions/change_user_pass.html'
    model = User
    form_class = ChangePassFormAdmin
    #fields = ['password']

    def get_context_data(self, **kwargs):
        context = super(UpdateUsersPassAdmin,self).get_context_data(**kwargs)
        my_user = User.objects.get(id=self.kwargs.get('pk'))
        context['username_user'] = my_user.username
        return context

    def get_success_url(self):
        return reverse('admin_user_list')

class MyWebCompanyCreateAdmin(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.management_user'
    template_name = 'configuration/usercustom/permissions/create_myweb_admin.html'
    form_class = CityForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            objeto = form.save(commit=False)
            objeto.approved = True
            objeto.save()
            model2 = User.objects.filter(pk=self.kwargs.get('pk')).update(company=objeto.id)
            my_company = Company.objects.get(id=objeto.id)
            object_boosting = BoostingCompany(company_boosting=my_company, certification_boosting='subtracted', manufacturer_boosting='subtracted')
            object_boosting.save()
            return HttpResponseRedirect('/UserUpdateAdmin/'+self.kwargs.get('pk'))
        return render(request, self.template_name, {'form': form})  

def AcceptUser(request):
    if request.is_ajax:
        if request.method == 'POST':
            user = request.POST.get('user') #te permite recibir de un formulario, ajax
            new_user = User.objects.get(id=user)
            new_user.indicated = False
            new_user.save()
            return HttpResponse('Ok')
    return HttpResponse('Fallido')

def UpdateUserExtraName(request):
    if request.is_ajax:
        if request.method == 'POST':
            user = request.POST.get('user') #te permite recibir de un formulario, ajax
            extra_name = request.POST.get('extra')
            new_user = User.objects.get(id=user)
            new_user.extra_surename = extra_name
            new_user.save()
            return HttpResponse('Ok')
    return HttpResponse('Fallido')