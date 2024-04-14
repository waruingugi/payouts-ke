import uuid

from django.db import models


class Base(models.Model):
    """
    All other models inherit from Base.
    Base contains common fields among the models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["payout"], name="payout_idx"),
            models.Index(
                fields=["-created_at", "payout"], name="created_at_payout_idx"
            ),
        ]
