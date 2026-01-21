"""
URL configuration for staffmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin # импортируем модуль admin для работы с админкой
from django.urls import include, path # импортируем функции include() и path() для работы с URL

# импортируем модуль views из папки staff, содержащую функции-обработчики запросов
#from staff import views

# импорт модуля debug_toolbar для отладки
import debug_toolbar

# Импорт редактора django-ckeditor-5 для работы с HTML-редактором
import django_ckeditor_5

# импорт модуля settings и функции static
# для настройки обработки медиа-файлов проекта в режиме debug
# Кроме этого, в шаблонах следует загружать тег {% load static %}
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

# для работы с Swagger
from drf_yasg.views import get_schema_view  # Для добавления представление схемы Swagger к URL-адресам проекта Swagger
from drf_yasg import openapi                # Обеспечивает генерацию документов в стандарте OpenAPI для Swagger

# Для работы с JWT токенами
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


# Список всех адресов обработчиков запросов
urlpatterns = [
    # Для API
    #path("api/", include('staff.urls')),
    # URL для обработчика из модуля admin.py
    path("admin/", admin.site.urls, name="admin"),
    # URL для обработчика из проекта DjDt
#    path("__debug__/", include(debug_toolbar.urls)), # для отладки, для продакшена закомментировать
    # URL для редактора django-ckeditor-5
    path("admin/", include("django_ckeditor_5.urls")),
    # Путь поиска ссылок 'api/' в приложении staff для API
    #path("api/", include("staff.urls")),
    # Путь поиска ссылок в приложении staff для главной страницы
    path("", include("staff.urls")), 
]

"""
Эта настройка для работы с медиа файлами только в режиме разработки проекта: если DEBUG = True.
Если DEBUG = False, то функция static() не будет работать.
static() - возвращает путь к медиа файлу, если он существует.
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Staffmanager API",
        default_version='v1',
        contact=openapi.Contact(email='e@mail.ru'),
        license=openapi.License('BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# Адреса для Swagger
urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

# Для API
#urlpatterns += path("api/", include('staff.urls')),

# Для JWT получения, обновления и проверки токена
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]