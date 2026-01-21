# DJANGO

**ДЗ 1**
__Создано виртуальное окружение python 3.12 в папке DjangoSynergyProject.venv__

python3.12 -m venv .venv
.venv/Scripts/activate

__Установка Джанго версии 5.2.1.__
py -m pip install Django==5.2.1

__Установка автоформаттера black и сортировщика импортов isort__
pip install black
python -m pip install isort

__Создание Джанго-проекта staffmanager__
django-admin startproject staffmanager

__Создание Джанго-приложений staff (хранение инф. о персонале) и workplaces (хранение инф. о рабочих сестах)__
cd  staffmanager
py manage.py startapp staff
py manage.py startapp workplaces

__Регистрация приложений в settings.py__
Application definition
INSTALLED_APPS = [
    # Регистрируем приложения учёта персонала и рабочих мест в наcтройках
    'staff',
    'workplaces',
.............
]
__Создание пробного обработчика запросов в файле staff/views__
"""Для простоты вместо html шаблона используем класс HttpResponse - из пакета позволяет отправить текстовое содержимое.
Функция-обработчик index() принимает запрос request и возвращает ответ 'Здесь будет главная страница'  в теге h1 - заголовок первого уровня.
Для вызова этой функции-обработчика надо в Джанго-проекте staffmanager в urls.py внести в список адресов urlpatterns
адрес path('',views.index), по которому она находится. 
Путь 'staffmanager.urls' к файлу с адресами urls.py содержится в переменной ROOT_URLCONF в настройках проекта staffmanager в файле settings.py """

from django.http import HttpResponse

def index(request):
    return HttpResponse("Здесь будет главная страница")

__Внесение в список адресов обработчиков запросов в файле urls.py__
 #импортируем модуль views из папки staff, содержащую функции-обработчики запросов
from staff import views
urlpatterns = [
    path('admin/', admin.site.urls),                  # URL для обработчика из модуля 
    path('',views.index)                              # URL для обработчика index() 
]

__Запуск сервера на локальном хосте 127.0.0.1:8000__
cd staffmanager
py manage.py runserver

__Установка модуля отладки DebugToolbar__
cd..
pip install django-debug-toolbar

__Регистрация модуля отладки DebugToolbar в settings.py__
#1. Добавляем константу для DjDT, чтобы он понимал - запросы с каких IP адресов надо обрабатывать 
INTERNAL_IPS = ['127.0.0.1',]

INSTALLED_APPS = [
    ........................
    'django.contrib.staticfiles',
    # 2. Добавляем DjDT в список установленных приложений. DjDT must be after 'django.contrib.staticfiles'
    'debug_toolbar', 
]
MIDDLEWARE = [
    ...............................
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3. Добавляем DjDT в слой Middleware в качестве middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware', 
]
__Внесение обработчика из модуля DjDT в список адресов обработчиков запросов в файле urls.py__
 #импорт модуля debug_toolbar
import debug_toolbar

 #Список всех адресов обработчиков запросов
urlpatterns = [
    path('admin/', admin.site.urls),                  # URL для обработчика из модуля 
    path('__debug__/', include(debug_toolbar.urls) ), # URL для обработчика из другого джанго-проекта    
    path('',views.index)                              # URL для обработчика index() 
]



__Сохранение зависимостей в файле requirements.txt__
pip freeze > requirements.txt

__ДЗ 2__

__Создаём суперпользователя :__
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> py manage.py createsuperuser
Имя пользователя (leave blank to use 'evgenymini_s'): user1
Адрес электронной почты: 
Password: user1
Password (again):user1
Введённый пароль слишком похож на имя пользователя.
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully

__Устанавливаем WYSIWYG-редактор django_ckeditor_5__
pip install django-ckeditor-5

in file "staffmanager\staffmanager\settings.py":
INSTALLED_APPS = [
   .......
    # Регистрация WYSIWYG-редактора django-ckeditor-5
    'django_ckeditor_5',

  #Определим конфигурацию django-ckeditor-5: включаем режим полного набора инструментов и настраиваем высоту редактора
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    }
}

in file "staffmanager\staffmanager\urls.py":
path('admin/', include('django_ckeditor_5.urls')), # URL для редактора django-ckeditor-5

in file "staffmanager\staff\models.py":
from django_ckeditor_5.fields import CKEditor5Field  # Импортируем класс поля WYSIWYG-редактора django-ckeditor-5

class Employee(models.Model):
    ...
    description = CKEditor5Field(blank=True, null=True)

__Создание модели для хранения информации о сотрудниках. Расширение встроенной модели User__
в файле staffmanager\workplaces\models.py:
from django.contrib.auth.models import User          # Импортируем модель User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Связь с моделью User один к одному
    # Выбор пола
    gender = models.CharField(max_length=10, choices=(('male', 'Мужской'), ('female', 'Женский')))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # Отчество можно не указывать
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    # Связь с моделью Skills многие ко многим
    #skills = models.ManyToManyField(Skill, through='SkillLevel')         
    description = CKEditor5Field(blank=True, null=True)

    class Meta:         # Добавляем читабельность в админке
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):          # В заголовке карточки сотрудника вместо Employee object() будет имя и фамилия
        return(f'{self.first_name} {self.last_name}')


    
__Русификация полей:__
В моделях таблиц models.py и в конфигурациях  приложений apps.py указываем читабельные имена полей

В моделях models.py
 #staffmanager\staff\models.py
class Employee(models.Model):
................................
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

 #staffmanager\workplaces\models.py
 ...............................
 class Meta:
        verbose_name = 'Рабочее место'
        verbose_name_plural = 'Рабочие места'

В конфигурациях приложений
 #staffmanager\staff\apps.py:
class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'
    verbose_name = 'СОТРУДНИКИ'

 #staffmanager\workplaces\apps.py:
class WorkplacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workplaces'
    verbose_name = 'РАБОЧИЕ МЕСТА'

**ДЗ 2**
В приложении «сотрудники» созданы  модели для хранения
информации о сотрудниках с расширением встроенного класса User -
при создании класса Emplyee было создано отношение один-к-одному с User.
Названия полей русифицированы.
В админке "сотрудники" можно менять все поля, кроме Навыков.
Это из-за отношения многие (Сотрудники)-ко-многим(Навыки) через промежуточную таблицу Уровень навыка.
Для уровня навыка использованы валидаторы минимального(1) и максимального(10) значения уровня.
Для вывода навыков у пользователя была создана функция def employee_skills(self, obj):
Навык можно задавать в админке самого сотрудника. Для этого был наследован класс inline.
Для каждого навыка приведено описание.
Рабоичие места (один-к-одному с Сотрудниками) можно задавать как в админке сотрудника,
так и в общей админики Сотрудники.

Обновлены зависимости в файле requirements.txt:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject> pip freeze > requirements.txt

Рабочие файлы были отформатированы форматтером black:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> black staff\\
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staff\admin.py

All done! ✨ 🍰 ✨
1 file reformatted, 16 files left unchanged.
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> black staffmanager\\
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\asgi.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\wsgi.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\settings.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\staffmanager\urls.py

All done! ✨ 🍰 ✨
4 files reformatted, 1 file left unchanged.

