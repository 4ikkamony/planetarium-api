from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiRequest,
    OpenApiResponse,
    OpenApiExample,
)
from planetarium.serializers import (
    BookingCreateSerializer,
    EventListSerializer,
    EventDetailSerializer,
)


book_tickets_schema = {
    "parameters": [
        OpenApiParameter(
            name="id",
            description="Event ID",
            required=True,
            location=OpenApiParameter.PATH,
            type=int,
        )
    ],
    "request": OpenApiRequest(BookingCreateSerializer),
    "responses": {
        201: OpenApiResponse(
            description="Booking created",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "booking_id": {"type": "integer"},
                },
            },
            examples=[
                OpenApiExample(
                    name="Create booking example",
                    value={"message": "Booking successful", "booking_id": 1},
                    response_only=True,
                )
            ],
        ),
        400: OpenApiResponse(
            description="Bad Request - Validation Error (Seat already taken)",
            response={
                "type": "object",
                "properties": {
                    "tickets": {"type": "array", "items": {"type": "string"}}
                },
            },
            examples=[
                OpenApiExample(
                    name="Seat Already Taken",
                    value={"tickets": ["Seat (1, 1) is already taken."]},
                    response_only=True,
                )
            ],
        ),
    },
}


event_detail_schema = {
    "responses": {
        200: OpenApiResponse(
            description="Event details",
            response=EventDetailSerializer,
            examples=[
                OpenApiExample(
                    name="Existing event example",
                    value={
                        "id": 1,
                        "event_time": "2025-02-24T13:00:00Z",
                        "show": 1,
                        "dome": {
                            "id": 1,
                            "name": "Harris Peterson Planetarium",
                            "rows": 10,
                            "seats_in_row": 12,
                        },
                        "taken_seats": [{"row": 1, "seat": 1}],
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            description="Event not found",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Event not found example",
                    value={"detail": "No Event matches the given query."},
                    response_only=True,
                )
            ],
        ),
    }
}


event_list_schema = {
    "responses": {
        200: OpenApiResponse(
            description="List of events",
            response=EventListSerializer,
            examples=[
                OpenApiExample(
                    name="List of events example",
                    value=[
                        {
                            "id": 4,
                            "event_time": "2025-02-25T09:00:00Z",
                            "show_title": "Neutron Stars",
                            "dome_name": "Harris Peterson Planetarium",
                        },
                        {
                            "id": 2,
                            "event_time": "2025-02-24T15:00:00Z",
                            "show_title": "Our Earth: From Birth to Dawn of Humankind",
                            "dome_name": "Harris Peterson Planetarium",
                        },
                    ],
                    response_only=True,
                )
            ],
        ),
    }
}
