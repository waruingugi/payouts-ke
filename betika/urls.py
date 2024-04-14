from django.urls import path

from betika.views import BetikaDashboardView

app_name = "betika"

urlpatterns = [
    # Component urls
    path("", BetikaDashboardView.as_view(), name="dashboard"),
]
