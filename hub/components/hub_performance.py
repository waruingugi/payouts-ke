from django.utils.timezone import localtime
from django_unicorn.components import UnicornView

from commons.constants import BettingApps, ProbabilityPayoutFilter
from commons.models import Payouts
from commons.utils import calculate_intervals


class HubPerformanceView(UnicornView):
    performance: dict = {}
    template_name = "performance.html"

    def mount(self) -> None:
        """Get the performance of today vs yesterday of each app"""
        over_25x_filter = ProbabilityPayoutFilter.OVER_TWENTY_FIVE_FILTER

        start_time_today = localtime().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_time_today = localtime()

        start_time_yest = localtime().replace(
            day=localtime().day - 1, hour=0, minute=0, second=0, microsecond=0
        )
        end_time_yest = localtime().replace(day=localtime().day - 1)

        for app in BettingApps:
            app_payouts_today = Payouts.objects.filter(
                app=app.value,
                created_at__gt=start_time_today,
                created_at__lt=end_time_today,
            ).values_list("payout", flat=True)
            app_payouts_yest = Payouts.objects.filter(
                app=app.value,
                created_at__gt=start_time_yest,
                created_at__lt=end_time_yest,
            ).values_list("payout", flat=True)

            intervals_today: list = calculate_intervals(
                app_payouts_today, over_25x_filter
            )
            average_today = (
                sum(intervals_today) / len(intervals_today)
                if len(intervals_today) > 0
                else 0
            )

            intervals_yest: list = calculate_intervals(
                app_payouts_yest, over_25x_filter
            )
            average_yest = (
                sum(intervals_yest) / len(intervals_yest)
                if len(intervals_yest) > 0
                else 0
            )

            self.performance[app.value] = {
                "flow": "increase" if average_today > average_yest else "decrease",
                "percentage": (
                    abs(100 - (average_today / average_yest) * 100)
                    if average_yest > 0
                    else 0
                ),
            }
