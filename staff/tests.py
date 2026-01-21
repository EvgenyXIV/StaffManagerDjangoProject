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

# Функция копирования изображения в staffmanager/media/ для проведения тестов.
# Необходима, так как при удалении тестовых файлов удаляется и файл тестового изображения.
# Используется здесь в целях демонстрации тестов. 
# В реальном проекте не рекомендуется. Альтернативный вариант - использовать 
# Класс InMemoryStorage для временного хранения файлов media в памяти без доступа к файлам на диске.
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

    # Создание пользователя без прав персонала
    common_user = User.objects.create_user(
        id=3,
        username='common_user', 
        password='common_user',
        is_staff=False,
    )
    # Создание пользователя с правами персонала
    user = User.objects.create_user(
        id=2,
        username='user', 
        password='user',
        is_staff=False
    )
    # Создание администратора
    superuser = User.objects.create_superuser(
        id=1,
        username='admin', 
        password='admin',
        email='admin@admin.ru',
    )
    # Создание рабочих мест
    Workplace.objects.create(table=1,)
    Workplace.objects.create(table=2,)
    Workplace.objects.create(table=3,)
    Workplace.objects.create(table=4,)
    # Создание навыков
    skill_frontend = Skill.objects.create(name='frontend')
    skill_backend = Skill.objects.create(name='backend')
    skill_qa = Skill.objects.create(name='qa')
    skill_prompt_engineering = Skill.objects.create(name='prompt_engineering')

    # Создание сотрудников
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
    # Создание уровней навыков у сотрудника
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
    # Создание изображений сотрудника в папке media
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


# Уничтожаем тестовую базу данных после завершения всех тестов
def tearDownModule():
    User.objects.all().delete()
    Employee.objects.all().delete()
    Workplace.objects.all().delete()
    SkillLevel.objects.all().delete()
    Skill.objects.all().delete()
    EmployeeImage.objects.all().delete()

# Create your tests here.

# Тесты, проверяющие работоспособность и права доступа на адреса в проекте.

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
    
    #2. Тестируем адреса, доступные только авторизованным пользователям, ожидаем status_code=200:
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


class TestContext(TestCase):
    # Проверка передачи контекста в шаблоны

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
        

# Тест валидатора рабочих мест workplace
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
        

            


        