from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from medcombo.product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

class CreateProductCrm(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = Product
    fields = ['name', 'product_ID', 'price', 'company', 'ref', 'notes']
    template_name = "crm/product/create.html"
    success_url = reverse_lazy('ListProductCrm')

    def get_success_url(self):
        return reverse('ListProductCrm')

#Module: Product - sales
class ListProductCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    queryset = Product.objects.filter(company=1)
    context_object_name = 'product'
    template_name = "crm/product/list.html"

class UpdateProductCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.sales_user'
    model = Product
    fields = ['name', 'product_ID', 'price', 'ref', 'notes']
    template_name = "crm/product/update.html"
    success_url = reverse_lazy('ListProductCrm')

class DetailProductCrm(PermissionRequiredMixin, DetailView):
    permission_required = 'usercustom.sales_user'
    model = Product
    template_name = "crm/product/detail.html"

class DeleteProductCrm(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "crm/product/delete.html"

@permission_required('usercustom.sales_user')
def DeleteCrmProduct(request):
    id = request.POST.get('value')
    my_product = Product.objects.get(id=id)
    my_product.delete()
    return HttpResponse('Ok')
