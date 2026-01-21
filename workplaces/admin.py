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

# Регистрируем модель в админке Django 
@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    
    # Выводим в админке список сотрудников на рабочих местах
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