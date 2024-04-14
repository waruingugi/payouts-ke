from commons.components.predictions import PredictionsView
from commons.constants import BettingApps


class Betgr8PredictionsView(PredictionsView):
    template_name = "unicorn/predictions.html"
    app_name: str = BettingApps.BETGR8.value
