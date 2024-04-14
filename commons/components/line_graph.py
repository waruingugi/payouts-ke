from django_unicorn.components import UnicornView

from commons.constants import GraphDurationFilter
from commons.utils import get_graph_values


class LineGraphView(UnicornView):
    # Default values
    app_name: str = ""
    y_values: list[str] | None = None
    x_values: list[str] | None = None

    selected_graph_duration: int = GraphDurationFilter.ONE_HOUR.value
    graph_duration_filters = GraphDurationFilter.labels()

    def mount(self) -> None:
        self.data_points = 12
        self.x_values, self.y_values = get_graph_values(
            app_name=self.app_name,
            selected_graph_duration=self.selected_graph_duration,
            data_points=self.data_points,
        )

    def set_graph_duration(self, duration: int) -> None:
        self.selected_graph_duration = int(duration)
        self.update_graph()

    def update_graph(self):
        self.x_values, self.y_values = get_graph_values(
            app_name=self.app_name,
            selected_graph_duration=self.selected_graph_duration,
            data_points=self.data_points,
        )
        self.call("drawChart", self.x_values, self.y_values)
