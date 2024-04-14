from commons.components.payouts import PayoutsView
from commons.constants import BettingApps


class OdibetsPayoutsView(PayoutsView):
    template_name = "unicorn/payouts.html"
    app_name: str = BettingApps.ODIBETS.value
