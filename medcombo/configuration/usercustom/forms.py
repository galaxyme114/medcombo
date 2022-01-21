from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from captcha.fields import CaptchaField
from .models import User, Work
from django.contrib.auth.models import Group
import re
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
# from medcombo.configuration.location.models import Country, City

class SingupForm(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=4), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_en(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=3), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_en, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_en, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_fr(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=5), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_fr, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_fr, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_de(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=2), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_de, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_de, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_it(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=6), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_it, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_it, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_pt(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=7), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_pt, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_pt, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_ja(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=9), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_ja, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_ja, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_zh(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=8), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_zh, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_zh, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupForm_zhh(UserCreationForm):
    captcha = CaptchaField()
    #email = forms.EmailField(label=("Email"), max_length=75)
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=1), required='false')

    class Meta:
        model = User
        fields = ('username', 'email', 'work', 'country')

    def __init__(self, *args, **kwargs):
        super(SingupForm_zhh, self).__init__(*args, **kwargs)
        #self.fields['city'].queryset = City.objects.none()
        del self.fields['email']

        # if 'country' in self.data:
        #     try:
        #         country_id = int(self.data.get('country'))
        #         self.fields['city'].queryset = City.objects.filter(relationship=country_id).order_by('name')
        #     except (ValueError, TypeError):
        #         pass 
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        #self.instance.username = self.instance.email
        new_user = self.instance.username
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.username
        else:
            self.instance.email = None
        return super(SingupForm_zhh, self).save(commit=commit)

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('singup.html',locals())

class SingupEmployForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'groups')

    def __init__(self, *args, **kwargs):
        super(SingupEmployForm, self).__init__(*args, **kwargs)
        del self.fields['username']
        self.fields["groups"].widget = CheckboxSelectMultiple()
        self.fields["groups"].queryset = Group.objects.all()

    def save(self, commit=True):
        self.instance.username = self.instance.email
        self.instance.employee = True
        return super(SingupEmployForm, self).save(commit=commit)

class SingupEmployFormUpdate(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'groups', 'username')

    def __init__(self, *args, **kwargs):
        super(SingupEmployFormUpdate, self).__init__(*args, **kwargs)
        del self.fields['username']
        self.fields["groups"].widget = CheckboxSelectMultiple()
        self.fields["groups"].queryset = Group.objects.all()

    def save(self, commit=True):
        self.instance.username = self.instance.email
        self.instance.employee = True
        return super(SingupEmployFormUpdate, self).save(commit=commit)

class SingupEmployFormUpdatePassword(UserCreationForm):
    class Meta:
        model = User
        fields = ['work']

    def __init__(self, *args, **kwargs):
        super(SingupEmployFormUpdatePassword, self).__init__(*args, **kwargs)
        del self.fields['work']

    def save(self, commit=True):
        self.instance.employee = True
        return super(SingupEmployFormUpdatePassword, self).save(commit=commit)

class SingupFormAdmin(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=4), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                print('33333333333')
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin, self).save(commit=commit)

class SingupFormAdmin_en(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=3), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_en, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_en, self).save(commit=commit)

class SingupFormAdmin_zhh(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=1), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_zhh, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_zhh, self).save(commit=commit)

class SingupFormAdmin_zh(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=8), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_zh, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_zh, self).save(commit=commit)

class SingupFormAdmin_de(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=2), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_de, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_de, self).save(commit=commit)

class SingupFormAdmin_fr(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=5), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_fr, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_fr, self).save(commit=commit)

class SingupFormAdmin_it(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=6), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_it, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_it, self).save(commit=commit)

class SingupFormAdmin_pt(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=7), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_pt, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_pt, self).save(commit=commit)

class SingupFormAdmin_ja(UserCreationForm):
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=9), required='false')
    class Meta:
        model = User
        fields = ('username', 'work', 'country', 'first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(SingupFormAdmin_ja, self).__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, commit=True):
        user_new = User.objects.filter(lead=False).filter(employee=False)
        my_list = []
        if user_new.count() == 0:
            self.instance.username = 1000
        else:
            for user in user_new:
                value = str(user.username).isdigit()
                if value == True:
                    my_list.append(int(user.username))
            order = sorted(my_list, key=int, reverse=True)
            if order:
                self.instance.username = order[0] + 1
            else:
                self.instance.username = 1000
        self.instance.lead = False
        self.instance.employee = False
        self.instance.email = None
        return super(SingupFormAdmin_ja, self).save(commit=commit)

class ChangePassFormAdmin(UserCreationForm):
    class Meta:
        model = User
        fields = ['work']

    def __init__(self, *args, **kwargs):
        super(ChangePassFormAdmin, self).__init__(*args, **kwargs)
        del self.fields['work']

    def save(self, commit=True):
        self.instance.lead = False
        self.instance.employee = False
        return super(ChangePassFormAdmin, self).save(commit=commit)

class UserUpdateForm(ModelForm):
    username = None
    work = forms.ModelChoiceField(queryset=Work.objects.all())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone','picture', 'country', 'work','username']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['username']
