from rest_framework.pagination import PageNumberPagination     # для пагинации

class StaffPagination(PageNumberPagination): # класс для настройки пагинации
    page_size = 2                           # количество записей на странице
    page_query_param = 'page'               # параметр запроса для страницы