from pure_pagination.mixins import PaginationMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from .models import User, UserScore, UserOnline, Work
from django.urls import reverse_lazy
from django.shortcuts import render
from django.urls import reverse
from .forms import SingupForm, SingupForm_en, SingupForm_de, SingupForm_zh, SingupForm_zhh, SingupForm_fr, SingupForm_it, SingupForm_pt, SingupForm_ja #, UserUpdateForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import os
from django.utils import translation
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from PIL import Image


class ProfileList(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = 'configuration/usercustom/list.html'
    model = User
    paginate_by = 10

class SingupView(CreateView):
    model = User
    form_class = SingupForm
    form_class3 = SingupForm_en
    form_class5 = SingupForm_fr
    form_class6 = SingupForm_it
    form_class7 = SingupForm_pt
    form_class8 = SingupForm_zh
    form_class9 = SingupForm_ja
    form_class1 = SingupForm_zhh
    form_class2 = SingupForm_de
    initial = {'key': 'value'}
    template_name = 'configuration/usercustom/singup.html'
    success_url = reverse_lazy('view_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'en':
            formulario = SingupForm_en
        if actual_lang == 'es':
            formulario = SingupForm
        if actual_lang == 'it':
            formulario = SingupForm_it
        if actual_lang == 'pt':
            formulario = SingupForm_pt
        if actual_lang == 'de':
            formulario = SingupForm_de
        if actual_lang == 'fr':
            formulario = SingupForm_fr
        if actual_lang == 'ja':
            formulario = SingupForm_ja
        if actual_lang == 'zh-hans':
            formulario = SingupForm_zh
        if actual_lang == 'zh-hant':
            formulario = SingupForm_zhh
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
        #form = self.form_class(request.POST)
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        workid = request.POST.get('work')
        if workid is None or workid == "":
            work = None
        else:
            work= Work.objects.get(pk=workid)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name= name
            user.last_name= surname
            user.work= work
            user.save()
            user_actual = User.objects.get(id=user.pk)
            new_active_user = UserOnline(user=user_actual,active=False)
            new_active_user.save()
            mail = EmailMessage('Medcombo', 'Enhorabuena, su cuenta ha sido creada satisfactoriamente! ya puede comenzar a exponer sus productos...', to=[user.email])
            mail.send()
            # send_mail('Medcombo', 'Enhorabuena, su cuenta ha sido creada satisfactoriamente! ya puede comenzar a exponer sus productos...','contacto@medcombo.es',
            # [user.email],
            # fail_silently= True,
            # )
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'configuration/usercustom/update.html'
    model = User
    fields = ['first_name', 'last_name', 'email', 'telephone','picture', 'country']
    #form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate,self).get_context_data(**kwargs)
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
        context['work']= idwork
        context['formulario'] = formulario
        return context

    """def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            objeto = form.save(commit=False)
            model2 = User.objects.all().exclude(id=self.request.user.pk)
            print(model2)
            email = request.POST.get('email')
            print(email)
            print('++++++++++++++++++++++++++')
            counter = 0
            for i in model2:
                if email == i.email:
                    counter +=1
                    print(i.email)
                    print(counter)
            if counter == 0:
                objeto.save()
                return HttpResponseRedirect(self.get_success_url())
            else: 
               return render(request, self.template_name, {'form': form}) 
        return render(request, self.template_name, {'form': form})""" 

    def get_success_url(self):
        work=self.request.POST.get('work')
        #***************************** Image Crop part ***************************************
        User_Picture = User.objects.get(pk=self.kwargs.get('pk'))
        # if User_Picture.picture:
        #     img = Image.open(User_Picture.picture.path)
        #     width, height = img.size
        #     if width > 200 and height > 200:
        #         # keep ratio but shrink down
        #         img.thumbnail((width, height))
        #         width, height = img.size

        #         # check which one is smaller
        #         if height < width:
        #             # make square by cutting off equal amounts left and right
        #             left = (width - height) / 2
        #             right = (width + height) / 2
        #             top = 0
        #             bottom = height
        #             img = img.crop((left, top, right, bottom))
        #             img.thumbnail((200, 200))
        #             img.save(User_Picture.picture.path)

        #         elif width < height:
        #             # make square by cutting off bottom
        #             left = 0
        #             right = width
        #             top = 0
        #             bottom = width
        #             img = img.crop((left, top, right, bottom))
        #             img.thumbnail((200, 200))
        #             img.save(User_Picture.picture.path)
        #         else:
        #             # already square
        #             img.thumbnail((200, 200))
        #             img.save(User_Picture.picture.path)

        #     elif width > 100 and height == 100:
        #         left = (width - 200) / 2
        #         right = (width + 200) / 2
        #         top = 0
        #         bottom = 100
        #         img = img.crop((left, top, right, bottom))
        #         img.save(User_Picture.picture.path)

        #     elif width > 200 and height < 200:
        #         left = (width - height) / 2
        #         right = (width + height) / 2
        #         top = 0
        #         bottom = height
        #         img = img.crop((left, top, right, bottom))
        #         img.save(User_Picture.picture.path)

        #     elif width < 100 and height > 200:
        #         # most potential for disaster
        #         left = 0
        #         right = width
        #         top = 0
        #         bottom = width
        #         img = img.crop((left, top, right, bottom))
        #         img.save(User_Picture.picture.path)

        #     elif width < 100 and height < 200:
        #         if height < width:
        #             left = (width - height) / 2
        #             right = (width + height) / 2
        #             top = 0
        #             bottom = height
        #             img = img.crop((left, top, right, bottom))
        #             img.save(User_Picture.picture.path)
        #         elif width < height:
        #             height = width
        #             left = 0
        #             right = width
        #             top = 0
        #             bottom = height
        #             img = img.crop((left, top, right, bottom))
        #             img.save(User_Picture.picture.path)
        #         else:
        #             img.save(User_Picture.picture.path)

        #     elif width == 200 and height > 200:
        #         # potential for disaster
        #         left = 0
        #         right = 100
        #         top = 0
        #         bottom = 100
        #         img = img.crop((left, top, right, bottom))
        #         img.save(User_Picture.picture.path)

        #     elif width == 200 and height < 200:
        #         left = (width - height) / 2
        #         right = (width + height) / 2
        #         top = 0
        #         bottom = height
        #         img = img.crop((left, top, right, bottom))
        #         img.save(User_Picture.picture.path)

        #     elif width < 200 and height == 200:
        #         left = 0
        #         right = width
        #         top = 0
        #         bottom = width
        #         img = img.crop((left, top, right, bottom))
        #         img.save(User_Picture.picture.path)

        #     elif width and height == 200:
        #         img.save(User_Picture.picture.path)
        # else:
        #     pass
        User.objects.filter(pk=self.object.pk).update(work=work)
        """get_success_url."""
        score_table = UserScore.objects.all().filter(user_score=self.object.pk)
        #Editing
        if score_table:
            my_user = User.objects.get(id=self.object.pk)
            my_new_score = UserScore.objects.get(user_score=self.object.pk)
            if self.object.first_name != '' and self.object.last_name != '' and self.object.email != '' and self.object.telephone != '' and self.object.picture != '' and self.object.country != '' and self.object.work != '':
                if my_new_score.value_score == 'subtracted':
                    user = User.objects.get(id=self.object.pk)
                    user_all = User.objects.filter(id=self.object.pk)
                    for u in user_all:
                        user.score = u.score + 5
                        user.save()
                        my_new_score.value_score = 'added'
                        my_new_score.save()
            else:
                if my_new_score.value_score == 'added':
                    user = User.objects.get(id=self.object.pk)
                    user_all = User.objects.filter(id=self.object.pk)
                    for u in user_all:
                        user.score = u.score - 5
                        user.save()
                        my_new_score.value_score = 'subtracted'
                        my_new_score.save()
        #Creating
        else:
            my_user = User.objects.get(id=self.object.pk)
            user_score = UserScore(user_score=my_user, value_score='subtracted')
            user_score.save()
            my_new_score = UserScore.objects.get(user_score=self.object.pk)
            if self.object.first_name != '' and self.object.last_name != '' and self.object.email != '' and self.object.telephone != '' and self.object.picture != '' and self.object.country != '' and self.object.work != '':
                if my_new_score.value_score == 'subtracted':
                    user = User.objects.get(id=self.object.pk)
                    user_all = User.objects.filter(id=self.object.pk)
                    for u in user_all:
                        user.score = u.score + 5
                        user.save()
                        my_new_score.value_score = 'added'
                        my_new_score.save()
            else:
                if my_new_score.value_score == 'added':
                    user = User.objects.get(id=self.object.pk)
                    user_all = User.objects.filter(id=self.object.pk)
                    for u in user_all:
                        user.score = u.score - 5
                        user.save()
                        my_new_score.value_score = 'subtracted'
                        my_new_score.save()

        return reverse('view_profiledetail', kwargs={'pk': self.object.pk})

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User    
    template_name = 'configuration/usercustom/detail.html'

class ProfileDelete(LoginRequiredMixin, DeleteView):
    template_name = 'configuration/usercustom/delete.html'
    model = User
    success_url = reverse_lazy('list_users')

def ChangeViewUser(request):
    user_actual_inactive = UserOnline.objects.get(user=request.user.id)
    user_actual_inactive.active = False
    user_actual_inactive.save()
    return HttpResponse('Ok')

def ChangeActiveUser(request):
    user_actual_inactive = UserOnline.objects.get(user=request.user.id)
    user_actual_inactive.active = True
    user_actual_inactive.save()
    return HttpResponse('Ok')

def DeletePictureProfile(request):
    my_user = User.objects.get(id=request.user.id)
    #os.remove(my_user.picture.path)
    my_user.picture = None
    my_user.save()
    return HttpResponse('Ok')