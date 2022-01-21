from django.contrib import admin
from medcombo.product.models import Product
from medcombo.product.models import Area
from medcombo.product.models import Category
from medcombo.product.models import SubCategory
from import_export.admin import ImportExportModelAdmin


@admin.register(Product)
class Product(ImportExportModelAdmin):
    pass

@admin.register(Area)
class AreaAdmin(ImportExportModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    pass

""" @admin.register(Translate)
class TranslateAdmin(ImportExportModelAdmin):
    pass """




""" @admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    pass

@admin.register(RequestTray)
class RequestTrayAdmin(ImportExportModelAdmin):
    pass

class UserCategoryAdmin(admin.ModelAdmin):
	pass
admin.site.register(UserCategory, UserCategoryAdmin)

@admin.register(Keyword)
class KeywordAdmin(ImportExportModelAdmin):
    pass """
