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


class ShowPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ("id", "poster")


class ShowSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(read_only=False, required=False, allow_null=True)
    events = EventSerializer(write_only=True, many=True)

    class Meta:
        model = Show
        fields = (
            "id",
            "title",
            "description",
            "show_themes",
            "events",
            "poster",
        )


class EventDateSerializer(serializers.ModelSerializer):
    event_date = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ("event_date",)

    def get_event_date(self, obj):
        return obj.event_time.date()


class ShowListSerializer(serializers.ModelSerializer):
    show_themes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    events_count = serializers.IntegerField(read_only=True)
    events_dates = EventDateSerializer(source="events", many=True, read_only=True)

    class Meta:
        model = Show
        fields = (
            "id",
            "title",
            "description",
            "show_themes",
            "events_count",
            "events_dates",
            "poster",
        )


class ShowDetailSerializer(serializers.ModelSerializer):
    show_themes = ShowThemeSerializer(many=True, read_only=True)
    events = EventListSerializer(
        many=True,
        read_only=True,
    )

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
    event = serializers.PrimaryKeyRelatedField(read_only=True)

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
    dome = DomeSerializer(many=False, read_only=True)
    taken_seats = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Event
        fields = ("id", "event_time", "show", "dome", "taken_seats")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "tickets", "created_at")


class BookingListSerializer(BookingSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


class BookingCreateSerializer(BookingSerializer):
    tickets = TicketSerializer(many=True, write_only=True)

    def validate_tickets(self, tickets):
        """Check if the requested seats are available."""
        if not tickets:
            raise serializers.ValidationError("At least one ticket must be booked.")

        event = self.context["event"]
        taken_seats = {(t.row, t.seat) for t in event.tickets.all()}

        for ticket in tickets:
            seat_tuple = (ticket["row"], ticket["seat"])
            if seat_tuple in taken_seats:
                raise serializers.ValidationError(
                    f"Seat {seat_tuple} is already taken."
                )

        return tickets

    def create(self, validated_data):
        """Create a booking with multiple tickets."""
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            user = self.context["request"].user
            event = self.context["event"]

            booking = Booking.objects.create(user=user)
            tickets = [
                Ticket(
                    event=event,
                    booking=booking,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    ticket_type=ticket["ticket_type"],
                )
                for ticket in tickets_data
            ]
            Ticket.objects.bulk_create(tickets)

        return booking
