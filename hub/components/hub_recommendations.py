from django.utils.timezone import localtime
from django_unicorn.components import UnicornView

from commons.constants import BettingApps, ProbabilityPayoutFilter
from commons.models import Payouts
from commons.utils import calculate_intervals
from hub.constants import RECOMMENDED_DESCR


class HubRecommendationsView(UnicornView):
    recommendations: dict[str, str] = {}
    template_name = "recommendations.html"

    def mount(self) -> None:
        """Provide recommendations on which app to use today"""
        over_25x_filter = ProbabilityPayoutFilter.OVER_TWENTY_FIVE_FILTER
        filter_intervals: dict = {}

        start_time = localtime().replace(hour=0, minute=0, second=0, microsecond=0)

        # Loop through apps and get intervals of over 25x in the last hour
        for app in BettingApps:
            app_payouts = Payouts.objects.filter(
                app=app.value, created_at__gt=start_time
            ).values_list("payout", flat=True)

            intervals: list = calculate_intervals(app_payouts, over_25x_filter)

            average = (
                sum(intervals) / len(intervals) if len(intervals) > 0 else float("inf")
            )
            filter_intervals[app.value] = average

        # Sort according to apps with lowest distance between intervals of over 25x
        sorted_apps: list = sorted(filter_intervals, key=filter_intervals.get)  # type: ignore

        # Assign recommendations string
        self.recommendations = {}
        for i in range(len(sorted_apps)):
            app_name = sorted_apps[i]

            self.recommendations[app_name] = (
                RECOMMENDED_DESCR[i].format(app_name.title())
                if filter_intervals[app_name] > 0
                else "No recommendations. Please contact admin"
            )
