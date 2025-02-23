from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
    OpenApiTypes,
    OpenApiRequest,
)
from planetarium.serializers import (
    ShowListSerializer,
    ShowDetailSerializer,
    ShowSerializer,
)


show_list_schema = {
    "description": "Get list of Shows",
    "parameters": [
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            description="Search term for search on title and description.",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="show_themes",
            type=OpenApiTypes.INT,
            description="Filter shows by theme id",
            required=False,
            location=OpenApiParameter.QUERY,
        ),
    ],
    "responses": {
        200: OpenApiResponse(
            description="List of shows",
            response=ShowListSerializer,
            examples=[
                OpenApiExample(
                    name="Show List Example",
                    value=[
                        {
                            "id": 1,
                            "title": "Our Earth: From Birth to Dawn of Humankind",
                            "description": "A breathtaking journey through time.",
                            "show_themes": ["Earth", "Solar System"],
                            "events_count": 3,
                            "poster": "http://127.0.0.1:8000/media/uploads/shows/poster1.jpeg",
                        }
                    ],
                    response_only=True,
                ),
                OpenApiExample(
                    name="Search: earth",
                    summary="Example response for search=earth",
                    value=[
                        {
                            "id": 1,
                            "title": "Our Earth: From Birth to Dawn of Humankind",
                            "description": "Embark on a breathtaking journey through our planet's history!",
                            "show_themes": ["Earth", "Solar System"],
                            "events_count": 3,
                            "events_dates": [
                                {"event_date": "2025-02-24"},
                                {"event_date": "2025-02-24"},
                                {"event_date": "2025-02-24"},
                            ],
                            "poster": "http://127.0.0.1:8000/media/uploads/shows/planet-earth-from-birth-to-dawn-of-humankind-4f429d0a-50b6-4005-9291-44ffaac2cd96.jpeg",
                        },
                        {
                            "id": 3,
                            "title": "Gas Giants: Our Faithful Guardians",
                            "description": "This show, accompanied by breathtaking visuals, will explore the vital role gas giants play in protecting Earth from asteroids",
                            "show_themes": ["Solar System"],
                            "events_count": 0,
                            "events_dates": [],
                            "poster": "http://127.0.0.1:8000/media/uploads/shows/gas-giants-out-faithful-guardians-72fcd169-de76-4f0b-a426-0e50855bb9c9.jpg",
                        },
                    ],
                    response_only=True,
                ),
            ],
        )
    },
}


show_detail_schema = {
    "description": "Get detailed display of a Show. ",
    "responses": {
        200: OpenApiResponse(
            description="Detailed show information",
            response=ShowDetailSerializer,
            examples=[
                OpenApiExample(
                    name="Show Detail Example",
                    value={
                        "id": 1,
                        "title": "Our Earth: From Birth to Dawn of Humankind",
                        "description": "Detailed description of the show.",
                        "show_themes": [
                            {"id": 1, "name": "Earth"},
                            {"id": 2, "name": "Solar System"},
                        ],
                        "poster": "http://127.0.0.1:8000/media/uploads/shows/poster1.jpeg",
                        "events": [
                            {
                                "id": 3,
                                "event_time": "2025-02-24T09:00:00Z",
                                "show_title": "Our Earth: From Birth to Dawn of Humankind",
                                "dome_name": "Harris Peterson Planetarium",
                            }
                        ],
                    },
                    response_only=True,
                )
            ],
        ),
        404: OpenApiResponse(
            description="Not Found - Show not found.",
            response=OpenApiTypes.OBJECT,
        ),
    },
}


show_create_schema = {
    "description": (
        "Create a new show. " "It has title, description, show_themes and poster fields"
    ),
    "request": {
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "example": "Mars: New Home"},
                "description": {
                    "type": "string",
                    "example": "Is life on Mars possible? Find out!",
                },
                "show_themes": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "example": [6],
                },
                "poster": {"type": "string", "format": "binary"},
            },
        },
    },
    "responses": {
        201: OpenApiResponse(
            description="Show successfully created",
            response=ShowSerializer,
            examples=[
                OpenApiExample(
                    name="Show Create Response Example",
                    value={
                        "id": 1,
                        "title": "Our Earth: From Birth to Dawn of Humankind",
                        "description": "A breathtaking journey through time.",
                        "show_themes": [1, 2],
                        "poster": "http://127.0.0.1:8000/media/uploads/shows/poster1.jpeg",
                    },
                    response_only=True,
                ),
            ],
        ),
        400: OpenApiResponse(
            description="Bad Request - Missing required fields",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name="Missing required fields example",
                    value={
                        "title": ["This field may not be blank."],
                        "description": ["This field may not be blank."],
                    },
                    response_only=True,
                ),
            ],
        ),
    },
}
