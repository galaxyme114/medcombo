from django.shortcuts import get_object_or_404
from pure_pagination.mixins import PaginationMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import CreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse

#Module: Groups - System
class ListGroups(PermissionRequiredMixin, PaginationMixin, ListView):
    permission_required = 'usercustom.system_user'
    template_name = 'configuration/usercustom/groups/list.html'
    model = Group
    paginate_by = 10

class DetailGroups(LoginRequiredMixin, DetailView):
    template_name = 'configuration/usercustom/groups/detail.html'
    model = Group
    paginate_by = 1

class CreateGroups(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.system_user'
    form_class = CreateForm
    template_name = 'configuration/usercustom/groups/create.html'
    success_url = reverse_lazy('list_groups')

class UpdateGroups(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.system_user'
    template_name = 'configuration/usercustom/groups/update.html'
    model = Group
    form_class = CreateForm

    def get_success_url(self):
        return reverse('list_groups')

class DeleteGroups(LoginRequiredMixin, DeleteView):
    template_name = 'configuration/usercustom/groups/delete.html'
    model = Group
    success_url = reverse_lazy('list_groups')

@permission_required('usercustom.system_user')
def DeleteGroupActive(request):
    id = request.POST.get('value')
    opportunity = Group.objects.get(id=id)
    opportunity.delete()
    return HttpResponse('Ok')