(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> black workplaces\\
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\workplaces\models.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\workplaces\apps.py
reformatted C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager\workplaces\admin.py

All done! ✨ 🍰 ✨
3 files reformatted, 7 files left unchanged.

Далее приведены коды некоторых рабочих файлов:

__staffmanager\staff\models.py__

from django.db import models
from django.contrib.auth.models import User  # Импортируем модель User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)  # Для валидации поля level
from workplaces.models import Workplace  # Импортируем модель Workplace
from django_ckeditor_5.fields import (
    CKEditor5Field,
)  # Импортируем класс поля WYSIWYG-редактора django-ckeditor-5


    # Create your models here.


class Skill(models.Model):  # Класс Навык наследник базовой модели Model
    name = models.CharField(max_length=100)
    # Поле описания навыка (по желанию)
    description = CKEditor5Field(blank=True, null=True)

    # Добавляем читабельность в админке
    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Employee(models.Model):  # Класс Сотрудник наследник базовой модели Model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Связь с моделью User один к одному
    # Выбор пола
    gender = models.CharField(
        max_length=10, choices=(("male", "Мужской"), ("female", "Женский"))
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    # Отчество (по желанию)
    middle_name = models.CharField(
        max_length=100, verbose_name="Отчество", blank=True, null=True
    )
    # Связь с моделью Skill многие ко многим через модель SkillLevel
    skills = models.ManyToManyField(Skill, through="SkillLevel")
    # Связь с моделью Workplace один к одному.
    # Если не назначено, то в карточке сотрудника будет отображаться 'Рабочее место не назначено'
    # Удаление рабочего места не привидёт к удалению сотрудника (on_delete=models.SET_NULL)
    workplace = models.OneToOneField(
        Workplace,
        on_delete=models.SET_NULL,
        verbose_name="Рабочее место",
        blank=True,
        null=True,
    )
    # Описание сотрудника (по желанию)
    description = CKEditor5Field(blank=True, null=True)

    # Добавляем читабельность в админке
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    # В заголовке карточки сотрудника вместо Employee object() будет имя и фамилия
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    # Связь сотрудник/навык многие ко многим через модель SkillLevel
class SkillLevel(models.Model):  # Класс Уровень Навыка наследник базовой модели Model
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:  # Добавляем читабельность в админке
        verbose_name = "Уровень навыка"
        verbose_name_plural = "Уровни навыка"

    # Выводим в админке в виде: 'Сотрудник - Навык (уровень 1)'.
    # Если уровень 1, то выводим только 'Сотрудник - Навык'
    def __str__(self):
        if self.level == 1:
            return f"{self.employee} - {self.skill}"
        else:
            return f"{self.employee} - {self.skill} (уровень {self.level})"

__staffmanager\staff\admin.py__

from django.contrib import admin
from .models import Employee, Skill, SkillLevel

    # Register your models here.


@admin.register(Skill)  # Регистрируем модель Skill в админке
class SkillAdmin(admin.ModelAdmin):
    model = Skill

@admin.register(SkillLevel)  # Регистрируем модель SkillLevel в админке
class SkillLevelAdmin(admin.ModelAdmin):
    model = SkillLevel

    # Inline class для таблицы SkillLevel
    # Используется класс TabularInline, который представляет собой
    # табличное представление записей в административной панели
class SkillLevelInline(admin.TabularInline):
    model = SkillLevel
    extra = 0

@admin.register(Employee)  # Регистрируем модель Employee в админке c инлайнами
class EmployeeAdmin(admin.ModelAdmin):

    # Вывод всех навыков сотрудника в админке Сотрудники
    def employee_skills(self, obj):
        # Получение всех навыков пользователя
        a = obj.skills.all().values_list("name", flat=True).distinct()
        # Получение всех уровней навыков пользователя
        b = obj.skilllevel_set.all().values_list("level", flat=True).distinct()
        # Создание списка с названиями навыков и их уровнями
        c = []
        for i in range(len(b)):
            c.append(a[i] + f"({str(b[i])})")
        # Вывод элементов списка через запятую
        return ", ".join(c)

    employee_skills.short_description = "Навыки(уровень)"

    list_display = (
        "id",
        "first_name",
        "middle_name",
        "last_name",
        "employee_skills",
        "workplace",
        "description",
    )
    list_editable = (
        "first_name",
        "middle_name",
        "last_name",
        "workplace",
        "description",
    )
    search_fields = ("last_name",)
    list_filter = ("skills",)
    list_display_links = ("id",)
    # filter_horizontal = ('skills',)

    inlines = [SkillLevelInline]

    # class Meta:
    #     model = Employee
    #     fields = '__all__'

__staffmanager\workplaces\models.py__

from django.db import models

#Create your models here.


class Workplace(models.Model):
    table = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"

    def __str__(self):
        if self.table:
            return f"Рабочее место №{self.table}"
        else:
            return "Рабочее место не назначено"

__staffmanager\workplaces\admin.py__

from django.contrib import admin
from .models import Workplace
from staff.models import Employee

    # Register your models here.


    # Назначаем рабочие места прямо в фоме сотрудника
class EmployeeInline(admin.StackedInline):
    model = Employee
    extra = 0

    # Добавляем форму для ввода рабочих мест в админку в форме сотрудника
inlines = [EmployeeInline]
admin.site.register(
    Workplace,
)

*******************ДЗ 3   Представления (views) и шаблоны (templates)***********************************


Настройки шаблонов
__Подключить статические и медиа файлы Подключить шаблоны на уровне проекта__

В этом проекте для пользовательского интерфейса были выбраны представления
на основе классов Class-Based Views (CBV).
Использовались два класса представлений, встроенных в Django:
DetailView  - страница подробных сведений об объекте в модели базе данных;
ListView    - страница списка объектов модели базы данных.

На уровне проекта staffmanager были созданы ллокальные папки:
staffmanager\media      - локальная папка для хранения файлов пользователей;

staffmanager\static_dev - локальная папка для хранения статических файлов (подапки css, js, img, files);

staffmanager\templates  - для хранения шаблонов приложений, базовый шаблон base.html в корне папки,
                          подппапка staff с наследниками базового шаблона employee_detail.html и employee_list.html,
                          подпапка includes для шаблонов сторонних приложений;

__ФАЙЛ staffmanager\staffmanager\settings.py:__
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",   # Подключен Джанго-шаблонизатор (DjangoTemplates). 
                                                                        # Но можно использовать и Jinja2
        "DIRS": [BASE_DIR / 'templates'], # 'DIRS': [] поиск шаблонов по умолчанию будет в подпапке templates/app_name в папке приложения
                                          # или 'DIRS': [BASE_DIR / 'templates'] в указанной папке для хранения шаблонов в папке проекта BASE_DIR/,
        "APP_DIRS": True,                 # True - поиск шаблонов в папке приложения после поиска в папке проекта
    .................
    }
........................
]
STATIC_URL = "static/"        # Задано имя URL для статических файлов, которые будут доступны по адресу BASE_DIR / 'static_dev'
STATICFILES_DIRS = [
    BASE_DIR / "static_DEV",  # Локальная папка на уровне проекта static_dev для хранения статических файлов (подапки css, js, img, files..)
                              # Перед использованием в шаблонах надо загрузить тег {% load static %} в шаблонах
]

MEDIA_URL = 'media/'             # # Задано имя URL для загрузки файлов пользователями
MEDIA_ROOT = BASE_DIR / 'media'  # адрес локальной папки для хранения файлов пользователей

__ФАЙЛ staffmanager\staff\views.py:__

from .models import Employee
from django.contrib.auth.mixins import LoginRequiredMixin # для защиты доступа к страницам (для авторизованного пользователя,  
                                                          # например, для личного кабинета или для дилеров, или ...). 
                                                          # Указывается на первом месте в атрибутах класса
from django.views.generic import DetailView, ListView

"""
ПРЕДСТАВЛЕНИЕ CBV:
Для веб-интерфейса модели Employee используем встроенные классы ListView и DetailView
импортируем классы ListView и DetailView, модель Employee.
Имена шаблонов будут по умолчанию:
"""

class BookListView(LoginRequiredMixin, ListView):
    model = Employee

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Employee

__ФАЙЛ staffmanager\staffmanager\urls.py__

from django.contrib import admin
from django.urls import include, path

#импорт модуля debug_toolbar
import debug_toolbar

#Импорт редактора django-ckeditor-5
import django_ckeditor_5

#импорт модуля settings и функции static
#для настройки обработки медиа-файлов проекта в режиме debug
from django.conf import settings
from django.conf.urls.static import static  

#Список всех адресов обработчиков запросов
urlpatterns = [

    # Путь поиска ссылок в приложении staff для главной страницы
    path("", include("staff.urls")),
    # URL для обработчика из модуля admin.py
    path("admin/", admin.site.urls),
    # URL для обработчика из проекта DjDt
    path(
        "__debug__/", include(debug_toolbar.urls)
    ),
  
    # URL для редактора django-ckeditor-5    
    path(
        "admin/", include("django_ckeditor_5.urls")
    ),
    
]

