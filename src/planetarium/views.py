from django.db.models import F, Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from planetarium.models import ShowTheme, Dome, Show, Event, Booking
from planetarium.filters import ShowSearchFilter, BookingFilter
from planetarium.serializers import (
    ShowThemeSerializer,
    DomeSerializer,
    ShowSerializer,
    EventSerializer,
    EventListSerializer,
    ShowDetailSerializer,
    EventDetailSerializer,
    ShowListSerializer,
    BookingCreateSerializer,
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
    queryset = Show.objects.prefetch_related(
        "events",
        "events__dome",
        "show_themes",
    ).annotate(
        events_count=Count("events"),
    )

    serializer_class = ShowSerializer
    filter_backends = [DjangoFilterBackend, ShowSearchFilter]
    filterset_fields = [
        "show_themes",
    ]

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

    @action(detail=True, methods=["POST"], url_path="book-tickets")
    def book_tickets(self, request, pk=None):
        event = self.get_object()
        serializer = BookingCreateSerializer(
            data=request.data, context={"request": request, "event": event}
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        return Response(
            {"message": "Booking successful", "booking_id": booking.id},
            status=status.HTTP_201_CREATED,
        )


class BookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer

    queryset = Booking.objects.prefetch_related(
        "tickets__ticket_type",
        Prefetch(
            "tickets__event", queryset=Event.objects.select_related("show", "dome")
        ),
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
