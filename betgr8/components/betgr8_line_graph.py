from commons.components.line_graph import LineGraphView
from commons.constants import BettingApps


class Betgr8LineGraphView(LineGraphView):
    template_name = "unicorn/line_graph.html"
    app_name: str = BettingApps.BETGR8.value
