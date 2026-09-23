from django.shortcuts import render
from django.http import HttpResponse
# Импортируем модели Employee, SkillLevel, Skill, EmployeeImage, User, Workplace
from .models import (
    Employee,
    SkillLevel,
    Skill,
    EmployeeImage,
)
from django.contrib.auth.models import User 
from workplaces.models import Workplace

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)  # для защиты доступа к страницам (для авторизованного пользователя,
# например, для личного кабинета или для дилеров, или ...).
# Указывается на первом месте

# Для работы с классами ListView и DetailView при создании веб-интерфейса модели Employee
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# API-вьюшки
from rest_framework.views import APIView        # для создания API
from rest_framework.response import Response    # для ответа на запросы
from rest_framework import status               # для ответа на запросы
# ВЬЮСЕТЫ для создания API
from rest_framework import mixins, viewsets     # для создания API, mixins - наборы методов для API, viewsets - представления моделей для API
from .serializers import (
    SkillSerialaizer, 
    SkillLevelSerialaizer, 
    EmployeeImageSerialaizer, 
    WorkplaceSerialaizer, 
    UserSerialaizer, 
    EmployeeSerialaizer
)

from .paginators import StaffPagination                      # для пагинации выводим список сотрудников по 2 записи на странице

# from .permissions import IsAuthor               # для проверки прав доступа пользователя

from rest_framework.decorators import action    # для создания метода в API



# 

'''
"""Для простоты вместо html шаблона используем класс HttpResponse - из пакета позволяет отправить текстовое содержимое.
Функция-обработчик index() принимает запрос request и возвращает ответ 'Здесь будет главная страница'  в теге h1 - заголовок первого уровня.
Для вызова этой функции-обработчика надо в Джанго-проекте staffmanager в urls.py внести в список адресов urlpatterns
адрес path('',views.index), по которому она находится. 
Путь 'staffmanager.urls' к файлу с адресами urls.py содержится в переменной ROOT_URLCONF в настройках проекта staffmanager в файле settings.py """
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("<h1>Здесь будет главная страница<h1>")
'''

"""
ЭТИ ФУНКЦИИ index(request):  detail(request, pk): ДЛЯ WEB-интерфейса модели Book ПРИ ПРЕДСТАВЛЕНИИ FBV
"""


def index(request):
    template_name = "staff/index.html"
    try:
        context = {"staff": Employee.objects.all}
    except:
        context = {"staff": "список сотрудников пустой"}
    return render(request, template_name, context)


def detail(request, pk):
    template_name = "staff/detail.html"
    try:
        context = {"book": Employee.objects.get(pk=pk)}
    except:
        context = {"employee": "такого сотрудника нет в списке"}
    return render(request, template_name, context)


"""
ПРЕДСТАВЛЕНИЕ CBV:
Для веб-интерфейса модели Employee используем встроенные классы ListView и DetailView
импортируем классы ListView и DetailView, модель Employee.
Имена шаблонов будут по умолчанию employee_detail.html и employee_list.html:

Для упрощения создания вьюшек для API испоьзуем классы 
viewsets - для представления моделей для API
mixins - наборы методов для API
"""

# Класс ListView для отображения списка пользователей
class UserListView(ListView):
    # template_name = "staff/user_list.html" # Задаем имя и адрес  шаблона user_list.html для вывода списка пользователей
    model = User  # шаблон страницы по умолчанию: staffmanager\templates\staff\user_list.html


# Класс ListView для отображения списка сотрудников
class StaffListView(ListView):
    # template_name = 'staff/index.html' #  Задаем имя и адрес  шаблона index.html для вывода списка сотрудников
    # в приложении (model_name_list.html = employee_list.html)
    # context_object_name = 'staff'      # для шаблонов на уровне приложения имя переменной в шаблоне \staff\templates\staff\index.html,
    # в которой будут передаваться объекты (по умолчанию 'object_list')
    model = Employee  # шаблон страницы по умолчанию: staffmanager\templates\staff\employee_list.html
    context_object_name = "staff"
    paginate_by = 2  # Число записей на странице

    # class Meta:
    #    ordering = ('employment_date')  # Упорядочиваем вывод сотрудников по дате приёма на работу

    # Переопределяем метод get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )  # Получаем базовый контекст запроса в виде словаря из класса ListView
        context["staff_last4"] = self.model.objects.order_by("-employment_date")[
            :4
        ]  # Добавляем в контекст список последних 4х сотрудников, принятых на работу
        context["staff_list_length"] = (
            self.model.objects.count()
        )  # Добавляем в контекст количество сотрудников через агрегацию .count().

        # Выбор типа списка сотрудников на главной странице и на странице staff/.
        # В шаблоне staffmanager\templates\staff\employee_list.html в цикле for надо использовать список сотрудников с именем staff
        pattern_name = (
            self.request.resolver_match.url_name
        )  # Получаем имя url-паттерна при клике на ссылку в базовом шаблоне base.html
        if pattern_name == "staff-last4":
            context["staff"] = context["staff_last4"]
        elif pattern_name == "staff-list-all":
            context["staff"] = context["object_list"]

        """
        # ОПТИМИЗАЦИЯ ЗАПРОСА В БД для получения главных изображений для сотрудников O(1) запросов
        # Одним запросом в БД получаем из EmployeeImage список всех главных изображений для сотрудников 
        # в списке context["staff"]. 
        # (В модели EmployeeImage для сотрудника сохраняется только одно главное изображение)
        main_images = EmployeeImage.objects.filter(
            is_main=True, employee__in=context["staff"]
        )

        # Создаем словарь для быстрого доступа с учётом того, что у сотрудника только одно главное изображение
        main_images_dict = {img.employee_id: img for img in main_images}
        for employee in context["staff"]:   # Для сотрудника по id из словаря получаем в карточку его главное изображение. Оно одно (если есть)
            try:
                employee.main_image = main_images_dict.get(
                    employee.id
                )
            except Exception:
                print(
                    f"employee.id {employee.id} None image"
                )  # Вывод в терминал, если нет главного изображения
        """
        """"""
        # Не оптимальный вариант O(n) запросов, n - количество сотрудников в списке context["staff"]
        # Для каждого сотрудника в списке получаем в карточку главное изображение. Оно у сотрудника единственное (если есть)
        for employee in context["staff"]:
            try:
                main_image = employee.employee_gallery.get(
                    is_main=True
                )  # Получаем главное изображение сотрудника
                employee.main_image = (
                    main_image  # Передаём в карточку сотрудника его главное изображение
                )
            except Exception:
                print(
                    f"employee.id {employee.id} None image"
                )  # Вывод в терминал, если нет главного изображения
        
        return context  # Возвращаем полученный контекст в шаблон
        


