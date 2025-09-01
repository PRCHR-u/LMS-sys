from rest_framework.pagination import PageNumberPagination

class CoursePaginator(PageNumberPagination):
    """
    Пагинатор для модели курсов.
    Позволяет выводить по 10 курсов на страницу.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class LessonPaginator(PageNumberPagination):
    """
    Пагинатор для модели уроков.
    Позволяет выводить по 20 уроков на страницу.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
