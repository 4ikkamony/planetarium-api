from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    shows_search,
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

urlpatterns = [
    path("shows/search/", shows_search, name="shows-search"),
    path("", include(router.urls)),
]

app_name = "planetarium"
