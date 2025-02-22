import os
import uuid

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class Dome(models.Model):
    """Location where shows take place"""

    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class ShowTheme(models.Model):
    """Theme of the show"""

    name = models.CharField(max_length=255)


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


class Event(models.Model):
    """A specific planetarium event session in a specific Show"""

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="events")
    dome = models.ForeignKey(Dome, on_delete=models.CASCADE, related_name="events")
    event_time = models.DateTimeField()


class Booking(models.Model):
    """Booking of one or more tickets by a user"""

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )


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

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)


class Ticket(models.Model):
    """A ticket for a specific Event"""

    row = models.IntegerField()
    seat = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="tickets"
    )
    ticket_type = models.ForeignKey(
        TicketType, on_delete=models.CASCADE, related_name="tickets"
    )
