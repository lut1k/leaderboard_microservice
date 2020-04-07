from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    # TODO разобрать с пагинацией большого количества игроков (OFFSET ломает Materialized view).
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200
