import stripe
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from planetarium.models import Booking


stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutSessionCreateView(APIView):
    permission_classes = ()

    def post(self, request):
        booking_id = request.data.get("booking_id")
        if not booking_id:
            return Response(
                {"error": "Booking ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        booking = get_object_or_404(Booking, id=booking_id)

        amount = booking.calculate_booking_price()
        amount_kopiyok = int(amount * 100)

        success_url = (
            request.build_absolute_uri(reverse("payment:stripe-success"))
            + "?session_id={CHECKOUT_SESSION_ID}"
        )
        cancel_url = (
            request.build_absolute_uri(reverse("payment:stripe-cancel"))
            + "?session_id={CHECKOUT_SESSION_ID}"
        )

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "uah",
                            "product_data": {
                                "name": f"Booking #{booking.id} of {booking.user}",
                            },
                            "unit_amount": amount_kopiyok,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        Payment.objects.create(
            booking=booking,
            amount=amount,
            session_id=session.id,
            session_url=session.url,
        )

        return Response({"session_id": session.id, "session_url": session.url})


class CheckoutSessionSuccessView(APIView):
    permission_classes = ()

    def get(self, request):
        session_id = request.GET.get("session_id")
        if not session_id:
            return Response(
                {"error": "Session ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                payment = get_object_or_404(Payment, session_id=session.id)
                if payment:
                    payment.status = "completed"
                    payment.save()
                    return Response(
                        {
                            "message": "Payment successful",
                            "booking_id": payment.booking.id,
                        }
                    )

                return Response(
                    {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"error": "Payment not completed"}, status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.StripeError as e:
            return Response(
                {"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )


class CheckoutSessionCancelView(APIView):
    permission_classes = ()

    def get(self, request):
        session_id = request.GET.get("session_id")
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            return Response(
                {"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        if session:
            payment = get_object_or_404(Payment, session_id=session.id)
            payment.status = "cancelled"
            payment.save()
        return Response(
            {
                "message": "Payment was cancelled. You can try again.",
                "session_id": session.id,
                "session_url": session.url,
            }
        )
