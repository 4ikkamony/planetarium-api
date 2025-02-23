import os
import uuid

from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class Dome(models.Model):
    """Location where shows take place"""

    name = models.CharField(max_length=255)
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    seats_in_row = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return self.name


class ShowTheme(models.Model):
    """Theme of the show"""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


def show_poster_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    file_uploads_path = os.path.join("uploads/shows/", filename)
    return file_uploads_path


class Show(models.Model):
    """General information about a planetarium show"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    show_themes = models.ManyToManyField(ShowTheme, related_name="shows")
    poster = models.ImageField(null=True, upload_to=show_poster_file_path)

    def __str__(self) -> str:
        return self.title


class Event(models.Model):
    """A specific planetarium event session in a specific Show"""

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="events")
    dome = models.ForeignKey(Dome, on_delete=models.CASCADE, related_name="events")
    event_time = models.DateTimeField()

    def __str__(self) -> str:
        return (
            f"Event {self.id} "
            f"of {self.show} "
            f"in {self.dome} "
            f"at {self.event_time}"
        )


class Booking(models.Model):
    """Booking of one or more tickets by a user"""

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )

    def __str__(self) -> str:
        return f"Booking {self.created_at} by {self.user}"


class TicketType(models.Model):
    """Different ticket categories and their prices"""

    class TicketCategory(models.TextChoices):
        """Ticket category options"""

        ADULT = "adult", _("Adult")
        STUDENT = "student", _("Student")
        CHILD = "child", _("Child")
        WHEELCHAIR_USER = "wheelchair", _("Wheelchair User")
        COMPANION = "companion", _("Companion")

    category = models.CharField(
        max_length=20, choices=TicketCategory.choices, unique=True
    )

    def __str__(self):
        return f"{self.category} {self.price}"

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)


class Ticket(models.Model):
    """A ticket for a specific Event"""

    row = models.IntegerField(validators=[MinValueValidator(1)])
    seat = models.IntegerField(validators=[MinValueValidator(1)])
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="tickets"
    )
    ticket_type = models.ForeignKey(
        TicketType, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self) -> str:
        return f"Ticket {self.ticket_type} " f"row={self.row}, seat={self.seat} "
