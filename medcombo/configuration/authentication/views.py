from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import FormView, RedirectView
from medcombo.configuration.usercustom.models import User
from medcombo.configuration.usercustom.models import UserOnline, Userrunning_system, GetIP
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.utils.timezone import localtime, now
#import geocoder

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "configuration/authentication/login.html"
    #success_url = reverse_lazy("dashboard_client")

    def get_success_url(self):
        if self.request.POST.get('next') == 'None' or self.request.POST.get('next') is None:
            return reverse_lazy("dashboard_client")
        else:
            return self.request.POST.get('next')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        #****************** GET Running Client System time ****************
        user_delay = Userrunning_system()
        user_delay.user_id = form.get_user().id
        user_delay.start = localtime(now())
        user_delay.save()

        #****************Get Client IP Address ****************************
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        
        user_ip = GetIP()
        # g = geocoder.ip('188.43.136.32')
        # print(g.latlng)
        user_ip.user_ip_id = self.request.user.id
        user_ip.ipaddress = ip
        user_ip.save()
        #************************End Get IP Address ********************

        user_active = UserOnline.objects.filter(user=self.request.user.id)
        #Editing
        if user_active:
            user_online_actual = UserOnline.objects.get(user=self.request.user.id)
            user_online_actual.active = True
            user_online_actual.save()
        #Creating
        else:
            user_actual = User.objects.get(id=self.request.user.id)
            new_active_user = UserOnline(user=user_actual,active=True)
            new_active_user.save()

        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        UserOnline.objects.filter(user=request.user.id).update(active=False)
        # user_actual_inactive.active = False
        # user_actual_inactive.save()
        user_running_info = Userrunning_system.objects.filter(user_id=request.user.id).order_by('-start')
        all_data = Userrunning_system.objects.get(user=request.user.id,start=user_running_info[0].start )
        if all_data.start:
            all_data.end = localtime(now())
            all_data.save()
        
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
