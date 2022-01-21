from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from medcombo.configuration.usercustom.models import User, Work
from cities_light.models import Country

class UserResource(resources.ModelResource):
    work = fields.Field(
        column_name='work',
        attribute='work',
        widget=ForeignKeyWidget(Work, 'name'))
    country = fields.Field(
        column_name='country',
        attribute='country',
        widget=ForeignKeyWidget(Country, 'name'))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'work', 'country',)
        export_order = ('username', 'first_name', 'last_name', 'email', 'telephone', 'work', 'country',)

    def get_queryset(self):
        return self._meta.model.objects.filter(is_superuser=0, employee=0)