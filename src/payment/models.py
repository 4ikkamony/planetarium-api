from django.utils.translation import gettext_lazy as _
from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255)
    session_url = models.URLField(max_length=510)
    booking = models.OneToOneField(
        "planetarium.Booking",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment",
    )

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
