from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    DomeViewSet,
    ShowViewSet,
    EventViewSet,
    BookingViewSet,
)

router = routers.DefaultRouter()
router.register("show-themes", ShowThemeViewSet, basename="show-theme")
router.register("domes", DomeViewSet)
router.register("shows", ShowViewSet)
router.register("events", EventViewSet)
router.register("bookings", BookingViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
