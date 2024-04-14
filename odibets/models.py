from django.db import models

from commons.constants import BettingApps
from commons.models import Payouts


class OdibetsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(app=BettingApps.ODIBETS.value)


class Odibets(Payouts):
    objects = OdibetsManager()  # type: ignore

    class Meta:
        proxy = True
