from django.urls import path

from winpesa.views import WinpesaDashboardView

app_name = "winpesa"

urlpatterns = [
    # Component urls
    path("", WinpesaDashboardView.as_view(), name="dashboard"),
]
