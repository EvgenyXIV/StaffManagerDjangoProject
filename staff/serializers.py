from rest_framework import serializers      # Импортируем сериалайзеры из rest_framework 
                                            # для сериализации данных в формате JSON 
                                            # с использованием встроенного класса ModelSerializer
from django.contrib.auth.models import User # Импортируем модель User из django.contrib.auth.models 
                                            # для работы с пользователями
from .models import Skill,SkillLevel, EmployeeImage, Employee 
from workplaces.models import Workplace


# Сериалайзеры для моделей проекта StaffManager

class SkillSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SkillLevelSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = SkillLevel
        fields = '__all__'

class EmployeeImageSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = '__all__'

class WorkplaceSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = '__all__'

class UserSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployeeSerialaizer(serializers.ModelSerializer):
    # Вложенные сериалайзеры для связанных моделей
    skills = SkillSerialaizer(many=True, read_only=True)
    skilllevel = SkillLevelSerialaizer(read_only=True, many=True)
    workplace = WorkplaceSerialaizer(read_only=True)
    user = UserSerialaizer(read_only=True)
    employeeimage = EmployeeImageSerialaizer(read_only=True, many=True)

    class Meta:
        model = Employee
        fields = '__all__'
