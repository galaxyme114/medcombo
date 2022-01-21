from django.views.generic.detail import DetailView
from medcombo.configuration.company.models import Company, DescriptionCompany
from medcombo.social_network.contacts.models import Contacts
from django.contrib.auth.mixins import LoginRequiredMixin
from medcombo.product.models import Product, FavoriteProduct, BannerWeb
from medcombo.myweb.dashboard_client.post.models import Post
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation
from django.urls import reverse, reverse_lazy
from medcombo.myweb.catalogue.models import Catalogue


def MywebHomeDetail(request, pk): 
    print(pk)
    if pk == '1':
        return render(request, 'myweb/dashboard_client/index.html')

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
    iduser_logueado = request.user.id
    descriptions= DescriptionCompany.objects.filter(company_id= pk, language_id= idlang )
    if (descriptions):
        print('existe')
    else:
        descriptions= DescriptionCompany.objects.filter(company_id= pk, language_id= '3' )
    company= Company.objects.get(id=pk)
    if request.method== 'GET':
        if iduser_logueado == None:
            print('1')
            if company.approved==True: 
                print('2')
                banner = BannerWeb.objects.filter(banner_company= pk, language_campaign= idlang )
                return render(request, 'myweb/public/home.html', {'company': company, 'descriptions': descriptions, 'banner': banner})
            else:
                return redirect('view_login') #el redirect me cambia la url, los otros solo cambian la pantalla pero no la url. 
        else:
            print('3')
            print(request.user.company)
            if request.user.company == None:
                print('1')
                if company.approved == True:
                    print('2')
                    banner = BannerWeb.objects.filter(banner_company= pk, language_campaign= idlang )
                    return render(request, 'myweb/public/home.html', {'company': company, 'descriptions': descriptions, 'banner': banner})
                else:
                    print('3')
                    return render(request, 'myweb/dashboard_client/index.html')
            elif company.approved==True or request.user.company.id == company.id:
                print('4')
                banner = BannerWeb.objects.filter(banner_company= pk, language_campaign= idlang )
                return render(request, 'myweb/public/home.html', {'company': company, 'descriptions': descriptions, 'banner': banner})
            else:
                return render(request, 'myweb/dashboard_client/index.html')

class MywebProductList(DetailView):
    model = Company
    template_name = "myweb/public/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('***************************************** favoritos **************************************')
        favoritos = FavoriteProduct.objects.all().filter(user_id= self.request.user.id)
        print(favoritos.count())
        print('***************************************** favoritos **************************************')

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
        banner = BannerWeb.objects.filter(banner_company= self.kwargs.get('pk'), language_campaign= idlang )
        context['favoritos'] = favoritos
        context['banner'] = banner
        return context

class MywebCatalogueList(DetailView):
    model = Company
    template_name = "myweb/public/catalogue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favoritos = FavoriteProduct.objects.all().filter(user_id= self.request.user.id)
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
        catalogue = Catalogue.objects.filter(company=self.kwargs.get('pk'), language=idlang)
        banner = BannerWeb.objects.filter(banner_company= self.kwargs.get('pk'), language_campaign= idlang )
        context['banner'] = banner
        context['catalogue'] = catalogue
        return context
    

class MywebContact(DetailView):
    model = Company
    template_name = "myweb/public/contact.html"

    def get_context_data(self, **kwargs):
        context = super(MywebContact, self).get_context_data(**kwargs)
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
        banner = BannerWeb.objects.filter(banner_company= self.kwargs.get('pk'), language_campaign= idlang )
        contactos = Contacts.objects.all()
        context['contactos'] = contactos
        context['banner'] = banner
        return context

class MywebNewsList(DetailView):
    model = Company
    template_name = "myweb/public/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favoritos = FavoriteProduct.objects.all().filter(user_id= self.request.user.id)
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
        banner = BannerWeb.objects.filter(banner_company= self.kwargs.get('pk'), language_campaign= idlang )
        context['banner'] = banner
        return context

# class DetailPost(DetailView):
#     template_name = 'myweb/public/detail_post.html'
#     model = Post
#     #template_name = "myweb/dashboard_client/post/detail_post.html"

class DetailPost(DetailView):
    template_name = 'myweb/public/detail_product2.html'
    model = Product