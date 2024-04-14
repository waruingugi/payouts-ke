from django.db import models

from commons.constants import BettingApps
from commons.models import Payouts


class WinpesaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(app=BettingApps.WINPESA.value)


class Winpesa(Payouts):
    objects = WinpesaManager()  # type: ignore

    class Meta:
        proxy = True
