from django.conf.urls import url
from .views import ListUsersPermission
from .views import UpdatePermission
from .views import UpdatePermissionGroups
from .views import DeleteUserRegister
from .views import ActiveUserRegister
from .views import ListUserAdmin
from .views import ListEmployAdmin
from .views import CreateUserAdmin
from .views import CreateUserEmploy
from .views import UserDeleteAdmin
from .views import UpdateUsersAdmin
from .views import UpdateUsersPassAdmin
from .views import UpdateEmploy
from .views import EmployeeDelete
from .views import UpdateEmployPassword
from .views import ListUserSalesAdmin
from .views import MyWebCompanyCreateAdmin
from .views import AcceptUser
from .views import UpdateUserExtraName
from .views import ImportUserAdmin
from .views import ExportUserAdmin
from .views import SaleUserDelete

urlpatterns = [
               url(r'^List_Users_Permission$', ListUsersPermission.as_view(), name='list_permission'),
               url(r'^Permission/Update/(?P<pk>[0-9]+)/$', UpdatePermission.as_view(), name='update_permission'),
               url(r'^delete_user_register$', DeleteUserRegister, name='delete_user_register'),
               url(r'^active_user_register$', ActiveUserRegister, name='active_user_register'),
               url(r'^admin_user_list/$', ListUserAdmin.as_view(), name='admin_user_list'),
               url(r'^admin_user_sales/$', ListUserSalesAdmin.as_view(), name='admin_user_sales'),
               url(r'^admin_user_sales_delete/$', SaleUserDelete, name='admin_user_sales_delete'),
               url(r'^admin_employ_list/$', ListEmployAdmin.as_view(), name='admin_employ_list'),
               url(r'^admin_user_create/$', CreateUserAdmin.as_view(), name='admin_user_create'),
               url(r'^admin_employ_create/$', CreateUserEmploy.as_view(), name='admin_employ_create'),
               url(r'^EmployeeGroup/Update/(?P<pk>[0-9]+)/$', UpdatePermissionGroups.as_view(), name='update_permissiongroups'),
               url(r'^admin_user_delete$', UserDeleteAdmin, name='admin_user_delete'),
               url(r'^UserUpdateAdmin/(?P<pk>[0-9]+)/$', UpdateUsersAdmin.as_view(), name='UserUpdateAdmin'),
               url(r'^UserPassUpdateAdmin/(?P<pk>[0-9]+)/$', UpdateUsersPassAdmin.as_view(), name='UserPassUpdateAdmin'),
               url(r'^update_employ/(?P<pk>[0-9]+)/$', UpdateEmploy.as_view(), name='update_employ'),
               url(r'^EmployeeDelete/$', EmployeeDelete, name='EmployeeDelete'),
               url(r'^update_employee_password/(?P<pk>[0-9]+)/$', UpdateEmployPassword.as_view(), name='update_employee_password'),
               url(r'^admin/company/create/(?P<pk>[0-9]+)/$', MyWebCompanyCreateAdmin.as_view(), name='create_admin_company'),
               url(r'^User/accept$', AcceptUser, name='user_accept'),
               url(r'^User/update_extra$', UpdateUserExtraName, name='user_extra_update'),
               url(r'^admin_user_import/$', ImportUserAdmin, name='admin_user_import'),
               url(r'^admin_user_export/$', ExportUserAdmin, name='admin_user_export'),
              ]
