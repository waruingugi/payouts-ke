from django.test import TestCase

from commons.constants import BettingApps
from commons.models import Payouts
from winpesa.models import Winpesa


class WinpesaModelTest(TestCase):
    def test_model_creates_winpesa_database_instance(self) -> None:
        """Assert that the model can create database instances"""
        Winpesa.objects.create(app=BettingApps.WINPESA.name, payout=2.20)
        self.assertEqual(Winpesa.objects.count(), 1)

    def test_model_queries_winpesa_instances_only(self) -> None:
        """Assert the Betika models only queries instances where the app field is Betika"""
        Winpesa.objects.bulk_create(
            [
                Winpesa(app=BettingApps.WINPESA.name, payout=2.20),
                Winpesa(app=BettingApps.BETGR8.name, payout=1.13),
            ]
        )

        self.assertEqual(Payouts.objects.count(), 2)
        self.assertEqual(Winpesa.objects.count(), 1)
