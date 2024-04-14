from typing import Optional

from django.db.models.query import QuerySet
from django_unicorn.components import UnicornView

from commons.constants import DurationFilter, MinValueFilter, PageSizeFilter
from commons.utils import payouts_query


class PayoutsView(UnicornView):
    # payouts: Optional[list[QuerySet]] = None
    # Default values
    payouts: Optional[QuerySet] = None
    app_name: str = ""

    selected_duration: int = DurationFilter.TWO_HOURS.value
    selected_min_value: float = MinValueFilter.OVER_ONE.value
    selected_page_size: int = PageSizeFilter.THREE_HUNDRED.value

    duration_filters = DurationFilter.labels()
    min_value_filters = MinValueFilter.labels()
    page_size_filters = PageSizeFilter.labels()

    def mount(self) -> None:
        self.payouts = payouts_query(
            app_name=self.app_name,
            selected_page_size=self.selected_page_size,
            selected_duration=self.selected_duration,
            selected_min_value=self.selected_min_value,
        )

    def updated_selected_page_size(self, selected_page_size: int) -> None:
        """Update page size limit"""
        self.selected_page_size = int(selected_page_size)
        self.payouts = payouts_query(
            app_name=self.app_name,
            selected_page_size=self.selected_page_size,
            selected_duration=self.selected_duration,
            selected_min_value=self.selected_min_value,
        )

    def updated_selected_duration(self, selected_duration: int) -> None:
        """Filter query by duration"""
        self.selected_duration = int(selected_duration)
        self.payouts = payouts_query(
            app_name=self.app_name,
            selected_page_size=self.selected_page_size,
            selected_duration=self.selected_duration,
            selected_min_value=self.selected_min_value,
        )

    def updated_selected_min_value(self, min_value: float) -> None:
        """Filter query by minimum payout"""
        self.selected_min_value = float(min_value)
        self.payouts = payouts_query(
            app_name=self.app_name,
            selected_page_size=self.selected_page_size,
            selected_duration=self.selected_duration,
            selected_min_value=self.selected_min_value,
        )

    def refresh_payouts_query(self) -> None:
        """Refresh the payouts query and re-populate the table"""
        self.payouts = payouts_query(
            app_name=self.app_name,
            selected_page_size=self.selected_page_size,
            selected_duration=self.selected_duration,
            selected_min_value=self.selected_min_value,
        )
