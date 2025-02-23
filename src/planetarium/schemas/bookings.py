from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from planetarium.serializers import BookingListSerializer


booking_list_schema = {
    "parameters": [
        OpenApiParameter(
            name="event_time_after",
            type=OpenApiTypes.DATE,
            description="Filter events with event_time on or after this date.",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="event_time_before",
            type=OpenApiTypes.DATE,
            description="Filter events with event_time on or before this date.",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="event_id",
            type=OpenApiTypes.INT,
            description="Filter by Event ID.",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="show_id",
            type=OpenApiTypes.INT,
            description="Filter by Show ID.",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="dome_id",
            type=OpenApiTypes.INT,
            description="Filter by Dome ID.",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
    ],
    "responses": {
        200: OpenApiResponse(
            description="List of bookings",
            response=BookingListSerializer,
            examples=[
                OpenApiExample(
                    name="Booking List Example",
                    value=[
                        {
                            "id": 1,
                            "tickets": [
                                {
                                    "id": 1,
                                    "row": 1,
                                    "seat": 1,
                                    "event": {
                                        "id": 3,
                                        "event_time": "2025-02-24T09:00:00Z",
                                        "show_title": "Our Earth: From Birth to Dawn of Humankind",
                                        "dome_name": "Harris Peterson Planetarium"
                                    },
                                    "ticket_type": {
                                        "id": 1,
                                        "category": "adult",
                                        "price": "480.00"
                                    }
                                }
                            ],
                            "created_at": "2025-02-22T13:56:54.627000Z"
                        }
                    ],
                    response_only=True
                )
            ]
        )
    }
}
