from django.db import models

from commons.constants import BettingApps
from commons.models import Payouts


class Betgr8Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(app=BettingApps.BETGR8.value)


class Betgr8(Payouts):
    objects = Betgr8Manager()  # type: ignore

    class Meta:
        proxy = True
