from .views import SingupView
from .views import ProfileDetail
from .views import ProfileUpdate
from .views import ProfileList
from .views import ChangeViewUser
from .views import ChangeActiveUser
from .views import DeletePictureProfile
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
               url(r'^profile/list$', ProfileList.as_view(), name='profile_list'),
               url(r'^Sign-up/$', SingupView.as_view(), name='view_singup'),
               url(r'^Profile/Detail/(?P<pk>[0-9]+)/$', ProfileDetail.as_view(), name='view_profiledetail'),
               url(r'^Profile/Update/(?P<pk>[0-9]+)/$', ProfileUpdate.as_view(), name='view_profileupdate'),
	   	       url(r'^reset/password/$', PasswordResetView.as_view(template_name='configuration/usercustom/password_reset_form.html', email_template_name='configuration/usercustom/password_reset_email.html'), name='password_reset'),
		       url(r'^reset/password/reset/done/$', PasswordResetDoneView.as_view(template_name='configuration/usercustom/password_reset_done.html'), name='password_reset_done'),
		       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='configuration/usercustom/password_reset_confirm.html'), name='password_reset_confirm'),
		       url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='configuration/usercustom/password_reset_complete.html'), name='password_reset_complete'),
               url(r'^change/password/(?P<pk>[0-9]+)/$', PasswordChangeView.as_view(template_name='configuration/usercustom/password_change.html', success_url='/'), name='change_password'),
               url(r'^change/view/$', ChangeViewUser, name='change_view'),
               url(r'^change/view_active/$', ChangeActiveUser, name='change_view_active'),
               url(r'^delete_picture_user/$', DeletePictureProfile, name='delete_picture_user'),
              ]