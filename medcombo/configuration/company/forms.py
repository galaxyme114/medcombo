from django import forms
from cities_light.models import Country
from cities_light.models import City
from .models import Company
from dal import autocomplete
from django.forms import ModelChoiceField
from medcombo.myweb.catalogue.models import Catalogue
from dal import forward

class CityForm(forms.ModelForm):
    country_company = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    class Meta:
        model = Company
        fields = ('name', 'cif', 'address', 'country_company', 'city_company', 'code_postal', 'telephone', 'type_company', 'another_type_company', 'sector')
        widgets = {
            'city_company': autocomplete.ModelSelect2(url='city-autocomplete',
                                                       forward=['country_company'])
        }
    
    """def clean(self, *args, **kwargs):
        cleaned_data = super(CityForm, self).clean(*args, **kwargs)
        telephone = cleaned_data.get('telephone', None)
        if telephone is not None:
            if not telephone.isdigit():
                self.add_error('telephone', 'Ingrese un teléfono válido')"""

class CompanyUpdateForm(forms.ModelForm):
    country_company = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    class Meta:
        model = Company
        fields = ('name', 'cif', 'address', 'city_company', 'country_company', 'code_postal', 'telephone', 'type_company', 'another_type_company', 'sector', 'web', 'logo', 'certification_iso')
        widgets = {
            'certification_iso': forms.TextInput(attrs={'type':'file', 'class':'custom-file-input'}),
            'city_company': autocomplete.ModelSelect2(url='city-autocomplete',
                                                       forward=['country_company'], attrs={'class':'form-control'})
        }
    """def clean(self, *args, **kwargs):
        cleaned_data = super(CompanyUpdateForm, self).clean(*args, **kwargs)
        name = cleaned_data.get('name')
        print(name)
        if not name.isalpha():
            raise forms.ValidationError('El nombre no puede contener números')
        return name"""
    
    """def clean(self, *args, **kwargs):
        cleaned_data = super(CompanyUpdateForm, self).clean(*args, **kwargs)
        telephone = cleaned_data.get('telephone', None)
        if telephone is not None:
            if not telephone.isdigit():
                self.add_error('telephone', 'Ingrese un teléfono válido')"""

class CompanyFacturationForm(forms.ModelForm):
    invoicing_country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    class Meta:
        model = Company
        fields = ('invoicing_company_name', 'invoicing_address', 'invoicing_postal_code', 'invoicing_telephone', 'invoicing_fax', 'invoicing_title', 'invoicing_last_name', 'invoicing_first_name', 'invoicing_email', 'invoicing_vat_number', 'invoicing_country', 'invoicing_city' )
        widgets = {
            'invoicing_city': autocomplete.ModelSelect2(url='city-autocomplete-facturation',
                                                       forward=['invoicing_country'])
        }

class CatalogueForm(forms.ModelForm):
    class Meta:
        model = Catalogue
        fields = ('name', 'file', 'picture', 'company', 'language')
        widgets = {
            'file': forms.FileInput(attrs={'class':'custom-file-input', 'id':'customFileEs', 'type':'file'}),
            'picture': forms.FileInput(attrs={'class':'custom-file-input','onchange':'readURL(this);'})
        }