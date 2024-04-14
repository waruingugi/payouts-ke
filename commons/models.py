from django.db import models

from commons.base_model import Base
from commons.constants import APP_CHOICES


class Payouts(Base):
    """The payouts of each betting app.
    This is the payout at which the plane crashed."""

    app = models.CharField(choices=APP_CHOICES, max_length=50, null=True, blank=False)
    payout = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Payout"
        verbose_name_plural = "Payouts"
