from django import forms
from medcombo.crm.dashboard_admin.models import Banner, Campaign, BannerIndex, LanguageCampaign, CompanyLogo, Event
from medcombo.configuration.company.models import Company
from medcombo.product.models import Sponsor, BannerWeb, Area, Category, SubCategory
from dal import autocomplete
from django.forms import ModelChoiceField
from dal import forward
from medcombo.configuration.usercustom.models import User


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = (
            'start_campaign', 
            'end_campaign',
            'activate_campaign',
            'position_campaign'
        )
        widgets = {
            'start_campaign': forms.TextInput(attrs={'type':'date', 'class':'form-control col-md-9 col-lg-10', 'name':'dateInit', 'id':'dateInit', 'required':True}),
            'end_campaign': forms.TextInput(attrs={'type':'date', 'class':'form-control col-md-9 col-lg-10', 'name':'dateFinish', 'id':'dateFinish', 'required':True}),
            'activate_campaign': forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'activateBanner'}),
            'position_campaign': forms.NumberInput(attrs={'class':'form-control col-md-6','min':0, 'value':0, 'required':True})
        }

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = (
            'banner_campaign',
            'language_campaign',
            'url_campaign',
            'picture_campaign'
        )
        widgets = {
            'banner_campaign': forms.TextInput(attrs={'type':'date', 'class':'form-control col-sm-8', 'name':'dateInit', 'id':'dateInit', 'required':True}),
            'language_campaign': forms.TextInput(attrs={'class':'form-control', 'id':'selectBanner'}),
            'url_campaign': forms.TextInput(attrs={'type':'url', 'class':'form-control col-sm-12', 'name':'urlBanner', 'placeholder':'', 'required':True}),
            'picture_campaign': forms.TextInput(attrs={'type':'file', 'class':'custom-file-input', 'id':'customFileEs', 'onchange':'readURL(this,"Es");'})
        }

class SponsorForm(forms.ModelForm):
    empresas= Company.objects.all().exclude(pk=1).exclude(user_relationship__lead=1)# esta es la que iba dentro del queryset 
    company = forms.ModelChoiceField(queryset=empresas, required='true', widget=forms.Select(attrs={'class':'form-control select-company', 'style':'border-right: none; border-radius: 0.25rem 0 0 0.25rem;'}))
    class Meta:
        model = Sponsor
        fields = ('company', 'start', 'end', 'product','lateral')
        widgets = {
            'start': forms.TextInput(attrs={'type':'text', 'class':'form-control col-sm-12','required':'required'}),
            'end': forms.TextInput(attrs={'type':'text', 'class':'form-control col-sm-12','required':'required'}),
            'lateral': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class BannerIndexForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=LanguageCampaign.objects.all(), required="true", widget=forms.Select(attrs={'class':'form-control mt-3'}))
    class Meta: 
        model = BannerIndex 
        fields = (
            'language',
            'picture',
            'description',
            'date',
            'author',
            'order_created',
            'title', 
            'video'
        )
        widgets = {
            'picture': forms.TextInput(attrs={'type':'file', 'class':'custom-file-input', 'id':'customFileEs', 'onchange':'readURL(this,"Es");'}),
            'description': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5','required':True}),
            'date': forms.TextInput(attrs={'class':'form-control','required':True}),
            'author': forms.TextInput(attrs={'type':'text', 'class':'form-control','required':True}),
            'order_created': forms.NumberInput(attrs={ 'class':'form-control','min':0 ,'required':True}),
            'title': forms.TextInput(attrs={'type':'text', 'class':'form-control','required':True}),
        }

class CompanyLogoForm(forms.ModelForm):
    class Meta: 
        model = CompanyLogo 
        fields = (
            'url',
            'picture',
            'title'
        )
        widgets = {
            'url': forms.TextInput(attrs={'type':'url', 'class':'form-control','placeholder':'', 'required':True}),
            'picture': forms.TextInput(attrs={'type':'file', 'class':'custom-file-input', 'id':'customFileEs', 'onchange':'readURL(this);'}),
            'title': forms.TextInput(attrs={'type':'text', 'class':'form-control','required':True}),
        }

class EventForm(forms.ModelForm):
    class Meta: 
        model = Event 
        fields = (
            'start_event',
            'end_event',
            'picture',
            'title',
            'description_es',
            'description_en',
            'description_pt',
            'description_fr',
            'description_it',
            'description_de',
            'description_zh_hant',
            'description_zh_hans',
            'description_jp',
        )
        widgets = {
            'start_event': forms.TextInput(attrs={'type':'date', 'class':'form-control col-md-9 col-lg-10', 'name':'dateInit', 'id':'dateInit', 'required':True}),
            'end_event': forms.TextInput(attrs={'type':'date', 'class':'form-control col-md-9 col-lg-10', 'name':'dateFinish', 'id':'dateFinish', 'required':True}),
            'picture': forms.TextInput(attrs={'type':'file', 'class':'custom-file-input', 'id':'customFileEs', 'onchange':'readURL(this);'}),
            'title': forms.TextInput(attrs={'type':'text', 'class':'form-control','required':True}),
            'description_es': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_en': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_pt': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_fr': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_it': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_de': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_zh_hant': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_zh_hans': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
            'description_jp': forms.Textarea(attrs={'style':'resize: none;', 'class': 'form-control','rows':'5'}),
        }