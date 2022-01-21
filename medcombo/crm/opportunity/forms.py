from django import forms
from .models import Opportunity
from medcombo.configuration.usercustom.models import User
from medcombo.product.models import Product
from dal import autocomplete
from django.forms import ModelChoiceField
from dal import forward
from django.db.models import Q

class OpportunityForm(forms.ModelForm):
    query_opportunities = Opportunity.objects.filter(Q(state=1) | Q(state=2) | Q(state=3)).values_list('client',flat=True)
    client = forms.ModelChoiceField(queryset=User.objects.exclude(employee=True).exclude(username='admin').exclude(username='admin_medcombo@admin.com').exclude(id__in=query_opportunities), required='true')
    product = forms.ModelChoiceField(queryset=Product.objects.filter(company=1), required='True')

    class Meta:
        model = Opportunity
        fields = ('title', 'client', 'responsible', 'probability', 'state', 'automatic_percent', 'contacted_by', 'expected_revenue', 'product')
        widgets = {
            'automatic_percent': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'expected_revenue': forms.NumberInput(attrs={'class':'form-control','step':'0.10'})
        }

class OpportunityChangeForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(company=1), required='True')

    class Meta:
        model = Opportunity
        fields = ('title', 'probability', 'automatic_percent', 'contacted_by', 'expected_revenue', 'product')
        widgets = {
            'automatic_percent': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'expected_revenue': forms.NumberInput(attrs={'class':'form-control','step':'0.10'})
        }

class OpportunityUpdateForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['contacted_by']