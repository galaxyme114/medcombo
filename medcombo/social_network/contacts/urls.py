from django.conf.urls import url
from .views import ContactsList
from .views import add_contact
from .views import ContactsSearchData
from .views import load_contact, add_contact_favorite, delete_contact, add_favoriteproduct, ChangeStateContact, ContactsList_detail

urlpatterns = [
                url(r'^contacts/list$', ContactsList.as_view(), name='contacts_list'),
                url(r'^contacts/list_detail$', ContactsList_detail, name='contacts_list_detail'),
                url(r'^ajax/add_contact$', add_contact, name='ajax_add_contact'),
                url(r'^contacts-autocomplete/$', ContactsSearchData.as_view(create_field='name'), name='contacts-autocomplete'),
                url(r'^ajax/load_contact$', load_contact, name='ajax_load_contact'),
                url(r'^ajax/add_contact_favorite$', add_contact_favorite, name='ajax_add_contact_favorite'),
                url(r'^ajax/delete_contact$', delete_contact, name='ajax_delete_contact'),
                url(r'^ajax/add_favorite/product$', add_favoriteproduct, name='ajax_add_favorite'),
                url(r'^ajax/chage_state_contact$', ChangeStateContact, name='chage_state_contact'),
              ]