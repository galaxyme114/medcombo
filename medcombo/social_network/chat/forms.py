from django import forms
from medcombo.social_network.contacts.models import Message
from django.forms import ModelChoiceField
from dal import forward
from dal import autocomplete

class SearchFormMessages(forms.ModelForm):
    message = forms.ModelChoiceField(
        queryset=Message.objects.all(),
        widget=autocomplete.ModelSelect2(url='messages-autocomplete')
    )
    class Meta:
        model = Message
        fields = ('__all__')
