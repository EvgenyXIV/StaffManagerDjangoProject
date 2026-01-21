from django.contrib import admin
from .models import Employee, EmployeeImage, Skill, SkillLevel

# Для добавления полей модели сотрудника-пользователя на страницу  пользователя
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Для импорта экспорта данных из базы данных в Excel  и CSV файлы в формате CSV и XLSX
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

# Для добавления кастомного разрешения на изменение рабочего места у сотрудника
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from workplaces.models import Workplace

###############################################################################################################
"""
Так как в проекте используется 2 модели из разных приложений Employee и Workplace, 
то для того чтобы в админке отображались права доступа у пользователей к изменению рабочего места у сотрудника, 
надо добавить пользовательское разрешение на это.
"""
# Добавляем пользовательское разрешение на изменение рабочего места у сотрудника
def add_workplace_permission():
    # Получаем тип содержимого для модели Employee
    content_type = ContentType.objects.get_for_model(Employee)
    # Создаём разрешение
    permission = Permission.objects.create(
        codename="change_employee_workplace",
        name="Право изменять раб.место сотрудника",
        content_type=content_type,
    ) # Создаём разрешение, указываем код разрешения, название разрешения и контент-тип
    return permission
try:
    add_workplace_permission() # Регистрируем кастомное разрешение при загрузке приложения
except: Exception
#####################################################################################################################

# Register your models here.

# Модель для импорта/экспорта данных из базы данных в Excel  и CSV файлы в формате CSV и XLSX
class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'role', 'workplace__table')


@admin.register(Skill)  # Регистрируем модель Skill в админке
class SkillAdmin(admin.ModelAdmin):
    model = Skill

# Декоратор для регистрации модели Employee в админке нужен для того чтобы модель Employee была доступна в админке
@admin.register(SkillLevel)  # Регистрируем модель SkillLevel в админке
class SkillLevelAdmin(admin.ModelAdmin):
    model = SkillLevel


# Inline class для таблицы SkillLevel
# Используется класс TabularInline, который представляет собой
# табличное представление записей в административной панели
class SkillLevelInline(admin.TabularInline):
    model = SkillLevel
    extra = 0


# Регистрируем в админке модель EmployeeImage 
@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    class Meta:
        model = EmployeeImage
        fields = "__all__"
        extra = 3


# Регистриуем  в админке инлайн для изображений сотрудника в табличном виде
class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage


@admin.register(
    Employee
)  # Регистрируем  в админке модель Employee  c инлайном навык(уровень) и подключённым модулем ипорта/экспорта
class EmployeeAdmin(ImportExportModelAdmin):

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
        "role",
        "employment_date",
        "employment_days",
        "employee_skills",
        "workplace",
        "description",
    )
    list_editable = (
        "first_name",
        "middle_name",
        "last_name",
        "role",
        "employment_date",
        "workplace",
        "description",

    )
    search_fields = ("last_name",)
    list_filter = ("skills",)
    list_display_links = ("id",)
    # filter_horizontal = ('skills',)

    inlines = [SkillLevelInline, EmployeeImageInline]

    resources_class = [EmployeeResource]

    # class Meta:
    #     model = Employee
    #     fields = '__all__'
