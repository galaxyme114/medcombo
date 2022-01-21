from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from django.views.generic.edit import CreateView, BaseCreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post
from medcombo.myweb.dashboard_client.post.forms import PostForm
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.list import BaseListView
from django.shortcuts import render_to_response
from dal import autocomplete

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from medcombo.crm.dashboard_admin.models import LanguageCampaign

class PostUpdate(LoginRequiredMixin, UpdateView):
	model= Post
	template_name= "myweb/dashboard_client/post/update.html"
	fields='__all__'
	success_url="/post_createList"


class PostDelete(LoginRequiredMixin, DeleteView):
	model= Post
	template_name= "myweb/dashboard_client/post/delete.html"
	success_url="/post_createList"


class ListAndCreate(LoginRequiredMixin, CreateView):
	model =Post
	fields= '__all__'
	template_name= "myweb/dashboard_client/post/create.html"
	success_url = "/post_createList" 

	def get_context_data(self, **kwargs):
		context = super(ListAndCreate, self).get_context_data(**kwargs)
		context['objects'] = Post.objects.all().order_by('-pk')
		#context['language_filter'] = LanguageCampaign.objects.all().order_by('value_language')

		return context

@login_required
def load_post(request):
    title = request.GET.get('postes')
    post = Post.objects.filter(title__icontains=title).order_by('-pk')
    print(title)
    return render(request, 'myweb/dashboard_client/post/search_post.html', {'postes': post})

class DeleteUpdatePost(DetailView):
    model = Post
    template_name = "myweb/dashboard_client/post/confirm_delete_update_post.html"

    def post(self, request, *args, **kwargs):
    	action = request.POST.get('action')
    	idpost = request.POST.get('idpost')
    	if action == 'eliminar':
    		Post.objects.filter(pk=idpost).delete()
    		return HttpResponseRedirect(reverse_lazy('post_createList'))
    	else:
    		return HttpResponseRedirect(reverse_lazy('post_update', kwargs={'pk': idpost}))

class PostDetail(DetailView):
    model = Post
    template_name = "myweb/dashboard_client/post/detail_post.html"

def PostDeleteAjax(request):
    id = request.POST.get('value')
    my_post = Post.objects.get(id=id)
    my_post.delete()
    return HttpResponse('Ok')
    	
        

	

