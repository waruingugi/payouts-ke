from commons.components.predictions import PredictionsView
from commons.constants import BettingApps


class WinpesaPredictionsView(PredictionsView):
    template_name = "unicorn/predictions.html"
    app_name: str = BettingApps.WINPESA.value
