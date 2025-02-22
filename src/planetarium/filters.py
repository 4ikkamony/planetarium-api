from rest_framework.filters import BaseFilterBackend
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    TrigramSimilarity,
)


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
