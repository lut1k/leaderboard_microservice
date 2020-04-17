from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    # TODO разобраться с пагинацией большого количества игроков (OFFSET ломает Materialized view),
    #  а использование order_by бессмысленно ...
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200
