from datetime import datetime, timedelta

import pytest
from django.utils.timezone import make_aware

from planetarium.models import ShowTheme, Dome, Show


@pytest.fixture
def show_theme():
    return ShowTheme.objects.create(name="Mars")


@pytest.fixture
def another_show_theme():
    return ShowTheme.objects.create(name="Venus")


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
def future_date():
    return make_aware(datetime.now() + timedelta(days=1))
