from rest_framework import pagination


class DjatePagePagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 250
