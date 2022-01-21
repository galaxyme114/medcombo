from django.contrib import admin
from .models import Contacts


class ContactsAdmin(admin.ModelAdmin):
	pass
admin.site.register(Contacts, ContactsAdmin)