# Класс UserDetailView для отображения информации о пользователе
class UserDetailView(LoginRequiredMixin, DetailView):
    # template_name = "staff/user_detail.html"  #  Задаем имя и адрес  шаблона user_detail.html для вывода информации о пользователе
    model = User  # шаблон страницы по умолчанию: staffmanager\templates\staff\user_detail.html


# Класс EmployeeDetailView для html-отображения информации о сотруднике
class EmployeeDetailView(LoginRequiredMixin, DetailView):
    #template_name = "staff/employee_detail.html"  #  Задаем имя и адрес шаблона employee_detail.html для вывода информации о сотруднике
    model = Employee  # шаблон страницы по умолчанию: staffmanager\templates\staff\employee_detail.html

    # Функция для получения списка scillevel_set всех свойств сотрудника, связанных с другими таблицами проекта
    # (это навыки, их описания и уровени навыков)  для отображения через шаблон страницы подробных сведений о сотруднике
    def get_queryset(self):
        return Employee.objects.prefetch_related(
            "skilllevel_set"
        ).all()  # Возвращаем список уровней навыков для всех сотрудников

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_image"] = self.object.employee_gallery.get(
            is_main=True
        )  # Получаем в карточку сотрудника главное изображение
        return context  # Возвращаем полученный контекст в шаблон
    
    
# ВЬЮСЕТЫ ДЛЯ API
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()      # Получаем список всех навыков
    serializer_class = SkillSerialaizer # экземпляр класса SkillSerialaizer для сериализации навыков

class SkillLevelViewSet(viewsets.ModelViewSet):
    queryset = SkillLevel.objects.all()  # Получаем список всех уровней навыков
    serializer_class = SkillLevelSerialaizer # экземпляр класса SkillLevelSerialaizer для сериализации уровней навыков

class EmployeeImageViewSet(viewsets.ModelViewSet):
    queryset = EmployeeImage.objects.all()  # Получаем список всех изображений сотрудников
    serializer_class = EmployeeImageSerialaizer # экземпляр класса EmployeeImageSerialaizer для сериализации изображений сотрудников

class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.all()  # Получаем список всех рабочих мест
    serializer_class = WorkplaceSerialaizer # экземпляр класса WorkplaceSerialaizer для сериализации рабочих мест

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Получаем список всех пользователей
    serializer_class = UserSerialaizer # экземпляр класса UserSerialaizer для сериализации пользователей

class EmployeeViewSet(viewsets.ModelViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
):
    queryset = Employee.objects.all()       # Получаем список всех сотрудников
    serializer_class = EmployeeSerialaizer  # экземпляр класса EmployeeSerialaizer для сериализации сотрудников
    pagination_class = StaffPagination      # экземпляр класса StaffPagination для пагинации списка сотрудников

        
    """
    Создадим пользовательское разрешение для изменения рабочего места сотрудника на его api-странице
    """
    
    @action(detail=True, methods=["PATCH", "PUT", "GET"])   # Декоратор для изменения рабочего места сотрудника
    def change_workplace(self, request, pk=None):           # Метод для изменения рабочего места сотрудника
        employee = self.get_object()                        # Получаем объект сотрудника
        print(employee)
        #request = employee.workplace_id  # Получаем ID рабочего места из запроса
        print(request)

        # Проверяем наличие пользовательского разрешения
        if not request.user.has_perm("employees.change_employee_workplace"):
            return Response({"Ошибка": "Нет прав доступа"}, status=403)
        
        workplace_id = employee.workplace_id # Получаем ID рабочего места
        if not workplace_id:
            return Response({"Ошибка": "Требуется ID рабочего места"}, status=400)
        
        try:
            workplace = Workplace.objects.get(id=workplace_id)
            employee.workplace = workplace
            employee.save()
            return Response(EmployeeSerialaizer(employee).data, status=200) # 
        except Workplace.DoesNotExist:
            return Response({"Ошибка": "Рабочее место не найдено"}, status=404)
        
    """
    """
    def update(self, request, *args, **kwargs): # Метод для обновления данных сотрудника
        partial = kwargs.pop('partial', False)  # Получаем флаг для частичного обновления (метод PATCH)
        instance = self.get_object()            # Получаем объект сотрудника
        
        # Проверяем права доступа
        if not request.user.has_perm('app_name.change_employee_workplace'):
            return Response({'error': 'Нет прав доступа'}, status=403)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)  # Сериализуем данные
        serializer.is_valid(raise_exception=True)   # Проверяем валидность данных
        self.perform_update(serializer)             # Выполняем обновление данных
        return Response(serializer.data)            # Возвращаем обновленные данные
