from django.urls import path

from payment.views import (
    CheckoutSessionCreateView,
    CheckoutSessionSuccessView,
    CheckoutSessionCancelView,
)


urlpatterns = [
    path(
        "create/",
        CheckoutSessionCreateView.as_view(),
        name="stripe-checkout",
    ),
    path(
        "success/",
        CheckoutSessionSuccessView.as_view(),
        name="stripe-success",
    ),
    path(
        "cancel/",
        CheckoutSessionCancelView.as_view(),
        name="stripe-cancel",
    ),
]

app_name = "payment"
