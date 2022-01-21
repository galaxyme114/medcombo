from django import forms
from medcombo.product.models import Product
from medcombo.product.models import Area
from medcombo.product.models import Category
from medcombo.product.models import SubCategory
from medcombo.product.models import BannerWeb
from medcombo.configuration.company.models import Company
from dal import autocomplete
from django.forms import ModelChoiceField
from dal import forward
from dal import autocomplete

class CategoriesForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=4),widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)', 'multiple': 'multiple'}),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)'} ),                                           
        }

class SearchFormProduct(forms.ModelForm):
    """name = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2(url='products-autocomplete')
    )"""
    class Meta:
        model = Product
        fields = ['name']
        widgets = {
            'name': autocomplete.ListSelect2(url='products-autocomplete',attrs={'data-placeholder':'The Medical Directory','class':'form-control product-search','aria-label':'The Medical Directory','aria-describedby':'addon-wrapping'})                                                   
        }

class CategoriesForm1(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=1), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm2(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=2), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm3(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=3), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm5(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=5), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm6(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=6), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm7(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=7), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order','description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm8(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=8), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name', 'order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class CategoriesForm9(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.filter(language=9), widget=forms.Select(attrs={'onchange' :  'myfunction(1)'}))
    class Meta:
        model = Product
        fields = ('name','order', 'description', 'picture', 'area', 'category', 'subcategory', 'company', 'video', 'language', 'picture2', 'picture3', 'picture4')
        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete',
                                                       forward=['area'], attrs = {'onchange' :  'myfunction(2)' }),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete',
                                                       forward=['category'], attrs = {'onchange' :  'myfunction(3)' } )                                                       
        }

class BannerWebForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required='true', widget=forms.Select(attrs={'class':'form-control select-area', 'style':'border-right: none; border-radius: 0.25rem 0 0 0.25rem;'})),
    banner_company = forms.ModelChoiceField(queryset=Company.objects.all().exclude(pk=1).exclude(user_relationship__lead=1), required='true', widget=forms.Select(attrs={'class':'form-control select-area', 'style':'border-right: none; border-radius: 0.25rem 0 0 0.25rem;'}))
    class Meta:
        model = BannerWeb
        fields = ('area', 'banner_company', 'category', 'subcategory', 'language_campaign', 'picture_campaign','picture_campaign_search','start_banner',
            'end_banner', 'isActive')
        widgets = {
            #'language_campaign': forms.TextInput(attrs={'class':'form-control', 'id':'selectBanner'}),
            #'picture_campaign': forms.TextInput(attrs={'type':'file', 'class':'custom-file-input', 'id':'customFileEs', 'onchange':'readURL(this,"Es");'}),
            'category': autocomplete.ModelSelect2(url='category-autocomplete', forward=['area']),
            'subcategory': autocomplete.ModelSelect2(url='subcategory-autocomplete', forward=['category'], attrs = {'onchange' :  'myfunction()' } ),
            'start_banner': forms.TextInput(attrs={'type':'date', 'class':'form-control', 'name':'dateInit', 'id':'dateInit', 'required':True}),
            'end_banner': forms.TextInput(attrs={'type':'date', 'class':'form-control', 'name':'dateFinish', 'id':'dateFinish', 'required':True}),
            'isActive': forms.TextInput(attrs={'class':'form-control', 'name':'isActive'}),
       }