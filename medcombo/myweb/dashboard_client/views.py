from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardClient(LoginRequiredMixin, TemplateView):
    template_name = "myweb/dashboard_client/index.html"
