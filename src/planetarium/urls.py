from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    DomeViewSet,
    ShowViewSet,
    EventViewSet,
    BookingListView,
)

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet, basename="show-theme")
router.register("domes", DomeViewSet)
router.register("shows", ShowViewSet)
router.register("events", EventViewSet)

urlpatterns = [
    path("bookings/", BookingListView.as_view(), name="booking-list"),
    path("", include(router.urls)),
]

app_name = "planetarium"
