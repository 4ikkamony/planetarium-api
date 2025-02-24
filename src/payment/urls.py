from django.urls import path

from payment.views import (
    CheckoutSessionCreateView,
    CheckoutSessionSuccessView,
    CheckoutSessionCancelView,
)


urlpatterns = [
    path(
        "stripe/checkout/create/", CheckoutSessionCreateView.as_view(), name="stripe-checkout"
    ),
    path(
        "stripe/checkout/success/", CheckoutSessionSuccessView.as_view(), name="stripe-success"
    ),
    path("stripe/checkout/cancel/", CheckoutSessionCancelView.as_view(), name="stripe-cancel"),
]

app_name = "payment"
