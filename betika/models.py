from django.db import models

from commons.constants import BettingApps
from commons.models import Payouts


class BetikaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(app=BettingApps.BETIKA.value)


class Betika(Payouts):
    objects = BetikaManager()  # type: ignore

    class Meta:
        proxy = True
