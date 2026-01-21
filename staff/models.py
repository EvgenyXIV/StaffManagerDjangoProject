from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User  # Импортируем модель User

# Для валидации поля level
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from workplaces.models import Workplace  # Импортируем модель Workplace

# Импортируем класс поля WYSIWYG-редактора django-ckeditor-5
from django_ckeditor_5.fields import (
    CKEditor5Field,
)
from PIL import Image as PILImage  # Импортируем класс Image из библиотеки PIL

from datetime import date  # Импортируем класс date для расчёта стажа

from django.core.exceptions import (
    ValidationError,
)  # Импортируем класс ValidationError для создания валидатора

# Create your models here.


class Skill(models.Model):  # Класс Навык наследник базовой модели Model
    AppConfig.default = False # Для отключения автоматического поиска модели в проекте

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
    AppConfig.default = False # Для отключения автоматического поиска модели в проекте

    # Список ролей сотрудников
    ROLES = (
        ("frontend-developer", "фронтенд разработчик"),
        ("backend-developer", "бэкенд разработчик"),
        ("qa-engineer", "тестировщик"),
        ("project-manager", "руководитель проекта"),
        ("prompt engineer", "промпт-инженер"),
        ("other", "другое"),
    )
    # Расширение модели User через связь с моделью User один к одному
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    # Выбор пола
    gender = models.CharField(
        max_length=10,
        choices=(
            ("male", "Мужской"),
            ("female", "Женский"),
        ),
        verbose_name="Пол",
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    # Отчество (по желанию)
    middle_name = models.CharField(
        max_length=100, verbose_name="Отчество", blank=True, null=True
    )
    # Роль сотрудника
    role = models.CharField(
        choices=ROLES, verbose_name="Роль", default="other", blank=True, null=True
    )
    # Дата приёма на работу
    employment_date = models.DateField(
        verbose_name="Дата приёма на работу", blank=True, null=True
    )
    # Стаж в днях
    employment_days = models.PositiveIntegerField(
        verbose_name="Стаж в днях", blank=True, null=True, default=0, editable=False
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

    # Метод для расчёта стажа
    def save(self, *args, **qkwargs):  # Переопределяем метод сохранения
        if self.employment_date:  # Если дата приёма на работу заполнена
            today = date.today()  # Получаем текущую дату
            days = today - self.employment_date  # Рассчитываем стаж
            self.employment_days = (
                days.days
            )  # Записываем стаж в поле employment_days в днях
        self.full_clean()  # Проверяем валидность модели перед сохранением
        super().save(*args, **qkwargs)  # Продолжаем сохранять базовым методом модели

    
    # Переопределяем метод валидации
    def clean(self):
        self.validate_workplace()  # Вызываем метод валидации рабочего места

    # Метод для валидации рабочего места
    def validate_workplace(self):
        place = self.workplace.table  # Получаем номер рабочего места
        neighbour_workplaces = [place - 1, place + 1]  # Соседние рабочие места
        neighbours = Employee.objects.filter(
            workplace__table__in=neighbour_workplaces
        )  # Сотрудники на соседних рабочих местах
        if self.role == "qa-engineer":  # Если сотрудник тестировщик
            for neighbour in neighbours:
                if (
                    neighbour.role == "frontend-developer"
                ):  # Если соседний сотрудник фронтенд разработчик
                    raise ValidationError(
                        f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом"
                    )
                elif (
                    neighbour.role == "backend-developer"
                ):  # Если соседний сотрудник бэкенд разработчик
                    raise ValidationError(
                        f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом"
                    )
        if (
            self.role == "frontend-developer" or self.role == "backend-developer"
        ):  # Если сотрудник разработчик
            for neighbour in neighbours:
                if (
                    neighbour.role == "qa-engineer"
                ):  # Если соседний сотрудник тестировщик
                    raise ValidationError(
                        f"Сосед {neighbour} {neighbour.role} место № {neighbour.workplace} Нельзя размещать разработчиков и тестировщиков рядом"
                    )

    # Добавляем читабельность в админке
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["-employment_days"]

    # В заголовке карточки сотрудника вместо Employee object() будет имя и фамилия
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Связь сотрудник/навык многие ко многим через модель SkillLevel
class SkillLevel(models.Model):  # Класс Уровень Навыка наследник базовой модели Model
    AppConfig.default = False # Для отключения автоматического поиска модели в проекте

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


# Создание модели для хранения изображений с отношением многие к одному (ForeignKey)
class EmployeeImage(models.Model):
    AppConfig.default = False # Для отключения автоматического поиска модели в проекте

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="employee_gallery"
    )
    image = models.ImageField(
        upload_to="employee_images/", blank=False, null=True, verbose_name="Изображение"
    )
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")
    order = models.PositiveBigIntegerField(
        default=0, verbose_name="Порядок отображения"
    )  # Добавляем поле для сортировки изображений

    class Meta:
        ordering = ["order"]  # Сортируем изображения по порядку

    # Переопределяем метод сохранения изображения (Pillow)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Проверка наличия признака основного изображения
            if self.is_main:
                # Выбираем из базы основные изображения данного сотрудника,
                # кроме нового основного, и делаем их не основными
                EmployeeImage.objects.filter(
                    employee=self.employee, is_main=True
                ).exclude(pk=self.pk).update(is_main=False)

            # Новое изображение сохраняем с изменением размера на 300х300 пикселей (метод библиотеки Pillow)
            img = PILImage.open(self.image.path)
            # max_size = (300, 300)    # Максимальные размеры изображения (реальный размер будет уменьшен до этого значения)
            img = img.resize([300, 300])  # Устанавливаем размер изображения
            # img.thumbnail(max_size, PILImage.Resampling.LANCZOS) # Сжимаем иконку изображения на странице
            img.save(self.image.path)  # Сохраняем изменённое изображение
            return self.image

    def __str__(self):
        if self.is_main:
            return f"Основное изображение для {self.employee} - {self.image.name}"
        else:
            return f"Дополнительное изображение для {self.employee}"
