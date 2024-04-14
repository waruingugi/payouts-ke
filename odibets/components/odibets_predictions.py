from commons.components.predictions import PredictionsView
from commons.constants import BettingApps


class OdibetsPredictionsView(PredictionsView):
    template_name = "unicorn/predictions.html"
    app_name: str = BettingApps.ODIBETS.value
