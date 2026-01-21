from django.urls import path, include
from .views import (
    StaffListView,
    EmployeeDetailView,
    UserDetailView,
    UserListView,
    index,
    SkillViewSet,
    SkillLevelViewSet,
    EmployeeImageViewSet,
    WorkplaceViewSet,
    UserViewSet,
    EmployeeViewSet
)

from rest_framework.routers import DefaultRouter    # роутер для api

app_name = "staff"  # имя приложения, которое будет использоваться в шаблонах для url A

    # для FBV представления
    # path('', index),                  # для FBV представления ссылка на функцю-обработчик staff/views/index.py
    # path('employee/<int:pk>/', detail),   # для FBV представления ссылка на функцю-обработчик staff/views/detail.py,
    # /<int:pk>/ - параметр пути в url для передачи в функцию-обработчик staff/views/detail.py
    # int - это конвертер типа пути, который преобразует строку в неотрицательное целое число

    # для CBV представления
    # используются классы EmployeeListView EmployeeDetailView в staff/views.py,
    # а в name= указывается 'user-list' 'user-detail' 'staff-list' 'employee-detail'- имена url-паттернов (в шаблонах),
    # /<int:pk>/ - параметр пути в url для встроенной функции-обработчик в классе DetailView
    # с конвертером int (строку в неотрицательное целое).
    # При необходимости изменения адреса страницы достаточно изменить адрес только в   path(''...   - имена url не меняются.

# Экземпляр роутера для API
router = DefaultRouter()
# Адреса страниц API
# r - признак, что путь должен быть интерпретирован как регулярное выражение, 
# адрес будет достраиваться по адресу, начиная с /api/
router.register(r'employees', EmployeeViewSet)  
router.register(r'skills', SkillViewSet)
router.register(r'skill-levels', SkillLevelViewSet)
router.register(r'workplaces', WorkplaceViewSet)
router.register(r'employee-images', EmployeeImageViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path(
        "staff/",
        StaffListView.as_view(),
        name="staff-list-all",
    ),  # URL страницы со списком всех сотрудников
    path(
        "",
        # UserListView.as_view(),
        # name="user-list",
        StaffListView.as_view(),
        name="staff-last4",
    ),  # URL главной страницы со списком 4х недавно принятых сотрудников
    path(
        "employee/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),  # URL страницы с карточкой сотрудника
    path(
        "user/<int:pk>/",
        UserDetailView.as_view(),
        name="user-detail",
    ),  # URL страницы с карточкой пользователя
]

# Адреса страниц API. 
# Для исключения конфликтов с адресами обычных страниц сайта организовано пространство имён "staff" 
# с указанием имени приложения (app_name="staff")
urlpatterns +=[path("api/", include((router.urls, "staff"), namespace="staff")),] 
#urlpatterns.append(path("api/", include(router.urls)))