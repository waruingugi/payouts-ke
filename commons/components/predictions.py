from django_unicorn.components import UnicornView

from commons.utils import payouts_filter_probabilities


class PredictionsView(UnicornView):
    app_prob: dict[str, str] = {}
    app_name: str = ""

    def mount(self) -> None:
        self.app_prob = payouts_filter_probabilities(self.app_name)

        self.call("initializeCircleCharts")
