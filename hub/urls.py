from django.urls import path

from hub.views import HubDashboardView

app_name = "hub"

urlpatterns = [
    # Component urls
    path("", HubDashboardView.as_view(), name="dashboard"),
]
