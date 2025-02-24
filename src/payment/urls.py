from django.urls import path

from payment.views import (
    CreateCheckoutSession,
    StripeSuccessAPI,
    StripeCancelAPI
)

urlpatterns = [
    path("stripe/checkout/", CreateCheckoutSession.as_view(), name="stripe-checkout"),
    path("stripe/success/", StripeSuccessAPI.as_view(), name="stripe-success"),
    path("stripe/cancel/", StripeCancelAPI.as_view(), name="stripe-cancel")
]

app_name = "payment"