from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from planetarium.models import ShowTheme, Dome, Show, Event, Booking

from planetarium.serializers import (
    ShowThemeSerializer,
    DomeSerializer,
    ShowSerializer,
    EventSerializer,
    EventListSerializer,
    ShowDetailSerializer,
    EventDetailSerializer,
    ShowListSerializer,
    BookingSerializer,
    BookingListSerializer,
)


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class DomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Dome.objects.all()
    serializer_class = DomeSerializer


class ShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Show.objects.prefetch_related("show_themes")
    serializer_class = ShowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowListSerializer

        if self.action == "retrieve":
            return ShowDetailSerializer

        return ShowSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = (
        Event.objects.all()
        .select_related("show", "dome")
        .annotate(
            tickets_available=(
                F("dome__rows") * F("dome__seats_in_row") - Count("tickets")
            )
        )
    )
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer

        if self.action == "retrieve":
            return EventDetailSerializer

        return EventSerializer


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Booking.objects.prefetch_related(
        "tickets__event__show", "tickets__event__dome"
    )
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return BookingListSerializer

        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
