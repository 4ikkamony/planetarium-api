import pytest
from django.urls import reverse
from rest_framework import status
from planetarium.models import Event, TicketType, Booking


@pytest.fixture
def event(dome, show, future_date):
    return Event.objects.create(show=show, dome=dome, event_time=future_date)


@pytest.fixture
def ticket_type():
    return TicketType.objects.create(
        category=TicketType.TicketCategory.ADULT, price=10.00
    )


@pytest.mark.django_db
def test_event_list(api_client, event):
    url = reverse("planetarium:event-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert any(item["id"] == event.id for item in response.data)


@pytest.mark.django_db
def test_event_detail(api_client, event):
    url = reverse("planetarium:event-detail", args=[event.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == event.id


@pytest.mark.django_db
def test_book_tickets_unauthenticated(api_client, event, ticket_type):
    url = reverse("planetarium:event-book-tickets", args=[event.id])
    payload = {"tickets": [{"row": 1, "seat": 1, "ticket_type": ticket_type.id}]}
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_tickets_authenticated(api_client_regular, regular_user, event, ticket_type):
    client = api_client_regular
    url = reverse("planetarium:event-book-tickets", args=[event.id])
    payload = {"tickets": [{"row": 1, "seat": 1, "ticket_type": ticket_type.id}]}
    response = client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    booking = Booking.objects.filter(user=regular_user).first()
    assert booking is not None
    assert response.data["message"] == "Booking successful"
    assert response.data["booking_id"] == booking.id


@pytest.mark.django_db
def test_book_tickets_invalid_payload(api_client_regular, event):
    client = api_client_regular
    url = reverse("planetarium:event-book-tickets", args=[event.id])
    payload = {}
    response = client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
