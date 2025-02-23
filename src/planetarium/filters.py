from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    TrigramSimilarity,
)

from planetarium.models import Booking


class ShowSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query = request.query_params.get("search", "").strip()
        if not query:
            return queryset

        search_query = SearchQuery(query)
        search_vector = SearchVector("title", "description")

        results = (
            queryset.annotate(
                search_vector=search_vector,
                relevance=SearchRank(search_vector, search_query),
            )
            .filter(search_vector=search_query)
            .order_by("-relevance")
        )

        if not results.exists():
            results = (
                queryset.annotate(
                    relevance=(
                        TrigramSimilarity("title", query)
                        + TrigramSimilarity("description", query)
                    )
                )
                .filter(relevance__gt=0.05)
                .order_by("-relevance")
            )

        return results


class BookingFilter(filters.FilterSet):
    event_time = filters.DateFromToRangeFilter(field_name="tickets__event__event_time")
    event_id = filters.NumberFilter(field_name="tickets__event__id")
    show_id = filters.NumberFilter(field_name="tickets__event__show__id")
    dome_id = filters.NumberFilter(field_name="tickets__event__dome__id")

    class Meta:
        model = Booking
        fields = [
            "event_time",
            "event_id",
            "show_id",
            "dome_id",
        ]

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).distinct()
