from django.test import TestCase

from betika.models import Betika
from commons.constants import BettingApps
from commons.models import Payouts


class BetikaModelTest(TestCase):
    def test_model_creates_database_instance(self) -> None:
        """Assert that the model can create database instances"""
        Betika.objects.create(app=BettingApps.BETIKA.name, payout=2.20)
        self.assertEqual(Betika.objects.count(), 1)

    def test_model_queries_betika_instances_only(self) -> None:
        """Assert the Betika models only queries instances where the app field is Betika"""
        Betika.objects.bulk_create(
            [
                Betika(app=BettingApps.BETIKA.name, payout=2.20),
                Betika(app=BettingApps.BETGR8.name, payout=1.13),
            ]
        )

        self.assertEqual(Payouts.objects.count(), 2)
        self.assertEqual(Betika.objects.count(), 1)
