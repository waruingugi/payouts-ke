from datetime import timedelta
from uuid import uuid4

from betika.components.betika_payouts import BetikaPayoutsView
from betika.models import Betika
from commons.base_tests import SeedDBTestCase
from commons.components.payouts import DurationFilter, MinValueFilter, PageSizeFilter


class PayoutsComponentTestCase(SeedDBTestCase):
    comp_name: str = "payouts"
    comp_id: str = str(uuid4())
    comp = BetikaPayoutsView(component_name=comp_name, component_id=comp_id)

    def test_updated_selected_page_size_returns_correct_query(self) -> None:
        """Test changing page size filters updates the query"""
        for filter in PageSizeFilter:
            page_size = filter.value
            self.comp.updated_selected_page_size(page_size)
            self.assertTrue(len(self.comp.payouts), page_size)  # type: ignore

    def test_updated_selected_min_value_returns_correct_query(self) -> None:
        """Test changing min value filters updates the query"""
        for filter in MinValueFilter:
            min_value = filter.value
            self.comp.updated_selected_min_value(min_value)

            # Check if all payouts in the queryset are greater than the min value
            self.assertTrue(
                all(obj["payout"] >= min_value for obj in self.comp.payouts)
            )  # type: ignore

    def test_updated_updated_selected_duration_returns_correct_query(self) -> None:
        """Test changing duration filters updates the query"""
        for filter in DurationFilter:
            duration_value = filter.value
            self.comp.updated_selected_duration(duration_value)

            # Get the most recent date-time from the database
            recent_time = Betika.objects.first().created_at  # type: ignore
            duration = recent_time - timedelta(hours=duration_value)

            # Check if all payouts in the queryset are greater than the duration value
            self.assertTrue(
                all(obj["created_at"] >= duration for obj in self.comp.payouts)
            )  # type: ignore
