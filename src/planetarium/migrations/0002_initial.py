# Generated by Django 5.1.6 on 2025-02-21 16:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("planetarium", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="dome",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="planetarium.dome",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="astronomy_show",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="planetarium.show",
            ),
        ),
        migrations.AddField(
            model_name="show",
            name="show_themes",
            field=models.ManyToManyField(
                related_name="astronomy_shows", to="planetarium.showtheme"
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="booking",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="planetarium.booking",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="planetarium.event",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="ticket_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="planetarium.tickettype",
            ),
        ),
    ]
