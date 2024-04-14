from django.views.generic import TemplateView


class HubDashboardView(TemplateView):
    template_name = "hub.html"
