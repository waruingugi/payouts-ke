from django.urls import path

from odibets.views import OdibetsDashboardView

app_name = "odibets"

urlpatterns = [
    # Component urls
    path("", OdibetsDashboardView.as_view(), name="dashboard"),
]
