from django import forms
from .models import Contacts
from dal import autocomplete
from django.forms import ModelChoiceField
from dal import forward
from dal import autocomplete

class SearchFormContact(forms.ModelForm):
    contacts = forms.ModelChoiceField(
        queryset=Contacts.objects.all(),
        widget=autocomplete.ModelSelect2(url='contacts-autocomplete')
    )

    class Meta:
        model = Contacts
        fields = ('__all__')


# class SearchFormContact(forms.ModelForm):
#     class Meta:
#         model = Contacts
#         fields = ('__all__')
#         widgets = {
#             'contacts': autocomplete.ModelSelect2(url='contacts-autocomplete')
#         }        