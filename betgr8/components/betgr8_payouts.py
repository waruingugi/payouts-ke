from commons.components.payouts import PayoutsView
from commons.constants import BettingApps


class Betgr8PayoutsView(PayoutsView):
    template_name = "unicorn/payouts.html"
    app_name: str = BettingApps.BETGR8.value
