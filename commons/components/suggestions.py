from django_unicorn.components import UnicornView

from commons.constants import BettingApps, ProbabilityPayoutFilter
from commons.utils import payouts_filter_probabilities


class SuggestionsView(UnicornView):
    suggestions: dict[str, str] = {}

    def mount(self) -> None:
        for app_name in BettingApps:
            filter = ProbabilityPayoutFilter.OVER_TWENTY_FIVE_FILTER
            app_prob = payouts_filter_probabilities(app_name.value)
            filter_prob: float = app_prob[f"Over {filter.value}x"]["probability"]  # type: ignore

            if filter_prob > 90:
                self.suggestions[app_name.value] = (
                    "There's a high chance of an over 25x, but it is very risky."
                    f" Try {app_name.value.capitalize()} later."
                )

            elif filter_prob > 75:
                self.suggestions[app_name.value] = (
                    "There's a good chance of an over 25x. "
                    f"Play with {app_name.value.capitalize()} right now."
                )

            elif filter_prob > 50:
                self.suggestions[app_name.value] = (
                    "There's a fair chance of an over 25x. "
                    f"Keep an eye on {app_name.value.capitalize()}."
                )
            else:
                self.suggestions[app_name.value] = (
                    "There's a very low chance of an over 25x. "
                    f"Check on {app_name.value.capitalize()} later."
                )
