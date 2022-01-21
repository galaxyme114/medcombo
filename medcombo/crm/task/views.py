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
from .models import Task, CallTask
from .forms import TaskForm
from medcombo.crm.opportunity.models import HistoryOpportunity
from medcombo.configuration.usercustom.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import translation
from medcombo.crm.dashboard_admin.models import LanguageCampaign


class CreateTaskCrm(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = Task
    fields = '__all__'
    template_name = "crm/task/create.html"
    #success_url = reverse_lazy('ListTaskCrm')

    def get_context_data(self, **kwargs):
            context = super(CreateTaskCrm, self).get_context_data(**kwargs)
            actual_lang = translation.get_language()
            if actual_lang == 'en':
                formulario = CallTask.objects.filter(language_id=3)
            if actual_lang == 'es':
                formulario = CallTask.objects.filter(language_id=4)
            if actual_lang == 'it':
                formulario = CallTask.objects.filter(language_id=6)
            if actual_lang == 'pt':
                formulario = CallTask.objects.filter(language_id=7)
            if actual_lang == 'de':
                formulario = CallTask.objects.filter(language_id=2)
            if actual_lang == 'fr':
                formulario = CallTask.objects.filter(language_id=5)
            if actual_lang == 'ja':
                formulario = CallTask.objects.filter(language_id=9)
            if actual_lang == 'zh-hans':
                formulario = CallTask.objects.filter(language_id=8)
            if actual_lang == 'zh-hant':
                formulario = CallTask.objects.filter(language_id=1)
            context['call']= 0
            context['formulario'] = formulario
            return context

    def get_success_url(self):
        language=LanguageCampaign.objects.get(value_language= translation.get_language())
        task = Task.objects.get(id=self.object.pk)
        task_call_id = self.request.POST.get('call')
        micalltask= CallTask.objects.get(pk=task_call_id)
        task.done = True
        task.call=micalltask
        task.language= language
        task.save()
        return reverse('ListTaskCrm') 

#Module: Task - sales
class ListTaskCrm(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    model = Task
    #ordering = ['-id']
    template_name = "crm/task/list.html"

    def get_queryset(self):
        return Task.objects.filter(done=True).order_by('-id')

class ReadyTaskCrm(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = HistoryOpportunity
    fields = '__all__'
    template_name = "crm/task/ready.html"
    #success_url = reverse_lazy('ListTaskCrm')

    def get_context_data(self, **kwargs):
        context = super(ReadyTaskCrm, self).get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs.get('pk'))
        return context
    
    def get_success_url(self):
        task = Task.objects.get(id=self.kwargs.get('pk'))
        task.done = False
        task.save()
        return reverse('ListTaskCrm')  

class UpdateTaskCrm(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.sales_user'
    model = Task
    #fields = '__all__'
    form_class = TaskForm
    template_name = "crm/task/create.html"
    success_url = reverse_lazy('ListTaskCrm')

    def get_context_data(self, **kwargs):
        context = super(UpdateTaskCrm, self).get_context_data(**kwargs)
        pk= self.kwargs['pk']
        if pk:
            mytask= Task.objects.get(pk=pk)
            mytaskcall_id= mytask.call
            if mytaskcall_id:
                idtaskcall= mytaskcall_id.id #el id que voy a cargar en el select
            else:
                idtaskcall=0
        else:
            idtaskcall= 0
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            formulario = CallTask.objects.filter(language_id=3)
        if actual_lang == 'es':
            formulario = CallTask.objects.filter(language_id=4)
        if actual_lang == 'it':
            formulario = CallTask.objects.filter(language_id=6)
        if actual_lang == 'pt':
            formulario = CallTask.objects.filter(language_id=7)
        if actual_lang == 'de':
            formulario = CallTask.objects.filter(language_id=2)
        if actual_lang == 'fr':
            formulario = CallTask.objects.filter(language_id=5)
        if actual_lang == 'ja':
            formulario = CallTask.objects.filter(language_id=9)
        if actual_lang == 'zh-hans':
            formulario = CallTask.objects.filter(language_id=8)
        if actual_lang == 'zh-hant':
            formulario = CallTask.objects.filter(language_id=1)
        context['call']= idtaskcall
        context['formulario'] = formulario
        return context

    def get_success_url(self):
        call=self.request.POST.get('call')
        print(call)
        call_instance= CallTask.objects.get(pk=call)
        Task.objects.filter(pk=self.object.pk).update(call=call_instance)
        """get_success_url."""
        return reverse('ListTaskCrm')

class DeleteTaskCrm(LoginRequiredMixin, DeleteView):
	model = Task
	template_name = "crm/task/delete.html"
	success_url = reverse_lazy('ListTaskCrm')

@permission_required('usercustom.sales_user')
def TaskDelete(request):
    id = request.POST.get('value')
    my_task = Task.objects.get(id=id)
    my_task.delete()
    return HttpResponse('Ok')

class AppointmentBook(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    template_name = "crm/task/appointment_books.html"
    model = Task

    def get_context_data( self, **kwargs):
        context = super(AppointmentBook, self).get_context_data(**kwargs)
        pks= self.kwargs.get('pk')
        print('get_context_data')
        print(pks)
        context['users'] = User.objects.filter(employee= True)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            pk_empleado = request.POST.get('empleado')
            print('post')
            print(pk_empleado)
        return HttpResponseRedirect(reverse_lazy('AppointmentBookCrm'))

def AppointmentBook(request, pk_empleado):
    #el metodo get carga el area, categoria y subcategoria, keywords seleccionados
    print('*************************************')
    print(pk_empleado)
    id_empleado= pk_empleado
    users = User.objects.filter(employee= True)
    actual_lang = translation.get_language()
    if actual_lang == 'en':
        language= 3
    if actual_lang == 'es':
        language= 4
    if actual_lang == 'it':
        language= 6
    if actual_lang == 'pt':
        language= 7
    if actual_lang == 'de':
        language= 2
    if actual_lang == 'fr':
        language= 5
    if actual_lang == 'ja':
        language= 9
    if actual_lang == 'zh-hans':
        language= 8
    if actual_lang == 'zh-hant':
        language= 1
    if id_empleado == '0': #si no mando un id especifico, los traigo a todos
        task= Task.objects.filter(done= True, language=language)
    else:
       task= Task.objects.filter(responsible= id_empleado, done = True, language=language)
    if request.method == 'POST':
        print('desde el post')
        id_empleado= request.POST.get('empleado')
        print(id_empleado)
        users = User.objects.filter(employee= True)
        task= Task.objects.filter(responsible= id_empleado, done= True, language=language)
        return HttpResponseRedirect(reverse_lazy('AppointmentBookCrm', kwargs={'pk_empleado': id_empleado}))
    return render(request, 'crm/task/appointment_books.html', {'pk_empleado': id_empleado,'users': users, 'tasks': task})

class AppointmentBookDetail( DetailView):
    template_name = 'crm/task/appointment_books_detail.html'
    model = Task
