import csv
from os import path
from pathlib import Path

from django.test import TestCase

from commons.models import Payouts

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PAYOUT_DATA = path.join(BASE_DIR, "data", "payouts.csv").replace("\\", "/")


class SeedDBTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """Set up database by loading data from csv file"""
        super().setUpTestData()
        instances = []

        with open(PAYOUT_DATA, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                instance = Payouts(**row)
                instances.append(instance)

        Payouts.objects.bulk_create(instances)
