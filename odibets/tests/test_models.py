from django.test import TestCase

from commons.constants import BettingApps
from commons.models import Payouts
from odibets.models import Odibets


class OdibetsModelTest(TestCase):
    def test_model_creates_odibets_database_instance(self) -> None:
        """Assert that the model can create database instances"""
        Odibets.objects.create(app=BettingApps.ODIBETS.name, payout=2.20)
        self.assertEqual(Odibets.objects.count(), 1)

    def test_model_queries_odibets_instances_only(self) -> None:
        """Assert the Betika models only queries instances where the app field is Betika"""
        Odibets.objects.bulk_create(
            [
                Odibets(app=BettingApps.ODIBETS.name, payout=2.20),
                Odibets(app=BettingApps.BETGR8.name, payout=1.13),
            ]
        )

        self.assertEqual(Payouts.objects.count(), 2)
        self.assertEqual(Odibets.objects.count(), 1)
