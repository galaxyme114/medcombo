from django.contrib import admin
from .models import User
from .models import Work
from import_export.admin import ImportExportModelAdmin


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
	pass


class WorkAdmin(ImportExportModelAdmin):
	pass
admin.site.register(Work, WorkAdmin)