from django.db import transaction
from rest_framework import serializers


from planetarium.models import (
    ShowTheme,
    Dome,
    Show,
    Event,
    TicketType,
    Ticket,
    Booking,
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class DomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dome
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
        )


class ShowPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ("id", "poster")


class ShowSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(read_only=False, required=False, allow_null=True)

    class Meta:
        model = Show
        fields = (
            "id",
            "title",
            "description",
            "show_themes",
            "poster",
        )


class ShowListSerializer(serializers.ModelSerializer):
    show_themes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Show
        fields = (
            "id",
            "title",
            "description",
            "show_themes",
            "poster",
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "event_time", "show", "dome")


class EventListSerializer(EventSerializer):
    show_title = serializers.CharField(source="show.title", read_only=True)
    dome_name = serializers.CharField(source="dome.name", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "event_time",
            "show_title",
            "dome_name",
        )


class ShowDetailSerializer(serializers.ModelSerializer):
    show_themes = ShowThemeSerializer(many=True, read_only=True)
    events = EventListSerializer()

    class Meta:
        model = Show
        fields = (
            "id",
            "title",
            "description",
            "show_themes",
            "poster",
            "events",
        )


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = (
            "id",
            "category",
            "price",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "event", "ticket_type")


class TicketListSerializer(TicketSerializer):
    event = EventListSerializer(many=False, read_only=True)
    ticket_type = TicketTypeSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class EventDetailSerializer(EventSerializer):
    show = ShowListSerializer(many=False, read_only=True)
    dome = DomeSerializer(many=False, read_only=True)
    taken_seats = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Event
        fields = ("id", "event_time", "show", "dome", "taken_seats")


class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Booking
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Booking.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class BookingListSerializer(BookingSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
