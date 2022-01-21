from django.forms import ModelForm
from medcombo.configuration.usercustom.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.forms.widgets import CheckboxSelectMultiple

class FormPermissions(ModelForm):
    class Meta:
        model = User
        fields = ['groups', 'user_permissions']

    def __init__(self, *args, **kwargs):
        super(FormPermissions, self).__init__(*args, **kwargs)
        self.fields["user_permissions"].widget = CheckboxSelectMultiple()
        self.fields["user_permissions"].queryset = Permission.objects.all()
        """self.fields["user_permissions"].queryset = Permission.objects.filter(content_type_id__in=[
            2,3,7,8,12,14,15,16,17,18,19,20,21,22,23,24,25,27,28,29,30,31,32,33,34,35,36,37,39,41
        ])"""

        self.fields["groups"].widget = CheckboxSelectMultiple()
        self.fields["groups"].queryset = Group.objects.all()

class FormPermissionsGroups(ModelForm):
    class Meta:
        model = User
        fields = ['groups']

    def __init__(self, *args, **kwargs):
        super(FormPermissionsGroups, self).__init__(*args, **kwargs)
        self.fields["groups"].widget = CheckboxSelectMultiple()
        self.fields["groups"].queryset = Group.objects.all()