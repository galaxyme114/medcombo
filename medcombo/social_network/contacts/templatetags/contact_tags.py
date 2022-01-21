from django import template
from medcombo.social_network.contacts.models import Contacts


register = template.Library()

@register.inclusion_tag('contacts/_contacts.html',  takes_context=True)
def get_contacts_list():
    return {'contacts': Contacts.objects.filter(owner=self.request.user.id)}