from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatsPagination(PageNumberPagination):
    page_size = 4


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
            },
            'count': self.page.paginator.count,
            'response': data
        })