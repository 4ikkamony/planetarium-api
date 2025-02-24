from drf_spectacular.utils import extend_schema

checkout_session_create_schema = extend_schema(
    description="Create a new Stripe Checkout Session for a Booking. Accepts a booking_id and returns a session_id and session_url.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "integer",
                    "example": 1,
                }
            },
            "required": ["booking_id"],
        }
    },
    responses={
        201: {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "example": "cs_test_abc123"},
                "session_url": {"type": "string", "example": "https://checkout.stripe.com/pay/cs_test_abc123"},
            },
        },
        303: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Checkout session already exists"},
                "session_id": {"type": "string", "example": "cs_test_existing"},
                "session_url": {"type": "string", "example": "https://checkout.stripe.com/pay/cs_test_existing"},
            },
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Booking was already paid for or Booking ID is required"},
            },
        },
        500: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Stripe error: <error message>"},
            },
        },
    }
)

checkout_session_success_schema = extend_schema(
    description="Retrieve a Stripe Checkout Session and mark the payment as successful if completed.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Payment successful"},
                "booking_id": {"type": "integer", "example": 1},
            },
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Payment was not completed"},
            },
        },
    }
)

checkout_session_cancel_schema = extend_schema(
    description="Cancel a Stripe Checkout Session, marking the payment as cancelled.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Payment was cancelled."},
                "session_id": {"type": "string", "example": "cs_test_abc123"},
                "session_url": {"type": "string", "example": "https://checkout.stripe.com/pay/cs_test_abc123"},
            },
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Stripe error: <error message>"},
            },
        },
    }
)
