from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Contacts
from medcombo.configuration.usercustom.models import User
from dal import autocomplete
from django.http import Http404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from .forms import SearchFormContact
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from medcombo.product.models import Product, FavoriteProduct
from django.db.models import Q

class FormListView(FormMixin, ListView):
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class ContactsList(LoginRequiredMixin, FormListView):
    form_class = SearchFormContact
    model = Contacts
    ordering = ['-favorite']
    template_name = 'social_network/contacts/list.html'

class ContactsSearchData(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Contacts.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(relationship__username__istartswith=self.q)
        return qs

@login_required
def add_contact(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk=user_id)
    contacts = Contacts.objects.create(relationship=user, owner=request.user, favorite= "False")
    relation = Contacts.objects.filter(relationship=request.user, owner=user)
    if not relation:
        contacts_relationship = Contacts.objects.create(relationship=request.user, owner=user, favorite= "False", notification=True)
    print("guardado normalmente")
    return render(request, 'social_network/chat/dialog.html')

@login_required
def load_contact(request):
    username = request.GET.get('user')
    user = User.objects.filter(Q(first_name__icontains=username) | Q(last_name__icontains=username))
    contacts= Contacts.objects.all().order_by('-favorite')
    #user = User.objects.get(username=user_id)
    print(user)

    return render(request, 'social_network/contacts/search_contacts.html', {'userx': user, 'contacts': contacts})

@login_required
def add_contact_favorite(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk=user_id)
    try:
        micontacto= Contacts.objects.get(relationship=user_id, owner=request.user.id)
    except Contacts.DoesNotExist:
        micontacto= None
    if(micontacto):#si el contacto no existe, lo inserto
    #si el contacto existe, solo actualizo el estado de favorito
        if micontacto.favorite== False:
            Contacts.objects.filter(relationship=user_id).update(favorite="True")
            print("actualizado a favorito")
        else:
            Contacts.objects.filter(relationship=user_id).update(favorite="False")
            print("eliminado de favorito")
    else:
        contacts = Contacts.objects.create(relationship=user, owner=request.user, favorite="True")
        relation = Contacts.objects.filter(relationship=request.user, owner=user)
        if not relation:
            contacts_relation = Contacts.objects.create(relationship=request.user, owner=user, favorite="False", notification=True)
        print("guardado favorito")
    #return render(request, 'social_network/chat/dialog.html')
    return HttpResponse("OK")

@login_required
def delete_contact(request):
    user_id = request.POST.get('value')
    contacts = Contacts.objects.get(relationship=user_id, owner=request.user.id)
    contacts.delete()
    return HttpResponse('Ok')

@login_required
def add_favoriteproduct(request):
    user_id = request.GET.get('user_id')
    product_id = request.GET.get('product_id')
    user = User.objects.get(pk=user_id)
    product = Product.objects.get(pk=product_id)
    existe= FavoriteProduct.objects.filter(user=user, product=product).count()
    if(existe == 0):
        favorito = FavoriteProduct.objects.create(user=user, product=product)
        print("agregado a favoritos")
    elif(existe > 0):
        favorito = FavoriteProduct.objects.filter(user=user, product=product).delete()
        print("eliminado de favoritos")
        return redirect('list_favorites') #el redirect me cambia la url, los otros solo cambian la pantalla pero no la url. 
    return render(request, 'social_network/chat/dialog.html')

@login_required
def ChangeStateContact(request):
    user_id = request.POST.get('value')
    contacts = Contacts.objects.get(relationship=user_id, owner=request.user.id)
    contacts.notification = False
    contacts.save()
    return HttpResponse('Ok')

@login_required
def ContactsList_detail(request):
    user_id = request.POST.get('value')
    contacts = Contacts.objects.get(relationship=user_id, owner=request.user.id)
    product_user = User.objects.get(id=contacts.relationship_id)
    if product_user.company:
        main = Product.objects.filter(company_id=product_user.company.id)
        return render(request, 'social_network/contacts/contact_detail.html', {'contacts': contacts, 'string_main':main})
    else:
        print("no exists!")
        return render(request, 'social_network/contacts/contact_detail.html', {'contacts': contacts})