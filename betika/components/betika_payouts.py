from commons.components.payouts import PayoutsView
from commons.constants import BettingApps


class BetikaPayoutsView(PayoutsView):
    template_name = "unicorn/payouts.html"
    app_name: str = BettingApps.BETIKA.value
