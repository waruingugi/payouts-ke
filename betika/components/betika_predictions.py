from commons.components.predictions import PredictionsView
from commons.constants import BettingApps


class BetikaPredictionsView(PredictionsView):
    template_name = "unicorn/predictions.html"
    app_name: str = BettingApps.BETIKA.value
