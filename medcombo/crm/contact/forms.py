from django import forms
from medcombo.configuration.usercustom.models import User, Work
from django.contrib.auth.forms import UserCreationForm
from medcombo.configuration.company.forms import CityForm
from medcombo.configuration.company.models import Company
from cities_light.models import Country
from cities_light.models import City
from dal import autocomplete
from dal import forward

class LeadForm(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=4), required='true')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm, self).save(commit=commit)

class LeadForm_en(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=3), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_en, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_en, self).save(commit=commit)

class LeadForm_de(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=2), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_de, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_de, self).save(commit=commit)

class LeadForm_fr(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=5), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_fr, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_fr, self).save(commit=commit)

class LeadForm_it(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=6), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_it, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_it, self).save(commit=commit)

class LeadForm_pt(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=7), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_pt, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_pt, self).save(commit=commit)

class LeadForm_ja(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=9), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_ja, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_ja, self).save(commit=commit)

class LeadForm_zh(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=8), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_zh, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_zh, self).save(commit=commit)

class LeadForm_zhh(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    tracing = forms.ModelMultipleChoiceField(queryset=User.objects.filter(employee=True), required='true')
    work = forms.ModelChoiceField(queryset=Work.objects.filter(language_id=1), required='false')
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'country', 
            'first_name', 
            'last_name', 
            'telephone',
            'movil',
            'wechat',
            'work',
            'city',
            'tracing',
            'company',
            'lead']
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete-contact',
                                                       forward=['country'])
        }

    def __init__(self, *args, **kwargs):
        super(LeadForm_zhh, self).__init__(*args, **kwargs)
        del self.fields['username'] 

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(LeadForm_zhh, self).save(commit=commit)

class CompanyContactForm(CityForm):
    #country_company = forms.CharField(label=("Pais"), max_length=100)
    #city_company = forms.CharField(label=("Ciudad"), max_length=100)
    country_company = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')

    class Meta:
        model = Company
        fields = [
            'name',
            'address', 
            'country_company',
            'city_company',
            'code_postal', 
            'telephone',
            'web']
        widgets = {
            'city_company': autocomplete.ModelSelect2(url='city-autocomplete-contact-two',
                                                       forward=['country_company'])
        }

    # def __init__(self, *args, **kwargs):
    #     super(CompanyContactForm, self).__init__(*args, **kwargs)
    #     del self.fields['country']
    #     del self.fields['city']

    # def save(self, commit=True):
    #     self.instance.country = self.instance.country_company
    #     self.instance.city = self.instance.city_company
    #     return super(CompanyContactForm, self).save(commit=commit)

class EmailForm(forms.Form):
    sender = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

class CountryContactForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))