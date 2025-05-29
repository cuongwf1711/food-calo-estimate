# Copyright (C)
# date: 22-05-2025
# author: cuongwf1711
# email: ruivalien@gmail.com

"""My Input Image Pagination."""

from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyInputImagePagination(PageNumberPagination):
    """My Input Image Pagination."""

    # page_size_query_param = "page_size"
    # max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate the queryset."""
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view)

    def get_total_calories(self):
        """Get total calories."""
        return self.queryset.aggregate(total=Sum("calo"))["total"] or 0

    def get_paginated_response(self, data):
        """Get paginated response."""
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_calories": round(self.get_total_calories(), 2),
                "results": data,
            }
        )
