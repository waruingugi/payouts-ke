from django.urls import path

from betgr8.views import Betgr8DashboardView

app_name = "betgr8"

urlpatterns = [
    # Component urls
    path("", Betgr8DashboardView.as_view(), name="dashboard"),
]
