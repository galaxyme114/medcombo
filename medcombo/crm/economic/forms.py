from medcombo.crm.economic.models import Proposal_Commercial
from django import forms
from dal import autocomplete
from django.forms import ModelChoiceField
from dal import forward
from medcombo.configuration.usercustom.models import User
from medcombo.product.models import Product
from medcombo.crm.opportunity.models import Opportunity


class ProposalForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(lead=False,employee=False).order_by('-date_joined'), required="true", widget=forms.Select(attrs={'class':'form-control mt-3'}))
    product = forms.ModelChoiceField(queryset=Product.objects.filter(company=1), required="true", widget=forms.Select(attrs={'class':'form-control mt-3'}))
    opportunity = forms.ModelChoiceField(queryset=Opportunity.objects.all(), required="true", widget=forms.Select(attrs={'class':'form-control mt-3'}))
    class Meta: 
        model = Proposal_Commercial 
        fields = (
            'title',
            'commercial',
            'total',
            'edit_date',
            'payment_terms',
            'comments',
            'validata',

        )
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control col-sm-6','value': '', 'required':True}),
            'commercial': forms.TextInput(attrs={'class':'form-control col-sm-6','value': '', 'required':True}),
            'total': forms.TextInput(attrs={'class':'form-control col-sm-6','value':'', 'required':True}),
            'edit_date': forms.TextInput(attrs={'type':'date', 'class':'form-control col-sm-6', 'required':True}), 
            'payment_terms': forms.TextInput(attrs={'class':'form-control col-sm-6','value':'', 'required':True}),
            'comments': forms.TextInput(attrs={'class':'form-control col-sm-6','value':'', 'required':True}),
            'validata': forms.TextInput(attrs={'class':'form-control col-sm-6','value':'', 'required':True}),    
        }