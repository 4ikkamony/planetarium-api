import pytest
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status

from planetarium.models import Show, ShowTheme, Dome, Event
from planetarium.serializers import ShowDetailSerializer


@pytest.fixture
def show_theme():
    return ShowTheme.objects.create(name="Drama")


@pytest.fixture
def another_show_theme():
    return ShowTheme.objects.create(name="Comedy")


@pytest.fixture
def dome():
    return Dome.objects.create(name="Main Dome", rows=10, seats_in_row=20)


@pytest.fixture
def show(show_theme):
    s = Show.objects.create(title="Test Show", description="A test description")
    s.show_themes.add(show_theme)
    return s


@pytest.fixture
def another_show(another_show_theme):
    s = Show.objects.create(title="Another Show", description="Another description")
    s.show_themes.add(another_show_theme)
    return s


@pytest.fixture
def create_shows(show_theme, another_show_theme):
    show1 = Show.objects.create(title="Show 1", description="Desc 1")
    show1.show_themes.add(show_theme)
    show2 = Show.objects.create(title="Show 2", description="Desc 2")
    show2.show_themes.add(another_show_theme)
    show3 = Show.objects.create(title="Show 3", description="Desc 3")
    return [show1, show2, show3]


@pytest.fixture
def future_date():
    return make_aware(datetime.now() + timedelta(days=1))


@pytest.fixture
def show_list_url():
    return reverse("planetarium:show-list")


@pytest.fixture
def single_show_url():
    return lambda pk: reverse("planetarium:show-detail", kwargs={"pk": pk})


@pytest.fixture
def single_add_event_url():
    return lambda pk: reverse("planetarium:show-add-event", kwargs={"pk": pk})


@pytest.mark.django_db
class TestShowViewSet:

    @pytest.mark.parametrize(
        "client_fixture, show_index, expected_status",
        [
            ("api_client_staff", 0, 200),
            ("api_client_staff", 1, 200),
            ("api_client_staff", 2, 200),
            ("api_client_regular", 0, 200),
            ("api_client_regular", 1, 200),
            ("api_client_regular", 2, 200),
            ("api_client", 0, 200),
            ("api_client", 1, 200),
            ("api_client", 2, 200),
        ],
    )
    def test_show_detail_get(
        self,
        client_fixture,
        show_index,
        expected_status,
        request,
        single_show_url,
        create_shows,
    ):
        client = request.getfixturevalue(client_fixture)
        show_instance = create_shows[show_index]
        response = client.get(single_show_url(show_instance.pk))
        assert response.status_code == expected_status
        if expected_status == 200:
            serializer = ShowDetailSerializer(
                show_instance, context={"request": request}
            )
            assert response.data == serializer.data

    @pytest.mark.parametrize(
        "client_fixture, theme_fixture, expected_titles",
        [
            ("api_client_regular", "show_theme", ["Test Show"]),
            ("api_client_regular", "another_show_theme", ["Another Show"]),
        ],
    )
    def test_show_list_filter_by_theme(
        self,
        client_fixture,
        theme_fixture,
        expected_titles,
        request,
        show_list_url,
        show,
        another_show,
    ):
        client = request.getfixturevalue(client_fixture)
        theme = request.getfixturevalue(theme_fixture)
        response = client.get(show_list_url, {"show_themes": theme.id})
        assert response.status_code == status.HTTP_200_OK
        returned_titles = [item["title"] for item in response.data]
        assert set(returned_titles) == set(expected_titles)

    @pytest.mark.parametrize(
        "client_fixture, search_query, expected_titles",
        [
            ("api_client_regular", "Test", ["Test Show"]),
            ("api_client_regular", "Another", ["Another Show"]),
            ("api_client_regular", "Nonexistent", []),
        ],
    )
    def test_show_list_search(
        self,
        client_fixture,
        search_query,
        expected_titles,
        request,
        show_list_url,
        show,
        another_show,
    ):
        client = request.getfixturevalue(client_fixture)
        response = client.get(show_list_url, {"search": search_query})
        assert response.status_code == status.HTTP_200_OK
        returned_titles = [item["title"] for item in response.data]
        assert set(returned_titles) == set(expected_titles)

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            ("api_client_staff", 201),
            ("api_client_regular", 403),
        ],
    )
    def test_create_show(
        self, client_fixture, expected_status, request, show_list_url, show_theme
    ):
        client = request.getfixturevalue(client_fixture)
        payload = {
            "title": "New Show",
            "description": "A new show",
            "show_themes": [show_theme.id],
        }
        response = client.post(show_list_url, payload, format="json")
        assert response.status_code == expected_status
        if expected_status == 201:
            created_show = Show.objects.get(title="New Show")
            assert show_theme in created_show.show_themes.all()

    @pytest.mark.parametrize(
        "client_fixture, expected_status",
        [
            ("api_client_staff", 201),
            ("api_client_regular", 403),
            ("api_client", 401),
        ],
    )
    def test_add_event(
        self,
        client_fixture,
        expected_status,
        request,
        single_add_event_url,
        show,
        dome,
        future_date,
    ):
        client = request.getfixturevalue(client_fixture)
        payload = {
            "events": [
                {
                    "event_time": future_date.isoformat(),
                    "dome": dome.id,
                }
            ]
        }
        response = client.post(single_add_event_url(show.pk), payload, format="json")
        assert response.status_code == expected_status
        if expected_status == 201:
            event = Event.objects.filter(show=show).first()
            assert event is not None
            assert event.dome == dome