"""
Эта настройка для работы с медиа файлами только в режиме разработки проекта: если DEBUG = True.
Если DEBUG = False, то функция static() не будет работать.
static() - возвращает путь к медиа файлу, если он существует.
"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

__ФАЙЛ staffmanager\staff\urls.py__

from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

app_name = 'staff'  # имя приложения, которое будет использоваться в шаблонах

urlpatterns = [
    # для CBV представления
    # используются классы EmployeeListView EmployeeDetailView в staff/views.py,
    # а в name= указывается 'employee_list' 'employee_detail'- имена url (в шаблонах),
    # /<int:pk>/ - параметр пути в url для встроенной функции-обработчик в классе DetailView 
    # с конвертером int (строку в неотрицательное целое).
    # При необходимости изменения адреса страницы достаточно изменить адрес только в   path(''...  ) - имена url не меняются.
    path('', EmployeeListView.as_view(), name='employee_list',),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail',), 
]

__Модели__

Установка стороннего приложения django-cleanup
для физического удаления файлов (например - фотографий из галерей сотрудников)
после удаления ссылок на них в админке или удаления моделей.
ВАЖНО! Приложение django_cleanup должно быть последним в списке установленных приложений

>>> pip install django-cleanup
INSTALLED_APPS = (
    ...,
    'django_cleanup.apps.CleanupConfig',
)

Установка библиотеки Pillow для обработки изображений.
>>>python -m pip install Pillow

staffmanager\staff\models.py:
-Добавляем модель EmployeeImage с отношением многие к одному с моделью Employee.
-Добавляем поля "is_main" - главное изображение (True, False) 
 и "order" - порядковый номер (неотрицательное) для ранжирования и сортировки

-Определяем в модели EmployeeImage функцию save(self, *args, **kwargs) сохранения изображений
 с установкой единого размера изображений 300х300 пикселей - используется библиотека Pillow
-При назначении нового или уже существующего изображения главным  
 прежнее главное изображение меняет этот признак на False.

 #Переопределяем метод сохранения изображения (Pillow)
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        if self.is_main: #Если новый признак фото "главное", то всем остальным главным меняем атрибут is_main=False
            EmployeeImage.objects.filter(employee=self.employee, is_main=True).exclude(pk=self.pk).update(is_main=False)
        if self.image:
            img = PILImage.open(self.image.path)
            img = img.resize([300, 300]) # Устанавливаем размер изображения
            img.save(self.image.path) # Сохраняем изменённое изображение
            return self.image

staffmanager\staff\admin.py:
 #Регистрируем модель EmployeeImage в админке с выводом всех полей
@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    class Meta:
        model = EmployeeImage
        fields = '__all__'

 #Регистрируем инлайн для изображений сотрудника в админке в табличном виде
class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage

staffmanager\templates\includes\employee_header.html

В шаблоне вывода карточки сотрудника первым выводим главное изоражение в красной рамке и
добавляем вывод всех остальных изображений в порядке order

 Изображения:
<ul>
    {% for image in employee.employee_gallery.all %} # Перебираем все изображения
        {% if image.is_main %}                       # Если это главное изображение
            <img src="{{ image.image.url }}" alt="PHOTO" style="border: 8px solid red;">    # выводим главное изображение в красной рамке
        {% endif %}
    {% endfor %}
</ul>
<ul>
    {% for image in employee.employee_gallery.all %}
        {% if image.image %}
            {% if not image.is_main %}
                <img src="{{ image.image.url }}" alt="PHOTO">
            {% endif %}
        {% else %}
            <p> "нет изображения, добавьте изображение или удалите объект" </p>
            {% endif %}
    {% endfor %}

__Шаблоны, представления и адреса:__

Все представления выполнены по подходу CBV. 
Рабочие файлы представлений были описаны выше.

В проекте Django кроме страниц админки организованы страницы:
-главная страница со списков всех пользователей  http://127.0.0.1:8000/
-страница со списком всех сотрудников   http://127.0.0.1:8000/staff/
-страница подробных сведений о пользователе http://127.0.0.1:8000/user/pk=user_id/
-страница подробных сведений о сотруднике    http://127.0.0.1:8000/employee/pk=employee_id/

Все шаблоны и статические файлы расположены на уровне проекта staffmanager/
и имеют стандартную архитектуру.

Папка staffmanager\static_dev содержит статические файлы. Подпапки css files img js.
Папка staffmanager содержит базовый шаблон base.html
Папка staffmanager\templates\staff содержит шаблоны-наследники для приложения staff.
Папка staffmanager\templates\includes содержит шаблоны для вставки в базовом шаблоне или в его наследниках

Для всех страниц проекта шаблоны наследуются от базового шаблона base.html, который:
-определяет одинаковый титул для всех страниц,
-выводит логотип Синергии,
-определяет поле блок-контента для наследников и
-создаёт две ссылки для перехода на главную страницу и на страницу списка сотрудников.

Для читабельности основных шаблонов громоздкие блоки были выведены в папку includes в виде отдельных шаблонов.
а в основных шаблонах вставлены ссылки на них. Пример:
В employee_detail.html:
{% include 'includes/employee_header.html' %}


На главной странице http://127.0.0.1:8000/ (шаблон )
-выводится список всех пользователей с использованием данных из встроенной модели пользователя User
-в списке пользователей созданы кнопки для перехода на страницу карточки подробных сведений о пользователе
Пример:
ПОДРОБНОСТИ О ПОЛЬЗОВАТЕЛЕ
/static/css/index.css
ПОЛЬЗОВАТЕЛЬ: user1
user.username - user1
user.password - pbkdf2_sha256$1000000$8VyAT9hx5zntiE2gBC2APc$WPl12Lhh7XkSyuucJuF/2HOuIbu5m+f1jIciGVt/r8Q=
user.email -
user.first_name -
user.last_name -
user.groups - auth.Group.None
user.user_permissions - auth.Permission.None
user.is_staff - True
user.is_superuser - True
user.is_active - True
user.date_joined - 5 сентября 2025 г. 6:24
user.last_login - 12 сентября 2025 г. 9:38

На странице сотрудников http://127.0.0.1:8000/staff/
-выводится список всех сотрудников с использованием данных из модели сотрудника Employee
-в списке сотрудников созданы кнопки для перехода на страницу карточки подробных сведений о сотруднике

Для оптимизации запросов к базе при выводе списка связанных объектов
(навык, уровень) из модели сотрудников Employee
в классе EmployeeDetailView (модуль staff/views.py)
была написана специальная функция get_queryset(self) :

    def get_queryset(self):
        return Employee.objects.prefetch_related('skilllevel_set').all()

Менеджер запроса к базе Employee.objects использует метод .prefetch_related,
выполняющий предварительную загрузку всех связанных отношением many-to many объектов,
а метод .all() возвращает список skilllevel_set из всех связанных объектов запроса.
Таким образом, имеем один запрос к базе вместо нескольких запросов.

Вывод навыков в шаблоне staffmanager\templates\includes\employee_header.html в цикле for:
<ul>
    {% for skill_ in employee.skilllevel_set.all %}
        <li>
            {{ skill_.skill.name }} ({{ skill_.level }})
        </li>
        {% empty %}
            <li>Нет навыков</li>
    {% endfor %}
</ul>

Пример:
ПОДРОБНОСТИ О СОТРУДНИКЕ
/static/css/index.css
СОТРУДНИК: user2 user2
user.username - user1
employee.user_id - 2
employee.email -
employee.first_name - user2
employee.last_name - user2
employee.gender - female
employee.workplace - Рабочее место №7
employee.description - <p>Сотрудница успешно прошла стажировку и работает в команде с 2021 года.&nbsp;</p>

Навыки(уровень):

фронтенд (1)
тестирование (2)
управление проектами (5)

Страницы подробных сведений о сотрудниках и пользователях доступны только авторизованным пользователям. 
Для контроля доступа к страницам использовался встроенный в Django класс LoginRequiredMixin
при создании классов path-паттернов в модуле staff/view.py:
class UserDetailView(LoginRequiredMixin, DetailView):
...........

class EmployeeDetailView(LoginRequiredMixin, DetailView):
...........

Обновлены зависимости в файле requirements.txt:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject> pip freeze > requirements.txt

Рабочие файлы были отформатированы форматтером black:
(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject> black staffmanager\


*******************ДЗ 4   Запросы в БД****************************

1. Добавить к модели сотрудника поля с датой приёма на работу и стаж в днях.

Для расчёта стажа переопределим метод модели save(). 
Стаж будет перерассчитываться при сохранении сотрудника, это поле будет не редактируемо.
Дата приёма на работу косвенно валидируется стажем.
Стаж неотрицателен - поэтому дата приёма на работу !!не может!! превышать текущую дату - возникнет !!!ошибка по стажу!!

***staffmanager\staff\models.py:***

class Employee(models.Model):  # Класс Сотрудник наследник базовой модели Model
............
    # Дата приёма на работу
    employment_date = models.DateField(verbose_name="Дата приёма на работу", blank=True, null=True)
    # Стаж в днях
    employment_days = models.PositiveIntegerField(verbose_name="Стаж в днях", blank=True, null=True, default=0, editable=False)
..............
    Выполним миграцию БД

    Изменим админку - добавим в отображение столбцы приёма на работу и стажа

***staffmanager\staff\admin.py***

    list_display = (
..................
        "employment_date",
        "employment_days",
....................
    )
    list_editable = (
........................
        "employment_date",
..........................
    )

    Изменим шаблон карточки сотрудника - добавим вывод приёма и стажа

***staffmanager\templates\includes\employee_header.html***

            СОТРУДНИК: {{ employee.first_name }} {{ employee.last_name }}
            <ul>
...............................................................................
                <li>Дата приёма на работу - {{ employee.employment_date }}</li>
                <li>Стаж в днях - {{ employee.employment_days }}</li>
.................................................................................
            </ul>

2. Создать  валидатор, который не допускает нахождение тестировщиков и разработчиков за соседними столами.
    Для этого  в модели Employee:
    ***staffmanager\staff\models.py***
    - импортируем встроенный в Django класс ValidationError
        from django.core.exceptions import ValidationError
    
    - создадим поле role с выбором ролей(должностей) у сотрудников из списка ROLES.
        class Employee(models.Model):
            ROLES = (
        ('frontend-developer','фронтенд разработчик'),
        ('backend-developer','бэкенд разработчик'), 
        ('qa-engineer', 'тестировщик'), 
        ('project-manager','руководитель проекта'), 
        ('prompt engineer', 'промпт-инженер'),
        ('other', 'другое'),
    )
        role = models.CharField(choices=ROLES, verbose_name="Роль", default='other', blank=True, null=True)

    - Напишем метод-валидатор def validate_workplace(self):, в котором получаем текущий номер рабочего места через запрос по связанному
        ОДИН К ОДНОМУ полю workplace,
        по списку из двух номеров соседних мест получаем сотрудников для этих мест через запрос к модели сотрудника Employee 
        с пробросом  к данным из связанной ОДИН К ОДНОМУ модели рабочего места Workplace. Формат проброса двойное нижнее подчеркивание:
        Employee.objects.filter(workplace__table__in=neighbour_workplaces). 
        
        Затем по ролям текущего сотрудника и его соседей работает логика валидации из нескольких логических конструкций,
        в результате которой возникают сообщения о недопустимом соседстве 
        с указанием соседа, его роли и номера его места и сохранение модели сотрудников не происходит.
        
        Для запуска пользовательского метода-валидатора служит встроенный метод  валидации clean(). 
        Дополнительно, при окончании пользовательской валидации рабочих мест  в методе save() вызывается 
        встроенный метод полной валидации модели full_clean() перед продолжением сохранения модели

         #Переопределяем метод сохранения
        def save(self, *args, **qkwargs):   
        .....................................
        self.full_clean()  # Проверяем валидность модели перед сохранением
        super().save(*args, **qkwargs)  # Продолжаем сохранять базовым методом модели

        #Переопределяем метод валидации
        def clean(self):
        self.validate_workplace()

            # Метод для валидации рабочего места
    def validate_workplace(self):
        place = self.workplace.table # Получаем номер рабочего места
        neighbour_workplaces = [place - 1, place + 1] # Соседние рабочие места
        neighbours = Employee.objects.filter(workplace__table__in=neighbour_workplaces)    # Сотрудники на соседних рабочих местах
        if self.role == "qa-engineer":  # Если сотрудник тестировщик
            for neighbour in neighbours:
                if neighbour.role == "frontend-developer":    # Если соседний сотрудник фронтенд разработчик
                    raise ValidationError(f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом")
                elif neighbour.role == "backend-developer":  # Если соседний сотрудник бэкенд разработчик
                    raise ValidationError(f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом")
        if self.role == "frontend-developer" or self.role == "backend-developer":  # Если сотрудник разработчик
            for neighbour in neighbours:
                if neighbour.role == "qa-engineer":    # Если соседний сотрудник тестировщик
                    raise ValidationError(f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом")
                
    - необходимо сделать миграцию базы данных.

    В админке сотрудника  прописываем в списках выводимых и редактируемых атрибутов роль сотрудника для вывода на общий экран
    ***staffmanager\staff\admin.py***
        list_display = (
.................
        "role",
 ................
    )
    list_editable = (
....................
        "role",
..................
    )

3. На главной странице добавить и вывести в произвольном месте шаблона страницы сотрудников общее
количество сотрудников в базе данных.
4. На главной странице вывести карточки только 4-х последних по дате приёма работы
сотрудников. 
На главной странице и в Списке всех сотрудниковВ карточку сотрудника добавить стаж работы в компании в днях
5. В Списке всех сотрудников вывести карточки сотрудников с пажинацией по 2 на странице.

В базовом шаблоне добавляем ссылки 
"На главную" на страницу http://127.0.0.1:8000/ со списком 4х последних нанятых сотрудников 
"На список сотрудников" на страницу staff/ всех сотрудников

***staffmanager\templates\base.html***
<a href="{% url 'staff:staff-last4' %}">На главную</a>
<a href="{% url 'staff:staff-list-all' %}">На список сотрудников</a></br>

В паттернах path в urls.py в приложении staff
задаём шаблон главной страницы http://127.0.0.1:8000/  
и страницы /staff списка всех сотрудников  

***staffmanager\staff\urls.py***
path("staff/", StaffListView.as_view(), name="staff-list-all",),    # URL страницы со списком всех сотрудников
path("", StaffListView.as_view(), name="staff-last4", ),            # URL главной страницы со списком 4х недавно принятых сотрудников

В представлениях приложения staff переопределяем метод get_context_data для модели StaffListView

***staffmanager\staff\views.py***
в модели StaffListView
class StaffListView(ListView):
-добавляем пагинацию по 2 записи на странице всех сотрудников:
-----------------------------------
     paginate_by = 2 # Число записей на странице
-----------------------------------     

 Переопределяем метод get_context_data и пишем код для выбора типа списка сотрудников при клике на ссылки на страницы.
При клике на ссылку "На главную" откроется страница http://127.0.0.1:8000/ со списком 4х последних нанятых сотрудников
При клике на ссылку "На список сотрудников" окроется страница staff/ всех сотрудников
В шаблоне staffmanager\templates\staff\employee_list.html в цикле for надо использовать список сотрудников с именем staff

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs) # Получаем базовый контекст запроса в виде словаря из класса ListView
    context['staff_list_length'] = self.model.objects.count() - агрегацию общего числа сотрудников count()
    context['staff_last4'] = self.model.objects.order_by('-employment_date')[:4] -  список последних 4х сотрудников,
                                                                                    отсортированных по дате приёма DSC 
                                                                                    (знак "-" перед именем поля сортировки)
    pattern_name = self.request.resolver_match.url_name # Получаем имя url-паттерна при клике на ссылку в базовом шаблоне base.html
    if pattern_name == 'staff-last4': 
        context['staff'] =  context['staff_last4']
    elif pattern_name == 'staff-list-all':
        context['staff'] =  context['object_list']

В шаблоне главной страницы employee_list.html размещаем обработку этих  контекст-данных {{ staff_list_length }} и {{ staff_last4 }} 
и, используя имя контекстного списка context['staff'], выводим в цикле for требуемые данные сотрудника employee
***staffmanager\templates\staff\employee_list.html***
    <h1>СПИСОК СОТРУДНИКОВ.</h1>
    <h1>Всего сотрудников: {{ staff_list_length }}</h1>
    <h2>{{ staff_last4 }}</h2></br></br>
    ----------------------------------------------
     {% for employee in staff %}
    <li>
        {% include 'includes/employee_card.html' %} 
    -----------------------------------------------

Добавляем код для перехода по страницам при пагинации
***staffmanager\templates\staff\employee_list.html***
        <!-- Пагинация -->
    <div class="pagination">
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">Предыдущая</a>
        {% endif %}
        
        Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Следующая</a>
        {% endif %}
    </div>

В инклюде в шаблон главной страницы выводим имя фамилию и стаж в днях сотрудника и ссылку "подробнее" на подробную карточку сотрудника 

***staffmanager\templates\includes\employee_card.html***
    <b>{{ forloop.counter1 }}.</b> Сотрудник: {{ employee.first_name }} {{ employee.last_name }}
            Стаж в Компании, дней ={{ employee.employment_days }}
    <a href="{% url 'staff:employee-detail' employee.id %}">Подробнее</a><br>

6. На Главной странице и в Списке всех сотрудников в карточку сотрудника добавить имя, фамилию, стаж в днях и главное изображение галереи
сотрудника.

Для вывода главного изображения сотрудника 
Оптимизированный запрос в базу данных
-Одним запросом в БД получаем из EmployeeImage список main_images всех главных изображений для сотрудников в списке context["staff"]
-Создаем словарь main_images_dict {id сотрудника:галвное изображение }
-В цикле по сотрудникам в context["staff"] передаём  главное изображение в карточку сотрудника

class StaffListView(ListView):
--------------------------------------------
def get_context_data(self, **kwargs):
-----------------------------------------------
  #Создаем словарь для быстрого доступа с учётом того, что у сотрудника только одно главное изображение

    main_images_dict = {img.employee_id: img for img in main_images}
    
    for employee in context["staff"]: # Для сотрудника по id из словаря получаем в карточку его главное изображение. Оно одно (если есть)
        try:
            employee.main_image = main_images_dict.get(
                employee.id
            )   
        except Exception:
            print(
                f"employee.id {employee.id} None image"
            )  # Вывод в терминал, если нет главного изображения
    return context                                                          # Возвращаем полученный контекст в шаблон
---------------------------------------------------

В инклюд-шаблоне  staffmanager\templates\includes\employee_card.html для шаблона staffmanager\templates\staff\employee_list.html
***staffmanager\templates\includes\employee_card.html***
<b>{{ forloop.counter }}.</b>  Сотрудник: {{ employee.first_name }} {{ employee.last_name }} Стаж в Компании, дней ={{ employee.employment_days }}
    <!--Путь к фото upload_to="employee_images/" указан в image - экземпляре класса ImageField() в модели EmployeeImage-->
    <!-- выводим главное изображение в красной рамке из контекстного объекта main_image -->
    <img src="{{ employee.main_image.image.url }}" alt="PHOTO" style="border: 8px solid red;"></br></br>  

7. Подробная карточка сотрудника
Добавьте в контекст и разместите в шаблоне главное изображение сотрудника. 

Для вывода главного изображения сотрудника (CBV класс ass EmployeeDetailView(LoginRequiredMixin, DetailView)):
- методом .get(is_main=True)  получаем главное изображение сотрудника
- сохраняем его в контекст-объекте context['main_image']. Оно у сотрудника единственное (если есть)

EmployeeDetailView(LoginRequiredMixin, DetailView):
--------------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.employee_gallery.get(is_main=True)   # Получаем в карточку сотрудника главное изображение
        return(context)                                                          # Возвращаем полученный контекст в шаблон
-----------------------------------------------

В инклюд-шаблоне  staffmanager\templates\includes\employee_header.html для шаблона staffmanager\templates\staff\employee_detail.html
***staffmanager\templates\includes\employee_header.html***
            <!--Путь к фото upload_to="employee_images/" указан в image - экземпляре класса ImageField() в модели EmployeeImage-->
            <!-- выводим главное изображение в красной рамке из контекстного объекта main_image -->
            <img src="{{ main_image.image.url }}" alt="PHOTO" style="border: 8px solid red;">

Выводим имя, фамилия, пол, навыки с уровнями освоения, стаж в днях, номер стола,галерея изображений (без первого).

Это было сделано в ДЗ 3   Представления (views) и шаблоны (templates)
через перебор изображений в цикле for с исключением из вывода главного изображения
***staffmanager\templates\includes\employee_header.html***

        <!-- Получаем данные сотрудника из встроенной модели Employee и выводим их списком -->
        СОТРУДНИК: {{ employee.first_name }} {{ employee.last_name }}</br>
            <ul>
                <li>user.username - {{ user.username}}</li>
                <li>employee.user_id - {{ employee.user_id }}</li>
                <li>email - {{ employee.email }}</li>
                <li>Имя - {{ employee.first_name }}</li>
                <li>Фамилия - {{ employee.last_name }}</li>
                <li>Пол - {{ employee.gender }}</li>
                <li>Дата приёма на работу - {{ employee.employment_date }}</li>
                <li>Стаж в днях - {{ employee.employment_days }}</li>
                <li>Номер стола - {{ employee.workplace }}</li>
                <li>Описание - {{ employee.description }}</li>
            </ul>
            Навыки(уровень):
            <ul>
                {% for skill_ in employee.skilllevel_set.all %}
                    <li>
                        {{ skill_.skill.name }} ({{ skill_.level }})
                    </li>
                    {% empty %}
                        <li>Нет навыков</li>
                {% endfor %}
            </ul>
            Изображения:
            <ul>
                {% for image in employee.employee_gallery.all %}
                    {% if image.image %}
                        {% if not image.is_main %}
                            <img src="{{ image.image.url }}" alt="PHOTO">
                        {% endif %}
                    {% else %}
                        <p> "нет изображения, добавьте изображение или удалите объект" </p>
                    {% endif %}
                {% endfor %}
            </ul>


# *******************ДЗ 5  ТЕСТИРОВАНИЕ****************************

1.Тестирование адресов**
Напишите тесты, проверяющие работоспособность и права доступа на адреса в проекте. 

2.Тестирование контекста 
Проверьте корректность информации, отдаваемой на адреса проекта. 

3.Тестирование валидатора 
Напишите тест, проверяющий работу валидатора, запрещающего невозможность для тестировщиков и разработчиков занимать соседние столы 

Тесты написаны в python-приложении tests.py в папке staff (персонал). 

Проведены позитивные и негативные тесты.

Добавлена программа перезаписи файла главного изображения сотрудника из-за его удаления при завершении отладочных тестов.
Запись проводилась с использованием модуля shutil на диск, класс InMemoryStorage не использовался.

При тесте валидатора был использован контекстный менеджер для получения результатов работы метода assertRaises, чтобы сам тест не «падал». Сообщения теста проверяются методом assertIn для идентификации валидации именно рабочего места workplace и выводятся в терминал. 

"""
Тестирование на базе UnitTest.
"""

from django.forms import ValidationError        # Импортируем класс для валидации форм
from django.test import TestCase                # Импортируем класс для тестирования

# Базу для тестирования динамических ссылок и контекстов создадим на уровне модуля, чтобы каждый раз её использовать.

from django.contrib.auth import get_user_model  # Импортируем функцию для получения модели пользователя
from .models import Employee, Skill, SkillLevel, EmployeeImage # Импортируем модели приложения staff
from workplaces.models import Workplace         # Импортируем модель Workplace

import shutil                                    # Импортируем модуль для работы с файловой системой

User = get_user_model()                         # Получаем модель пользователя

**Функция копирования изображения в staffmanager/media/ для проведения тестов.**
**Необходима, так как при удалении тестовых файлов удаляется и файл тестового изображения.**
**Используется здесь в целях демонстрации тестов.**
**В реальном проекте не рекомендуется. Альтернативный вариант - использовать**
**Класс InMemoryStorage для временного хранения файлов media в памяти без доступа к файлам на диске.**

def copy_test_image(source_file, dst_dir):
    if source_file and dst_dir:
        shutil.copy(source_file, dst_dir)
        return
    else: print("Ошибка копирования изображения")
    return

surce_file = 'C:\\Users\\EvgenyMINI_S\\PythonProjects\\DjangoSynergyProject\\staffmanager\\media\\employee_images\\image.jpg'
dst_dir = "C:\\Users\\EvgenyMINI_S\\PythonProjects\\DjangoSynergyProject\\staffmanager\\media"

def setUpModule():                              # Фикстура setUpModule 
                                                # - Функция, которая выполняется один раз перед запуском всех тестов 
                                                # Настройки тестов на уровне модуля tests.py

**# Создание пользователя без прав персонала**
    common_user = User.objects.create_user(
        id=3,
        username='common_user', 
        password='common_user',
        is_staff=False,
    )
**# Создание пользователя с правами персонала**
    user = User.objects.create_user(
        id=2,
        username='user', 
        password='user',
        is_staff=False
    )
**# Создание администратора**
    superuser = User.objects.create_superuser(
        id=1,
        username='admin', 
        password='admin',
        email='admin@admin.ru',
    )
**# Создание рабочих мест**
    Workplace.objects.create(table=1,)
    Workplace.objects.create(table=2,)
    Workplace.objects.create(table=3,)
    Workplace.objects.create(table=4,)
**# Создание навыков**
    skill_frontend = Skill.objects.create(name='frontend')
    skill_backend = Skill.objects.create(name='backend')
    skill_qa = Skill.objects.create(name='qa')
    skill_prompt_engineering = Skill.objects.create(name='prompt_engineering')

**# Создание сотрудников**
    Employee.objects.create(
        user_id=1,
        workplace_id=1,
        gender='male',
        first_name='employee',
        last_name='employee',
        role ='qa-engineer',
    )
    Employee.objects.create(
        user_id=2,
        workplace_id=2,
        gender='male',
        first_name='employee2',
        last_name='employee2',
        role ='project-manager',
    )
    Employee.objects.create(
        user_id=3,
        workplace_id=3,
        gender='male',
        first_name='employee3',
        last_name='employee3',
        role ='backend-developer',
    )
**# Создание уровней навыков у сотрудника**
    SkillLevel.objects.create(
        employee_id=1,
        skill = skill_frontend,
        level=10,
    )
    SkillLevel.objects.create(
        employee_id=1,
        skill = skill_backend,
        level=9,
    )
    SkillLevel.objects.create(
        employee_id=1,
        skill = skill_qa,
        level=8,
    )
    SkillLevel.objects.create(
        employee_id=2,
        skill = skill_frontend,
        level=3,
    )
    SkillLevel.objects.create(
        employee_id=2,
        skill = skill_backend,
        level=3,
    )
    SkillLevel.objects.create(
        employee_id=2,
        skill = skill_qa,
        level=3,
    )
    SkillLevel.objects.create(
        employee_id=3,
        skill = skill_frontend,
        level=8,
    )
    SkillLevel.objects.create(
        employee_id=3,
        skill = skill_backend,
        level=7,
    )
**# Создание изображений сотрудника в папке media**
    surce_file = 'C:\\Users\\EvgenyMINI_S\\PythonProjects\\DjangoSynergyProject\\staffmanager\\media\\employee_images\\test_image.jpg'
    dst_dir = "C:\\Users\\EvgenyMINI_S\\PythonProjects\\DjangoSynergyProject\\staffmanager\\media"
    copy_test_image(surce_file, dst_dir)
    # Создание изображений сотрудника
    EmployeeImage.objects.create(
        employee_id=1,
        image='test_image.jpg',
        is_main=True,
    )
    EmployeeImage.objects.create(
        employee_id=2,
        image='test_image.jpg',
        is_main=True,
    )
    EmployeeImage.objects.create(
        employee_id=3,
        image='test_image.jpg',
        is_main=True,
    )


**# Уничтожаем тестовую базу данных после завершения всех тестов**
def tearDownModule():
    User.objects.all().delete()
    Employee.objects.all().delete()
    Workplace.objects.all().delete()
    SkillLevel.objects.all().delete()
    Skill.objects.all().delete()
    EmployeeImage.objects.all().delete()

# Create your tests here.

# 1. Тесты, проверяющие работоспособность и права доступа на адреса в проекте.

class TestUrls(TestCase):
    # 1.Тестируем публичные URL-адреса, ожидаем status_code=200:
    """
    "/"             - главная страница со списком последних сотрудников, публичный адрес
    "/admin/login/" - страница входа, публичный адрес
    "/staff/"       - страница со списком всех сотрудников, публичный адрес
    """
    
    def test_public_urls(self):
        urls = ["/", "/admin/login/", "/staff/"]
        for url in urls:
            status_code = self.client.get(url).status_code  # функция client.get возвращает объект Response, .status_code возвращает код ответа сервера
            self.assertEqual(status_code, 200)              # assertEqual проверяет равенство кодов ответа
    
    # Тестируем адреса, доступные только авторизованным пользователям, ожидаем status_code=200:
    #   Авторизоваться могут только пользователи с правами персонала.
 
    # "/admin/"                   - страница начальная администратора: все авторизованные пользователи 
    # "/admin/staff/"             - страница  с персоналом: суперпользователь, авторизованные пользователи с нужным наборо прав
    # "/admin/auth/"              - страница  с пользователями: суперпользователь, авторизованные пользователи с нужным наборо прав                     
    # "/admin/staff/employee/"    - страница  с карточками сотрудников: 
    #                                       суперпользователь, авторизованные пользователи с нужным наборо прав

    # Тестирование доступа сперпользователя, ожидаем status_code=200
    def test_urls_superuser_(self):
        urls = ["/admin/", "/admin/staff/", "/admin/auth/", "/admin/staff/employee/"]
        # Авторизация пользователя  с правами персонала в системе
        self.client.login(username='admin', password='admin') 
        for url in urls:
            status_code = self.client.get(url).status_code  # функция client.get возвращает объект Response, .status_code возвращает код ответа сервера
            #print(url, status_code)
            #try:
            self.assertEqual(status_code, 200)              # assertEqual проверяет равенство кодов ответа
            #except: Exception

    
    # Проверка доступа авторизованного пользователя user без набора прав доступа. 
    # Проверяем доступ по адресу /admin/ и отказ доступа по остальным адресам.
    def test_user(self):
        urls = ["/admin/", "/admin/staff/", "/admin/auth/" , "/admin/staff/employee/"]
        # Авторизация пользователя  с правами пользователя в системе
        self.client.login(username='user', password='user') 
        for url in urls:
            status_code = self.client.get(url).status_code  # функция client.get возвращает объект Response, .status_code возвращает код ответа сервера
            if status_code == 200:
                self.assertEqual(status_code, 200)              # assertEqual проверяет равенство кодов ответа
            else:
                self.assertNotEqual(status_code, 200)           # Негативный тест assertNotEqual проверяет неравенство кодов ответа


# 2.Проверка передачи контекста в шаблоны
class TestContext(TestCase):

    # Страницы с пользователями, context["user"]:
    #   "/admin/auth/" 
    # Страницы с информацией о персонале:
    #   "/"                   context["staff"]
    #   "/staff/"             context["staff"]  
    #   ""/employee/1/        context["employee"]

    
    # Позитивный тест передачи контекста в шаблоны, проверка информации о сотруднике по id=1, context["staff"]
    def test_context_employee_pos(self):
        self.client.login(username='admin', password='admin')   # Авторизация в системе 
        url = "/employee/1/"                                    # Проверка контекста для страницы сотрудника ""/employee/1/", context["employee"]
        context = self.client.get(url).context                  #
        expected_employee = Employee.objects.get(id=1)          # Получение сотрудника из БД по id=1
        self.assertEqual(expected_employee, context["employee"])# assertEqual проверяет равенство объектов из БД и контекста


    # Негативный тест передачи контекста в шаблоны, context["staff"]
    # Предварительная (ограниченный набор номеров id) проверка отсутствия информации 
    # о сотрудниках c другими id.  У нас сотрудники с id=1, 2, 3. На главной странице список из 4-х "свежих" сотрудников
    def test_context_employee_neg(self):
        self.client.login(username='admin', password='admin')  # Авторизация в системе 
        url = "/"                                              # Проверка контекста для страницы "/", context["staff"]
        context = self.client.get(url).context                 # Получение контекста из ответа сервера
        unexpected_employees = Employee.objects.filter(id__in=[4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        for object in unexpected_employees:     # Перебор объектов, которые не должны быть в контексте
            with self.subTest(object=object):   # Метод subTest изолирует проверку блока кода 
                                                # позволяет группировать проверки внутри одного теста
                                                # и продолжать выполнение теста, если он не пройден
                if object in context["staff"]:   # Проверка наличия объекта в контексте context["staff"]
                    print(f"unexpected_employee id = {object.id}")
                    pass
                self.assertNotIn(object, context["staff"])  # assertNotIn проверяет отсутствие объекта в контексте
    
    # Позитивный тест проверки контекста для страницы "/" на число сотрудников, 
    # информация о которых есть в контексте, context["staff"]. У нас 3 сотрудника.
    def test_context_employee_neg(self):
        self.client.login(username='admin', password='admin')   # Авторизация в системе 
        url = "/"                                               # Проверка контекста для страницы "/", context["staff"]
        context = self.client.get(url).context                  # Получение контекста из ответа сервера
        expected_employees = Employee.objects.all()             # Получение списка всех сотрудников из БД
        context_employyes = context["staff"]                    # Получение списка сотрудников из контекста
        expected_employees_quantity = len(expected_employees)   # Получение количества объектов в списке БД
        context_employyes_quantity = len(context_employyes)     # Получение количества объектов в списке контекста
        # assertEqual проверяет равенство количества объектов в списках
        self.assertEqual(expected_employees_quantity, context_employyes_quantity)  
        
    # Позитивный тест
    # Проверка навыков сотрудника по контексту страницы "/employee/3/" у сотрудника с id=3 2 навыка из 4-х возможных 
    def test_employee_skills(self):
        self.client.login(username='admin', password='admin')   # Авторизация в системе 
        url = "/employee/3/"                                               # Проверка контекста для страницы "/employee/3/", context["employee"]
        context = self.client.get(url).context  
        employee = context["employee"]  
        skill_list = Skill.objects.filter(employee=employee).all()  # Получение списка навыков сотрудника
        skill_list_lenth = len(skill_list)  
        self.assertEqual(skill_list_lenth, 2)                       # assertEqual проверяет равенство длины списка навыков сотрудника


    # Позитивный тест
    # Проверка изображения сотрудника по контексту страницы "/employee/2/" у сотрудника с id=2 есть одно изображение 
    def test_employee_image(self):
        self.client.login(username='admin', password='admin')   # Авторизация в системе 
        url = "/employee/2/"                                               # Проверка контекста для страницы "/employee/2/", context["employee"]
        context = self.client.get(url).context                  # Получение контекста из ответа сервера
        employee = context["employee"]  
        image = EmployeeImage.objects.get(employee=employee)    # Получение изображения сотрудника
        self.assertIsNotNone(image)                             # assertIsNone подтверждает наличие картинки у сотрудника из контекста.
        

# 3.Тест валидатора рабочих мест workplace
class TestWorkplaceValdator(TestCase):
    """
    В тестовой базе сводбодно рабочее место №4. Место №3 занимает разработчик.
    Проверим работу валидатора, создавая на рабочем месте №4 сотрудника-тестировщика (должна быть ошибка валидации) 
    и сотрудника-разработчика (валидация должна быть успешной).
    """
    
    def test_workplace_validator(self):

        # Создание тестового пользователя с id=4
        User.objects.create(
            id=4,
            username="test",
            password="test",
            is_staff=True,
        )
        # Создание тестового сорудника с user id=4 на рабочем месте №4
        test_employee = Employee.objects.create(
            user_id=4,
            first_name="test",
            last_name="test",
            gender="male",
            workplace=Workplace.objects.get(id=4),
            )
        # На рабочем месте №3 сидит bacend-developer.
        # Назначаем тестовому сотруднику роль разработчика frontend-engineer.
        # Валидация должна проходить успешно
        Employee.objects.filter(id=4).update(role='frontend-developer')

        employee = Employee.objects.get(id=4)   # Получение сотрудника с id=4
        employee.full_clean()                   # Проверка валидации

        # Назначаем тестовому сотруднику роль тестировщика qa-egineer.
        # Валидация должна проходить ошибкой
        Employee.objects.filter(id=4).update(role='qa-engineer')

        employee = Employee.objects.get(id=4)   # Получение сотрудника с id=4
        # Внутри блока контекстного менеджера with с помощью класса ValidationError 
        # обрабатывается сообщение об ошибке валидации - если возникла ошибка валидации, 
        # то её сообщение будет записано в переменную mistake.exception
        with self.assertRaises(ValidationError) as mistake: 
            employee.full_clean()                   # Проверка валидации
        # Проверка assertIn того, что сообщение об ошибке валидации именно рабочего места workplace.
        self.assertIn("Нельзя размещать разработчиков и тестировщиков рядом", str(mistake.exception)) 
        print(str(mistake.exception))      
        
# *******************ДЗ 6  Django REST Framework****************************
# **************************************************************************

НЕ ВХОДИЛО В ДЗ 6: django-import-export
__Установка модуля django-import-export__
Служит для загрузки/выгрузки данных 
из/в файлов/файлы .CSV (по малчанию) .XLSX(указываем при установке) в/из таблицы БД.
После установки и настройки django-import-export в модели Employee в админке
модели появятся кнопки "ИМПОРТ" и "ЭКСПОРТ"
РУКОВОДСТВО ПО ДЖАНГО-ИМПОРТ-ЭКСПОРТ:
https://django-import-export.readthedocs.io/en/latest
>>(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> pip install django-import-export
>>(.venv) PS C:\Users\EvgenyMINI_S\PythonProjects\DjangoSynergyProject\staffmanager> pip install tablib[xlsx]

   ***staffmanager\staffmanager\settings.py***
from import_export.formats.base_formats import CSV, XLSX    # для импорта и экспорта данных в формате CSV и XLSX
    # Application definition
IMPORT_FORMATS = [CSV, XLSX]
EXPORT_FORMATS = [CSV, XLSX]

INSTALLED_APPS = (
    ...
    'import_export',
    ...
    )
    ***staffmanager\staff\admin.py***
    from import_export.admin import ImportExportModelAdmin
    from import_export import resources, fields
    
@admin.register(Employee)  
class EmployeeAdmin(ImportExportModelAdmin):
------------------------------------------------
 resources_class = [EmployeeResource]

НЕ ВХОДИЛО В ДЗ 6: Генератор документации Swagger/ReDoc
# Устанавливаем и регистрируем одновременно последние версии (-U) Swagger и ReDoc
>>(venv) pip install -U drf-yasg

***staffmanager\staffmanager\settings.py***
INSTALLED_APPS = [
-----------------------------
    'drf_yasg',         # для генерации документации по API
]

Добавляем URLs Swagger и ReDoc на уровне проекта
***staffmanager\staffmanager\urls.py***
#для работы с Swagger
from drf_yasg.views import get_schema_view  # Для добавления представление схемы Swagger к URL-адресам проекта Swagger
from drf_yasg import openapi                # Обеспечивает генерацию документов в стандарте OpenAPI для Swagger

urlpatterns = [
----------------------
]
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

НЕ ВХОДИЛО В ДЗ_6
    # Выводим в админке приложения workplaces список сотрудников на рабочих местах
***staffmanager\workplaces\admin.py***
    def employee_at_table(self, obj):
        if Employee.objects.filter(workplace_id=obj.id): # Проверяем наличие сотрудника на рабочем месте
            employee = Employee.objects.filter(workplace_id=obj.id) # Получаем список сотрудников (он может быть только один)
            return f"Сотрудник: {employee[0]}" # Возвращаем сотрудника
        else:
            return "Рабочее место свободно" # Возвращаем сообщение о том, что рабочее место свободно
    
    list_display = (
        "id",
        "table",
        "employee_at_table",
    )
    list_editable = (
       "table",
    )
# ********************************************************************************************************

Установите и настройте DRF в проект.

Создайте методы (эндпоинты, сериалайзеры и запросы) API:
¹ Получение списка всех сотрудников (с пажинацией по 10 на странице).
    Получение списка сотрудников с фильтрацией по параметрам (навыки, стаж)
¹ Получение подробной информации о сотруднике (аналог подробного личного дела)
¹ Добавление информации о сотруднике
¹ Изменение информации о сотруднике
¹ Удаление информации о сотруднике
¹ JWT Авторизация пользователей.

Пользователи системы и права доступа
1.Посетитель. Может просматривать каталог.
2.Смотритель. Может перемещать сотрудников между столами.
3.Администратор. Может добавлять, изменять, удалять сотрудников, а также перемещать их между столами.
Доступы до методов API и страниц должны соответствовать правам
пользователя.

**Создайте методы (эндпоинты, сериалазеры и запросы) API:**
1.Установка DRF Django-Rest-Framework в виртуальном окружении

>>pip install djangorestframework

2.Регистрация DRF в приложении staffmanager\staffmanager

***staffmanager\staffmanager\settings.py***

INSTALLED_APPS = [
--------------------------------------
    "django.contrib.staticfiles",
    # Добавляем приложение rest_framework
    'rest_framework',   # для работы с API
----------------------------------------    
]

3.Создание сериалайзеров (экземпляров класса ModelSerializer) 

в файле staffmanager\staff\serializers.py
Сериализер выступает в роли шаблона для API. Конвертирует данные из модели в JSON 
для передачи их в API (через представления из файла views.py по адресу из urls.py),
полученный ответ из API переводит из JASON в формат данных модели для загрузки в модель.

Для вывода подробных данных по всем связанным моделям в карточке сотрудника 
используем вложенные сериалайзеры
***staffmanager\staff\serializers.py***
from rest_framework import serializers      # Импортируем сериалайзеры из rest_framework 
                                            # для сериализации данных в формате JSON 
                                            # с использованием встроенного класса ModelSerializer
from django.contrib.auth.models import User # Импортируем модель User из django.contrib.auth.models 
                                            # для работы с пользователями
from .models import Skill,SkillLevel, EmployeeImage, Employee 
from workplaces.models import Workplace

    #Сериалайзеры для моделей проекта StaffManager
class SkillSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
#----------------------------------------------------

class EmployeeSerialaizer(serializers.ModelSerializer):
    # Вложенные сериалайзеры для связанных моделей
    skills = SkillSerialaizer(many=True, read_only=True)
    skilllevel = SkillLevelSerialaizer(read_only=True, many=True)
    workplace = WorkplaceSerialaizer(read_only=True)
    user = UserSerialaizer(read_only=True)
    employeeimage = EmployeeImageSerialaizer(read_only=True, many=True)

    class Meta:
        model = Employee
        fields = '__all__' # Вывод всех полей модели Employee

4.Создание представлений API  для модели Employee с использованием библиотеки ViewSet.

ViewSet это абстракция над APIView, которая позволяет автоматически управлять CRUD-операциями
GET /books/ — получить список всех объектов
POST /books/ — создать новый объект
GET /books/<pk>/ — получить объект по ID
PUT/PATCH /books/<pk>/ — обновить объект по ID
DELETE /books/<pk>/ — удалить объект по ID 
избавляя нас от необходимости писать однообразный код для стандартных методов.

Представления создадим на уровне приложения staff: staffmanager\staff\views.py
В представлениях предоставим возможность использовать миксины.
Основная идея — принцип Don’t Repeat Yourself (DRY): вместо того чтобы вручную реализовывать методы get(), post(), put(), delete() для каждого ресурса API, можно наследовать соответствующий миксин, который уже содержит необходимую реализацию.
CreateModelMixin — реализует метод .create() для обработки POST-запросов.
RetrieveModelMixin — предоставляет метод .retrieve() для обработки GET-запросов к конкретному объекту.
UpdateModelMixin — реализует методы .update() и .partial_update() для обработки PUT и PATCH-запросов соответственно.
DestroyModelMixin — предоставляет метод .destroy() для обработки DELETE-запросов
ListModelMixin — предоставляет метод .list() для обработки GET-запросов для получения списка объектов.


5.АДРЕСА API. Автоматическая генерация адресов страниц API.

В файле staffmanager\staff\urls.py укажем путь к API страницам, 
используя метод register из класса DefaultRouter(),
который берёт на себя задачу генерации URL-адресов на основе структуры ViewSet
для всех CRUD и других операций с объектами в вьюсетах
Добавим для перехода на API с lokalhost:
***staffmanager\staff\urls.py***
from django.urls import include

urlpatterns = [
----------------------
]

#Экземпляр роутера для API
router = DefaultRouter()

#Адреса страниц API
#r - признак, что путь должен быть интерпретирован как регулярное выражение, 
#адрес будет достраиваться по адресу, начиная с /api/staff/
router.register(r'employees', EmployeeViewSet)  
router.register(r'skills', SkillViewSet)
router.register(r'skill-levels', SkillLevelViewSet)
router.register(r'workplaces', WorkplaceViewSet)
router.register(r'employee-images', EmployeeImageViewSet)
router.register(r'users', UserViewSet)

#Адреса страниц API 
urlpatterns +=[ path("", include(router.urls)),]

На главной API странице http://127.0.0.1:8000/api/ будет словарь api-страниц:
{
    "employees": "http://127.0.0.1:8000/api/employees/",
    "skills": "http://127.0.0.1:8000/api/skills/",
    "skill-levels": "http://127.0.0.1:8000/api/skill-levels/",
    "workplaces": "http://127.0.0.1:8000/api/workplaces/",
    "employee-images": "http://127.0.0.1:8000/api/employee-images/",
    "users": "http://127.0.0.1:8000/api/users/"
}

На api-страницах ПРЕДСТАВЛЕНЫ ДОПУСТИМЫЕ CRUD-оперции

ПОДРОБНАЯ КАРТОЧКА СОТРУДНИКА по адресу http://127.0.0.1:8000/api/employees/employee_id


6.ПАГИНАЦИЯ API

Параметры пагинации задаём в отдельном файле staffmanager\staff\paginators.py
Пагинацию на уровне вьюсета EmployeeViewSet задаём непосредственно в файле staffmanager\staff\views.py 
через файл staffmanager\staff\paginators.py
***staffmanager\staff\paginators.py***
from rest_framework.pagination import PageNumberPagination     # для пагинации

class StaffPagination(PageNumberPagination): # класс для настройки пагинации
    page_size = 2                           # количество записей на странице
    page_query_param = 'page'               # параметр запроса для страницы

***staffmanager\staff\views.py***

from .paginators import StaffPagination                      # для пагинации выводим список сотрудников по 2 записи на странице

class EmployeeViewSet(viewsets.ModelViewSet,
-----------------------------------------------
):
    queryset = Employee.objects.all()  # Получаем список всех сотрудников
    serializer_class = EmployeeSerialaizer # экземпляр класса EmployeeSerialaizer для сериализации сотрудников
    pagination_class = StaffPagination # экземпляр класса StaffPagination для пагинации списка сотрудников


# 7.JWT АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЕЙ

 Устанавливаем библиотеки JWT и Djoser:
 >>(venv) pip install djoser djangorestframework-simplejwt

 Регистрируем приложения
 ***staffmanager\staffmanager\settings.py***
from datetime import timedelta      # для установки времени жизни токена
from django.conf import settings    # для импорта настроек из settings.py (SECRET_KEY для SimpleJWT)

 ВАЖНО!!! Приложение Djoser должно быть зарегистрировано ПОСЛЕ django.contrib.auth и rest_framework, чтобы переписать нужные адреса
 INSTALLED_APPS = [
----------------------------------------
    'django.contrib.auth',
--------------------------------------------
    "rest_framework",               # Для работы с API
    "rest_framework.authtoken",      # Для авторизации через токен    
    "djoser",                       # Для авторизации токеном
    "rest_framework_simplejwt",     # для авторизации через токен c SimpleJWT
 ]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', # # Авторизация через токен c SimpleJWT
    ],
}
#Настройки для авторизации через токен c SimpleJWT - копируем из документации по SimpleJWT
#https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    # Обязательно импортировать from datetime import timedelta
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),         # # Устанвливаем время жизни токена
    'AUTH_HEADER_TYPES': ('Bearer',),                   # Тип заголовка для авторизации
}

    # Добавляем маршруты для представлений в паттерны в корневом файле staffmanager\staffmanager\urls.py
***staffmanager\staffmanager\urls.py***
    # Для работы с JWT токенами
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

    # ЭНДПОЙНТЫ для JWT получения, обновления и верификации токена
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
ВАЖНО!! ПОСЛЕ ВСЕХ НАСТРОЕК ДЕЛАЕМ МИГРАЦИЮ БД >>py -m manage migrate

Создадим через административную панель три группы пользователей:
Customer    - Может просматривать каталог.
Supervisor  - Может просматривать сотрудников и перемещать сотрудников между столами.
Admin       - Может добавлять, изменять, удалять сотрудников,
              в .т.ч. их роли, навыки, изображения, а также перемещать их между столами.

При авторизации пользователя в API по токену, полученному по его username/passsword для админки,
его права будут действовать и в API.

Имитация авторизации по токенам из стороннего приложения производилась через программу POSTMAN

ПОЛУЧАЕМ ТОКЕН
Заходим по адресу 
http://127.0.0.1:8000/api/token/
Получаем контент для ввода имени и пароля пользователя
{
    "username": "",
    "password": ""
}
Заполняем и отправляем ( жмём POST)
Пользователь user1 имет доступ ко всем правам
{
    "username": "user1",
    "password": "user1"
}
Получаем два токена для входа и для обновления
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTUxNTY4OCwiaWF0IjoxNzU5MDgzNjg4LCJqdGkiOiJmMGJmYTMzODY5MGU0NTQ2OWE4N2UzZDdlMWFjYTI1NCIsInVzZXJfaWQiOiIxIn0.yW4o7u61voyMvLioUopYInoQNo1hzDkAwpCjnuzxYCw",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5MTEzNjg4LCJpYXQiOjE3NTkwODM2ODgsImp0aSI6ImIzYzc2ZDA0ODU4ZjRhNjk4MWI1Y2FkMjczZjI5OTg3IiwidXNlcl9pZCI6IjEifQ.k5YMygeSylTltv7256zQ-4sS2tmzQYEUiE-t-imegYg"
}
Пользователь user2 в группе Suprvisor может только просматривать сотрудников
{
    "username": "user2",
    "password": "user2"
}
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTUxNzQ4MiwiaWF0IjoxNzU5MDg1NDgyLCJqdGkiOiJjZDBhZGE4MjZhYTA0ZmUwYmIzZDA2YzExNTA0ZWI2MyIsInVzZXJfaWQiOiIyIn0.LgcibxYF9vlpXb1CvWUj4jw84ArKdkqZS6aUVPBVo4A",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5MTE1NDgyLCJpYXQiOjE3NTkwODU0ODIsImp0aSI6IjE4ZjRkZDMwNjRmYTQ0Y2M4NDY3MDM3NGMzYmJmZThjIiwidXNlcl9pZCI6IjIifQ.sN8QyhMR7mnRPChZwUvKEBk8PxsOjBxyjJtz4FLaaJo"
}




# *******************ДЗ 7  Django Деплой и инфраструктура****************************

Что нужно сделать:

# СОЗДАТЬ ДОКУМЕНТАЦИЮ В ФОРМАТЕ Swagger.
Выполнено в ДЗ_6
Доступ свободный по адресу
http://127.0.0.1:8000/swagger/

# НАСТРОИТЬ CORS ДЛЯ ОТКРЫТОГО API.
pip install django-cors-headers

***staffmanager\staffmanager\settings.py***
INSTALLED_APPS = [
------------------------------------------------------------------------------------------------
    "corsheaders",                          # Для указания разрешенных источников и заголовков запросов
-----------------------------------------------------------------------------------------------------
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",    # Поле для CORS должно быть первым
---------------------------------------------------------------
]
#CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_METHODS = [ 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [ 'Authorization', 'Content-Type', ]

# ОБЕРНУТЬ ПРИЛОЖЕНИЕ В КОНТЕЙНЕР Docker И docker-compose для быстрого запуска инфраструктуры (например, PostgreSQL).

1.Скачиваем и устанавливаем приложение Docker для win11
https://www.docker.com/products/docker-desktop/

2.Отключаем DEBUG TOOLBAR
***staffmanager\staffmanager\settings.py***
    #"debug_toolbar.middleware.DebugToolbarMiddleware",  # Должен быть последним, для продакшена закомментировать
    #"debug_toolbar",                                    # для отладки, для продакшена закомментировать
***staffmanager\staffmanager\urls.py***
    #path("__debug__/", include(debug_toolbar.urls)), # для отладки, для продакшена закомментировать

3.Сохраняем зависимости проекта в файле  .\staffmanager\requirements.txt
>>>(.venv) PS C:...\staffmanager> pip freeze > requirements.txt

4.Сохраняем чувствительные переменные окружения в файле вне проекта ./.env.dev (.env.prod)
Получить переменную окружения можно по ключу 'NAME' из словаря переменных окружения
os.environ.get('NAME')

DEBUG=1
SECRET_KEY=django-insecure-=jv8f-b_8uv8nqr!n_p30zqyf3zur$ex_v81elysd5possu6kx
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=StaffManager
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

5.Файлы в папке проекта staffmanager:

Проект должен запускаться через docker-compose up.
Опишите порядок запуска приложения.

1.Заменим БД на postgres
pip install psycopg2
python manage.py dumpdata > datadump.json # Бэкап базы данных
или
python manage.py dumpdata --indent=2 --exclude auth.permission --exclude contenttypes -o datadb.json
или (самое правильное для русского текста)
py -Xutf8 manage.py dumpdata -o datadump.json
py -Xutf8 manage.py dumpdata --natural-foreign --indent=2 -o datadump3.json

***staffmanager\staffmanager\settings.py***
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Staffmanager',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Make sure you can connect on PostgreSQL. Then:
Run this on Django shell to exclude contentype data
(.venv) python3 manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
выполнить миграцию структуры таблиц
(.venv) python manage.py makemigrations
(.venv) python manage.py migrate
восстановить данные
(.venv) python manage.py loaddata datadump.json # загрузка данных в БД

# *******************ДЗ 7  Django Деплой и инфраструктура****************************

1. Создать документацию в формате Swagger. 
Автоматическая генерация документации в форматах Swagger/ReDoc была реализована в dev-проекте Staffmanager при выполнении ДЗ_6 Django REST Framework.

2. Настроить CORS для открытого API. 
Механизм CORS (Cross-Origin Resource Sharing)  служит для установки явных разрешений на допуск к Django-серверу из внешних доменов при кросс-доменных запросах путём вставки в ответы соответствующих заголовков. Разрешения включают заголовки, ip-адреса, методы.
Был реализован в dev-проекте Staffmanager с использованием пакета django-cors-headers.

Установка пакета:
pip install django-cors-headers

Настройка в settings.py:
INSTALLED_APPS = [
------------------------------------------------------------------------------------------------
    "corsheaders",					# Для указания разрешенных источников запросов, методов и заголовков запросов
-----------------------------------------------------------------------------------------------------
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",		# Поле для CORS должно быть первым
---------------------------------------------------------------
]
#CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [			# Порт :3000 обычно используется при разработке веб-серверов, разворачиваемых из докер-контейнеров
    "http://localhost:3000",					
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_METHODS = [ 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [ 'Authorization', 'Content-Type', ]


3. Обернуть приложение в контейнер Docker и docker-compose – для быстрого запуска инфраструктуры (например, PostgreSQL). 
Проект должен запускаться через docker-compose up. Опишите порядок запуска приложения.

ВАЖНО!!!
Для использования «контейнеризации», т.е., изоляции,  dev-проекта Staffmanager  было установлено приложение docker-desktop, предоставляющее инструменты для работы с Docker-контейнерами через консоль и через графический интерфейс с установкой WSL -  Linux-подсистемы для Windows. При этом не требуется запускать виртуальную машину с Linux.

Порядок запуска приложения из контейнера.

0. Отключаем DEBUG TOOLBAR (комментируем строки с debug_toolbar)
***staffmanager\staffmanager\settings.py***
    #"debug_toolbar.middleware.DebugToolbarMiddleware", 
    #"debug_toolbar",       
***staffmanager\staffmanager\urls.py***
    #path("__debug__/", include(debug_toolbar.urls)), 

А. Создание файлов 
Для построения образа проекта и запуска контейнера (контейнеров) были созданы файлы:

Внутри проекта Staffmanager 
Dockerfile – управление сборкой образа проекта;
entrypoint.sh – для контроля за подключением к базе данных, выполнения обязательной миграции баз данных и запуска контейнерного сервера проекта;
requirements.txt – для установки зависимостей проекта. Этот файл используется в Dockerfile для загрузки и установки необходимых python-пакетов, используемых в проекте.
>>>(.venv) PS C:...\staffmanager> pip freeze > requirements.txt


Вне проекта Staffmanager
docker-compose_...yml  - для определения сервисов и их зависимостей. Запуск одного или двух двух контейнеров с web-сервисом (сервер) и db-сервисом (для базы PostgreSQL).
.env.dev – файл с набором переменных окружения, необходимых для работы проекта в контейнере. Этот файл используется в docker-compose_...yml  для настройки переменных окружения перед запуском контейнеров
Получить переменную окружения можно по ключу 'NAME' из словаря переменных окружения
os.environ.get('NAME')

DEBUG=1
SECRET_KEY=django-insecure-=jv8f-b_8uv8nqr!n_p30zqyf3zur$ex_v81elysd5possu6kx
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=StaffManager
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres

В dev-проекте Staffmanager изначально была заполнена и настроена база SQLite3 “db.sqlite3”. 
Поэтому в entrypoint.sh была реализована логика выбора типа базы данных. Также реализованы функция wait_for_postgres() ожидания базы PostgreSQL,  так как запуск web-сервиса возможен только после удачного запуска сервера postgres, и функция create_db() для создания пустой базы, если такой базы ещё нет. Эти функции используют psql (клиент для работы с базой postgres через терминал) и утилиты pg_isready (проверки состояния соединения с сервером базы), grep (поиск строк по шаблону). Это требует установки postgresql-клиента в Dockerfile
RUN apt-get update && \
    apt-get install -y \
    postgresql-client

Реализованы разные варианты файлов для команды docker-compose для проекта с той или иной базой данных.
docker-compose_sqlite.yml – для запуска проекта с исходной базой «db.sqlite3». Запускается только один web-сервис, так как база находится внутри проекта. По этой же причине здесь нет нужды описывать переменные окружения для базы (кроме одной DATABASE: sqlite для работы  entrypoint.sh) – они представлены в  settings.py
docker-compose_sqlite.yml – для запуска проекта с базой postgres «StaffManager». Запускаются два сервиса web- и db. Здесь также реализована проверка условия рабочего состояния контейнера db-сервиса - база подключена, используя команду healthcheck: и условие condition: service_healthy.
Так как база postgres «StaffManager» сначала не существовала, то после первого запуска контейнера будет создана пустая база с нужной структурой, но для работы с ней нужно будет создать суперюзера из консоли Docker-Desktop, находясь в корне проекта (рабочей директории проекта) и запустив python-shell:
PS C:\...\DjangoSynergyProject\staffmanager> python
>>> py manage.py createsuperuser
Создание суперюзера можно было реализовать в entrypoint.sh с логикой проверки на его существование в базе, но так как это однократная операция, то целесообразно не загромождать код.

Б. Сборка Docker-образа 
Команда из места расположения Dockerfile «.»
(.venv) PS … > docker build –t <имя образа> .

B. Запуск контейнера (контейнеров)
Перед запуском контейнеров с Django-проектом требуются 
- установка зависимостей. Это реализовано в Dockerfile с использованием файла requirements.txt
- проверка доступности баз данных. Это реализовано в entrypoint.sh функциями wait_for_postgres() и create_db()
- обязательное проведение миграции баз данных. Это реализовано в entrypoint.sh командой
python manage.py migrate
- разворачивание сервера проекта. Это реализовано командой
python manage.py runserver 0.0.0.0:8000
Эта команда может быть указана или в docker-compose_...yml со ссылкой на неё из entrypoint.sh (exec "$@") или явно в entrypoint.sh
Запуск проекта с помощью команды docker-compose
(.venv) PS … docker-compose -f <file ...yml> up <options>
Опции позволяют запустить сборку образа и развернуть сервер с контейнерами одной командой
(.venv) PS … docker-compose -f <file ...yml> up –d –-build

# Django Extensions
это набор полезных команд и утилит для разработки на Django.
Они включают в себя команды для работы с базой данных, генерации диаграмм моделей и многое другое.

Установка:
(venv) pip install django-extensions
Чтобы делать диаграмму в виде изображения:
(venv) pip install pydotplus
pip install pydot

Настройка:
добавить 'django_extensions' в список INSTALLED_APPS.

Пример использования команды для генерации диаграммы моделей:
С помощью этой команды вы можете визуализировать
структуру вашей базы данных, что особенно полезно при
работе с большими и сложными проектами.
(venv) python manage.py graph_models -a -o models.png
python manage.py graph_models staff staffmanager workplaces --rankdir LR -o staff_models.png --pydot


Настройка шрифта settings.py, используемого утилитой graph_models
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
    'output': 'png',
    'arrow_shape': 'open',
    'fontname': 'Arial',  # Устанавливаем по умолчанию доступный в системе шрифта (исходный шрифт ROBOTO)
}
